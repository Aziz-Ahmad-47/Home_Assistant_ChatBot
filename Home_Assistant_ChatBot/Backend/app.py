import streamlit as st
from rag.chat import ask_home_assistant

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Daily Home Management Assistant",
    page_icon="🏠",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: #f5f7fb;
}

.main-title {
    font-size: 32px;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 5px;
}

.subtitle {
    color: #6b7280;
    font-size: 15px;
    margin-bottom: 25px;
}

.chat-user {
    background: #2563eb;
    color: white;
    padding: 12px 16px;
    border-radius: 15px 15px 4px 15px;
    margin: 10px 0;
    margin-left: 20%;
}

.chat-assistant {
    background: white;
    color: #1f2937;
    padding: 14px 16px;
    border-radius: 15px 15px 15px 4px;
    margin: 10px 20% 10px 0;
    border: 1px solid #e5e7eb;
}

.online {
    color: #16a34a;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🏠 Home Assistant")

    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.markdown("### ⚡ Quick Questions")

    quick_questions = [
        "What are my pending family tasks?",
        "How much was the electricity bill?",
        "How much did we spend on groceries?",
        "Show me our monthly expenses.",
        "Make a budget for a family of four.",
        "Which month had the highest electricity bill?",
        "Show me recent grocery purchases."
    ]

    for question in quick_questions:
        if st.button(question, use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })

            with st.spinner("Thinking..."):
                answer = ask_home_assistant(question)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            st.rerun()

    st.markdown("---")

    st.markdown(
        '<div class="online">🟢 Assistant Online</div>',
        unsafe_allow_html=True
    )

# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🏠 Daily Home Management Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI-powered assistant for household expenses, bills, groceries and family tasks.'
    '</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# WELCOME MESSAGE
# --------------------------------------------------

if not st.session_state.messages:

    st.markdown("""
    <div style="
        background:white;
        padding:30px;
        border-radius:18px;
        text-align:center;
        border:1px solid #e5e7eb;
        margin-bottom:25px;
    ">

    <div style="font-size:55px;">🏡</div>

    <h2>Welcome Home!</h2>

    <p style="color:#6b7280;">
    I can help you manage household expenses, bills,
    groceries and family tasks.
    </p>

    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# DISPLAY CHAT
# --------------------------------------------------

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="chat-user">
            <b>You</b><br>
            {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="chat-assistant">
            <b>🏠 Home Assistant</b><br>
            {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask your Home Assistant..."
)

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.spinner("Thinking..."):

        try:
            answer = ask_home_assistant(question)

        except Exception as error:
            answer = (
                "Sorry, something went wrong while processing your question."
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()