"""
Challenge implementation with the Fixed Window Counter algorithm to enforce rate limits
"""


import jwt
import time
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort

from cache import RedisClient, CacheClientInterface


app = Flask(__name__)

# Load configuration from .env file
load_dotenv()

# Configuration
requests_per_minute = int(os.getenv('REQUESTS_PER_MINUTE', 100))


def get_user_id_from_jwt(token):
    """
    Extracts the user ID from the JWT token.

    Args:
        token (str): JWT token.

    Returns:
        str: User ID extracted from the token.

    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token is invalid.
    """
    try:
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        abort(401, 'Token expired. Please log in again.')
    except jwt.InvalidTokenError:
        abort(401, 'Invalid token. Please log in again.')


class FixedWindow:

    def __init__(self, cache_server: CacheClientInterface, requests_per_minute: int):
        self.requests_per_minute = requests_per_minute
        self.cache_server = cache_server

    def get_window_start_time(self):
        """
        Gets the start time of the current minute.

        Returns:
            int: Start time of the current minute.
        """
        return int(time.time() / 60) * 60  # Start of the current minute

    def is_within_rate_limit(self, user_id):
        """
        Checks if the user is within the rate limit for the current minute.

        Args:
            user_id (str): User ID.

        Returns:
            bool: True if the user is within the rate limit, False otherwise.
        """
        window_start_time = self.get_window_start_time()
        key = f"{user_id}:{window_start_time}"
        current_count = self.cache_server.get(key)
        if current_count is None:
            current_count = 0
        else:
            current_count = int(current_count)
        if current_count < self.requests_per_minute:
            self.cache_server.incr(key)
            self.cache_server.expire(key, 60)  # Expire in 60 seconds
            return True
        else:
            return False

    def rate_limit(self, token):
        """
        Checks if the user identified by the JWT token is within the rate limit.

        Args:
            token (str): JWT token.

        Returns:
            bool: True if the user is within the rate limit, False otherwise.
        """
        user_id = self.get_user_id_from_jwt(token)
        return self.is_within_rate_limit(user_id)


def handle_api_request(redis_client, requests_per_minute):
    """
    Handle API requests.

    This function performs rate limiting logic and returns appropriate responses.

    Args:
        redis_client: Redis client object.
        requests_per_minute (int): Maximum number of requests per minute.

    Returns:
        tuple: JSON response, HTTP status code, and response headers.
    """

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Authorization token required'}), 401

    fw_obj = FixedWindow(redis_client, requests_per_minute)

    if fw_obj.rate_limit(token):
        return jsonify({'message': 'Request accepted.'}), 200
    else:
        reset_time = fw_obj.get_window_start_time() + 60
        reset_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reset_time))
        headers = {'Retry-After': reset_time_str}
        return jsonify({'error': f'Rate limit exceeded. Try again in {reset_time_str}'}), 429, headers


@app.route('/api', methods=['POST'])
def api():
    """
    Endpoint for API requests.

    Returns:
        Response: JSON response.
    """

    return handle_api_request(RedisClient(host='localhost', port=6379, db=0), requests_per_minute=100)

if __name__ == '__main__':
    app.run(debug=True)
