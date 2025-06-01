import os
import streamlit as st
from streamlit_oauth import OAuth2Component
import openai

# Set environment variables
AUTHORIZE_URL = os.environ.get('AUTHORIZE_URL')
TOKEN_URL = os.environ.get('TOKEN_URL')
REFRESH_TOKEN_URL = os.environ.get('REFRESH_TOKEN_URL')
REVOKE_TOKEN_URL = os.environ.get('REVOKE_TOKEN_URL')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
SCOPE = os.environ.get('SCOPE')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Prompts
SYSTEM_PROMPT = """
    You are a helpful agent who always provides with concise responses.
"""
DEFAULT_USER_PROMPT = """
    What files are in the glroland/sudoku repository?
"""

# Create OAuth2Component instance
oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

# Check if token exists in session state
if 'token' not in st.session_state:
    # If not, show authorize button
    result = oauth2.authorize_button("Authorize", REDIRECT_URI, SCOPE)
    if result and 'token' in result:
        # If authorization successful, save token in session state
        st.session_state.token = result.get('token')
        st.rerun()
else:
    # If token exists in session state, show the token
    token = st.session_state['token']
    st.json(token)
    if st.button("Refresh Token"):
        # If refresh token button is clicked, refresh the token
        token = oauth2.refresh_token(token)
        st.session_state.token = token
        st.rerun()

    # Get the user prompt
    user_prompt = st.text_area("Prompt", DEFAULT_USER_PROMPT.strip(), height=68)
    if st.button("Ask AI"):
        # Invoke the LLM
        openai.api_key = OPENAI_API_KEY
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        # Display the repsonse
        response_content = response.choices[0].message.content
        st.write("AI> ", response_content)
