class SessionManager:
    def __init__(self):
        # Store sessions in a dictionary
        self.sessions = {}
        # self.llm = llm  # Save the LLM object to initialize the ConversationChain

    def get_session(self, session_id: str):
        # If session does not exist, create it with default data and a new ConversationChain
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "history": [],       # A list of messages (user and AI)
                "user_data": {"name":"", "age":"", "email":""},     # A dictionary for user-specific information (e.g., name, age)
                # "conversation_chain": ConversationChain(llm=self.llm),  # ConversationChain instance for this session
            }
        return self.sessions[session_id]
