import redis
import json
from datetime import datetime, timedelta

import redis
import json
from datetime import timedelta

redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

# class SessionManager:
#     def __init__(self):
#         # Store sessions in a dictionary
#         self.sessions = {}
#         # self.llm = llm  # Save the LLM object to initialize the ConversationChain

#     def get_session(self, session_id: str):
#         # If session does not exist, create it with default data and a new ConversationChain
#         if session_id not in self.sessions:
#             self.sessions[session_id] = {
#                 "history": [],       # A list of messages (user and AI)
#                 "user_data": {"name":"", "age":"", "email":""},     # A dictionary for user-specific information (e.g., name, age)
#                 # "conversation_chain": ConversationChain(llm=self.llm),  # ConversationChain instance for this session
#             }
#         return self.sessions[session_id]


class SessionManager:
    def __init__(self, redis_host="localhost", redis_port=6379, session_ttl=3600):
        """
        Initialize the SessionManager with Redis connection.
        
        Args:
            redis_host (str): The Redis host (default: localhost).
            redis_port (int): The Redis port (default: 6379).
            session_ttl (int): Time-to-live for session data in seconds (default: 1 hour).
        """
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
        self.session_ttl = session_ttl  # Session expiry time in seconds

    def get_session(self, session_id: str):
        """
        Retrieve a session from Redis. Create a new session if it doesn't exist.
        
        Args:
            session_id (str): The unique ID for the session.
        
        Returns:
            dict: The session data.
        """
        key = f"session:{session_id}"
        session_data = self.redis_client.get(key)
        
        if session_data:
            # Parse existing session data from Redis
            return json.loads(session_data)
        else:
            # Create a new session if it doesn't exist
            session_data = {
                "history": [],  # A list of messages (user and AI)
                "user_data": {"name": "", "age": "", "email": ""},  # User-specific information
            }
            # Save new session to Redis
            self.redis_client.setex(key, timedelta(seconds=self.session_ttl), json.dumps(session_data))
            return session_data

    def save_session(self, session_id: str, session_data: dict):
        """
        Save a session to Redis.
        
        Args:
            session_id (str): The unique ID for the session.
            session_data (dict): The session data to save.
        """
        key = f"session:{session_id}"
        # Save session data with TTL
        self.redis_client.setex(key, timedelta(seconds=self.session_ttl), json.dumps(session_data))

    def delete_session(self, session_id: str):
        """
        Delete a session from Redis.
        
        Args:
            session_id (str): The unique ID for the session.
        """
        key = f"session:{session_id}"
        self.redis_client.delete(key)

