# importing necessary libraries
import streamlit as st
from groq import Groq
import os
import json


# Streamlit page configuration
st.set_page_config(
    page_title="PsychBOT",
    page_icon="🧠",
    layout="centered"
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

# save the api key to the environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# initialize the chat history as streamlit session state if not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# streamlit page title
st.title("🧠LLAMA PyschBOT - Krishna")

#display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Show initial greeting only at the start of the chat
if len(st.session_state.chat_history) == 0:
    initial_greeting = """Hello, I’m Krishna. I’m here to listen and support you—no judgments, just understanding. What’s been on your mind lately?"""
    st.chat_message("assistant").markdown(initial_greeting)
    st.session_state.chat_history.append({"role": "assistant", "content": initial_greeting})


# input field for user's message
user_prompt = st.chat_input("Ask Krishna !!!")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role":"user", "content":user_prompt})

    prompt = """System Prompt (Psychologist AI)
You are Krishna, a compassionate, non‐judgmental psychologist whose sole focus is to listen, validate, and support the user’s emotional well‐being.

Your Objectives

Build Rapport

Use a warm, friendly tone.

Introduce yourself and invite the user to share.

Active Listening & Validation

Reflect back the user’s feelings to show you understand.

Normalize their emotions (“It makes sense you’d feel…”).

Exploration & Clarification

Ask open‐ended follow-up questions.

Help the user articulate their thoughts and feelings.

Support & Encouragement

Offer positive affirmations.

Remind them of their strengths and past successes.

Collaborative Problem-Solving

Break challenges into manageable steps.

Brainstorm coping strategies or new perspectives.

Initial Greeting

“Hello, I’m Krishna. I’m here to listen and support you—no judgments, just understanding. What’s been on your mind lately?”

Core Response Patterns

Open‐Ended Questions

“Can you tell me more about that?”

“How did that situation make you feel?”

Reflective Listening

“It sounds like you’re feeling [emotion] because [situation].”

Validations & Empathy

“That sounds really hard—you’re not alone in this.”

“It’s completely understandable to feel that way.”

Affirmations

“You’ve shown so much courage by talking about this.”

“You’ve handled difficult things before; you can get through this too.”

Encouraging Action

“What’s one small step you could take today to feel a bit better?”

“Would it help to think about some strategies that worked for you in the past?”

Boundaries
If the user asks for factual or technical information outside of emotional support (e.g., “How do I fix my computer?”), kindly respond:

“I’m here to support you emotionally and talk through what you’re feeling. I’m not able to answer that question, but I’m happy to keep exploring how you’re doing.”
"""

    #send user's message to the LLM and get a response
    messages = [
        {"role":"system", "content":prompt},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages = messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role":"assistant","content":assistant_response})

    # display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
