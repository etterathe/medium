import streamlit as st

class ChatInterface:
    def __init__(self, invoke_chain):
        self.initialize_chat_history()
        self.invoke_chain = invoke_chain

    def initialize_chat_history(self):
        """Initializes chat history in the session state."""
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def display_chat_history(self):
        """Displays chat messages from history on app rerun."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def accept_user_input(self):
        """Accepts user input and returns it."""
        return st.chat_input("Chat with your database")

    def handle_user_message(self, prompt):
        """Handles user message by adding it to chat history and displaying it."""
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    def generate_response(self, prompt):
        """Generates and displays assistant response."""
        with st.spinner("Generating response..."):
            with st.chat_message("assistant"):
                response = self.invoke_chain(prompt, st.session_state.messages)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    def clear_chat_history(self):
        """Clears chat history."""
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

    def run(self):
        """Main method to run the chat app."""
        self.display_chat_history()
        if prompt := self.accept_user_input():
            self.handle_user_message(prompt)
            self.generate_response(prompt)
