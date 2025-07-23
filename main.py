import streamlit as st
import requests
import os
from dotenv import load_dotenv
import glob
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(page_title="ashiplexity", page_icon="assets/logo.png", layout="wide")

# Custom CSS
st.markdown(
    """
<style>
    /* Import Inter font (similar to FK Grotesk Neue) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide default Streamlit chrome */
    #MainMenu, footer {visibility: hidden;}
    
    /* Fix header and footer colors to match dark theme */
    header, .stHeader {
        background-color: #181B1A !important;
        color: #ECECEC !important;
    }
    
    footer, .stFooter {
        background-color: #181B1A !important;
        color: #ECECEC !important;
    }
    
    /* Fix browser chrome colors */
    .stApp > header {
        background-color: #181B1A !important;
    }
    
    .stApp > footer {
        background-color: #181B1A !important;
    }
    
    /* Dark theme with Inter font */
    .stApp {
        background-color: #181B1A;
        color: #ECECEC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Apply font to all elements */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Perplexity-style input */
    .perplexity-input {
        background: #1E2120 !important;
        border-radius: 24px !important;
        border: 1px solid #353945 !important;
        color: #ECECEC !important;
        font-size: 16px !important;
        padding: 12px 20px !important;
        width: 200px !important;
        margin: 20px auto !important;
        display: block !important;
        height: 100px !important;
    }
    
        /* Quick prompt button hover effect */
    .stButton > button:hover {
        border-color: #31B9C7 !important;
        color: #31B9C7 !important;
        background-color: transparent !important;
    }
    
    /* Quick prompt button click effect */
    .stButton > button:active {
        background-color: rgba(33, 129, 141, 0.5) !important;
        border-color: #21818D !important;
        color: #21818D !important;
    }
    
    /* Override any red error states */
    .stButton > button {
        border-color: #353945 !important;
        color: #ECECEC !important;
        background-color: #1E2120 !important;
    }
    
    /* Quick prompt button hover effect */
    .stButton > button:hover {
        border-color: #31B9C7 !important;
        color: #31B9C7 !important;
        background-color: transparent !important;
    }
    
    /* Quick prompt button click effect */
    .stButton > button:active {
        background-color: rgba(33, 129, 141, 0.5) !important;
        border-color: #21818D !important;
        color: #21818D !important;
    }
    
    /* Override any red error states */
    .stButton > button {
        border-color: #353945 !important;
        color: #ECECEC !important;
        background-color: #1E2120 !important;
    }
    
    /* Override input error states */
    input[data-testid="stTextInput"] {
        border-color: #353945 !important;
        color: #ECECEC !important;
        background-color: #1E2120 !important;
    }
    
    input[data-testid="stTextInput"]:focus {
        border-color: #31B9C7 !important;
        outline: none !important;
    }
    
    input[data-testid="stTextInput"]:hover {
        border-color: #31B9C7 !important;
        box-shadow: 0 0 0 1px #31B9C7 !important;
    }
    
    input[data-testid="stTextInput"]:active {
        border-color: #21818D !important;
        background-color: rgba(33, 129, 141, 0.1) !important;
    }
    
    /* Override any red error states for inputs */
    input[data-testid="stTextInput"][aria-invalid="true"],
    input[data-testid="stTextInput"].stTextInputError {
        border-color: #353945 !important;
        color: #ECECEC !important;
        background-color: #1E2120 !important;
    }
    
    input[data-testid="stTextInput"][aria-invalid="true"]:focus,
    input[data-testid="stTextInput"].stTextInputError:focus {
        border-color: #31B9C7 !important;
        outline: none !important;
    }
    
    input[data-testid="stTextInput"][aria-invalid="true"]:hover,
    input[data-testid="stTextInput"].stTextInputError:hover {
        border-color: #31B9C7 !important;
        box-shadow: 0 0 0 1px #31B9C7 !important;
    }
    
    .perplexity-input:focus {
        outline: none !important;
        border-color: #31B9C7 !important;
    }
    
    /* Center title image both horizontally and vertically */
    .stImage {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1E2120 !important;
    }
    
    /* Target sidebar elements */
    [data-testid="stSidebar"] {
        background-color: #1E2120 !important;
        width: 160px !important;
        min-width: 160px !important;
        max-width: 160px !important;
    }
    
    /* Sidebar content */
    .css-1lcbmhc {
        background-color: #1E2120 !important;
    }
    
    /* Reduce sidebar width */
    .css-1d391kg {
        width: 200px !important;
        min-width: 200px !important;
        max-width: 200px !important;
    }
    
    /* Ensure main content area adjusts */
    .main .block-container {
        padding-left: 220px !important;
    }
    
    /* Chat bubbles */
    .user-bubble {
        background: #383838;
        color: #ECECEC;
        padding: 12px 16px;
        border-radius: 10px;
        margin: 8px 0;
        text-align: left;
        max-width: 80%;
        margin-right: auto;
    }
    
    .bot-bubble {
        background: #1A1A1A;
        color: #ECECEC;
        padding: 12px 16px;
        border-radius: 20px;
        margin: 8px 0;
        text-align: left;
        max-width: 80%;
    }
    
    /* Status indicators */
    .status-success {
        color: #4CAF50;
        font-weight: bold;
    }
    
    .status-error {
        color: #f44336;
        font-weight: bold;
    }
    
    /* Debug info */
    .debug-info {
        background: #333;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-family: monospace;
        font-size: 12px;
    }

    
    /* Target the bottom block container by data-testid */
    [data-testid="stBottomBlockContainer"] {
        background-color: #181B1A !important;
    }
    

</style>
""",
    unsafe_allow_html=True,
)


# Title and header
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("assets/title.png", width=300)


col1, col2, col3 = st.columns([0.2,1,0.2])
with col2:
    st.markdown('<div style="text-align:center;">Hi! My name is Ashikka Gupta. This is a AI powered chat app built on top of Perplexity. You can use the text box below to learn more about me, or just chat!</div>', unsafe_allow_html=True)


# Load documents function
def load_documents():
    """Load all documents from the documents folder"""
    documents = {}
    doc_files = glob.glob("documents/*.txt")

    for file_path in doc_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                filename = os.path.basename(file_path)
                documents[filename] = content
        except Exception as e:
            st.error(f"Error loading {file_path}: {e}")

    return documents


# Perplexity API function with document context
def ask_perplexity_with_context(query, api_key, documents=None):
    """Ask Perplexity with document context"""
    # Build context from documents
    context = ""
    if documents:
        context = "Based on the following information about Ashikka:\n\n"
        for filename, content in documents.items():
            context += f"--- {filename} ---\n{content}\n\n"

    # Create the full prompt
    full_prompt = f"""{context}Question: {query}

Please provide a clear, engaging, and well-structured answer based on the information provided above. 

Guidelines:
- Write in a friendly, conversational tone that feels personal
- Keep your response concise and focused (aim for 2-3 paragraphs)
- Use markdown formatting to improve readability:
  - **Bold** important points and key achievements
  - Use bullet points (-) for lists and key details
  - Add ### headers for different topics when helpful
- Include specific examples and details when available
- If information is limited, be honest about it
- Make the response feel authentic to Ashikka's voice and experience
- Structure with clear sections and bullet points for easy reading

Answer:"""

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": full_prompt}],
        "max_tokens": 1000,
        "temperature": 0.7,
    }

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )

        if response.status_code != 200:
            raise Exception(
                f"API returned status {response.status_code}: {response.text}"
            )

        response_json = response.json()

        if "choices" not in response_json or not response_json["choices"]:
            raise Exception("No choices in API response")

        content = response_json["choices"][0]["message"]["content"]

        return content

    except requests.exceptions.RequestException as e:
        raise Exception(f"API Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load documents and API key
documents = load_documents()
api_key = os.getenv("PERPLEXITY_API_KEY")

# Dynamic layout based on chat history
user_input = ""  # Initialize user_input

if len(st.session_state.messages) == 0:
    # Initial state - centered input below title
    st.markdown(
        '<div style="text-align: center; margin: 20px 0;">', unsafe_allow_html=True
    )
    user_input = st.text_area(
        "",
        placeholder="Ask anything about Ashikka!",
        label_visibility="collapsed",
        key="perplexity_input",
    )
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Chat active state - input at bottom
    chat_input = st.chat_input("Ask anything about Ashikka...")
    if chat_input:
        user_input = chat_input

# Apply Perplexity styling to the input
st.markdown(
    """
<script>
document.addEventListener('DOMContentLoaded', function() {
    const input = document.querySelector('input[data-testid="stTextInput"]');
    if (input) {
        input.classList.add('perplexity-input');
    }
});
</script>
""",
    unsafe_allow_html=True,
)

# Sidebar with social links
with st.sidebar:
    st.markdown(
        """
    <div style="text-align: center; padding: 0; background-color: #1E2120;">
        <h3 style="color: #ECECEC; margin-bottom: 20px;">Ashikka's Socials</h3>
        <div style="display: flex; flex-direction: column; gap: 15px; align-items: center;">
            <a href="https://www.linkedin.com/in/ashikka-gupta/" target="_blank" style="text-decoration: none; color: #ECECEC; display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 8px; transition: background 0.3s;">
                <span style="width: 20px;"><img style="width: 20px;" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/960px-LinkedIn_logo_initials.png" /></span>
                <span>LinkedIn</span>
            </a>
            <a href="https://youtu.be/-r5PEEKaoTs?si=lbjiXHztyDnlj7GD" target="_blank" style="text-decoration: none; color: #ECECEC; display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 8px; transition: background 0.3s;">
                <span style="font-size: 20px;"><img style="width: 20px;" src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/YouTube_full-color_icon_%282017%29.svg/2560px-YouTube_full-color_icon_%282017%29.svg.png" /></span>
                <span>YouTube</span>
            </a>
            <a href="https://ashikka.medium.com/" target="_blank" style="text-decoration: none; color: #ECECEC; display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 8px; transition: background 0.3s;">
                <span style="font-size: 20px;"><img style="width: 20px;" src="https://cdn-icons-png.flaticon.com/256/5968/5968906.png" /></span>
                <span>Medium</span>
            </a>
            <a href="https://github.com/ashikka" target="_blank" style="text-decoration: none; color: #ECECEC; display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 8px; transition: background 0.3s;">
                <span style="font-size: 20px;"><img style="width: 20px;" src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/github-white-icon.png" /></span>
                <span>GitHub</span>
            </a>
            <a href="https://docs.google.com/document/d/1bx32f4hTLgGIyblQ3tgI2ND8ezQccYw6youj_fJkg60/edit?tab=t.0" target="_blank" style="text-decoration: none; color: #ECECEC; display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 8px; transition: background 0.3s;">
                <span style="font-size: 20px;">📄</span>
                <span>Resume</span>
            </a>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.text("")
    # Clear chat button - only show when there are messages
    if len(st.session_state.messages) > 0:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()


# Main chat area - only show when there are messages
if len(st.session_state.messages) >= 0:
    st.text("")
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f'<div class="user-bubble">{message["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            # Render bot messages with proper markdown
            st.markdown(
                f'<div class="bot-bubble">',
                unsafe_allow_html=True,
            )
            st.markdown(message["content"])

            # Check if this is the response to prompt 4 (beaches/mountains question)
            if (
                "beaches or mountains" in message["content"].lower()
                or "island" in message["content"].lower()
            ):
                try:
                    # Display vacation images in a grid
                    st.markdown("**Here are some photos from my island adventures:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(
                            "vacation/pic_1.jpeg",
                            caption="Broken Beach - Nusa Penida",
                            width=200,
                        )
                        st.image(
                            "vacation/pic_3.jpeg",
                            caption="Yellow Bridge - Nusa Ceningan",
                            width=200,
                        )
                    with col2:
                        st.image(
                            "vacation/pic_2.jpeg", caption="Street in Gili T", width=200
                        )
                        st.image(
                            "vacation/pic_4.jpeg",
                            caption="Sunset in Gili Air",
                            width=200,
                        )
                except Exception as e:
                    st.markdown("*Images not available*")

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Check for API key
        if not api_key or api_key == "your_api_key_here":
            error_msg = "❌ Please add your Perplexity API key to the .env file"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            col1, col2, col3, col4, col5 = st.columns(5)
            with col3:
                with st.spinner("ashiplexity is thinking...."):
                    st.text(" ")
                    st.text(" ")
                    # Get response and add to session state
                    try:
                        response = ask_perplexity_with_context(user_input, api_key, documents)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.session_state.messages.append(
                            {"role": "assistant", "content": error_msg}
                        )
        st.rerun()
    
    if len(st.session_state.messages) == 0:
        st.markdown('<div style="text-align:center; margin-bottom: 10px;">Here are some cool things we can talk about!</div>', unsafe_allow_html=True)
    # Quick prompt buttons - show in initial state below input
    # Show quick prompts in initial state
    st.markdown(
        '<div style="text-align: center; hover:margin: 20px 0;">',
        unsafe_allow_html=True,
    )
    col0, col1, col2, col3, col4, col5 = st.columns([0.5,1,1,1,1,0.5])

    with col1:
        if st.button("Most impactful project?", key="prompt1"):
            query = "What is Ashikka's most impactful project?"
            st.session_state.messages.append({"role": "user", "content": query})

            # Check for API key and make API call
            if not api_key or api_key == "your_api_key_here":
                error_msg = "❌ Please add your Perplexity API key to the .env file"
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
            else:
                try:
                    with st.spinner("ashiplexity is thinking...."):
                        response = ask_perplexity_with_context(query, api_key, documents)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
            st.rerun()

    with col2:
        if st.button("Why AI startup at 23?", key="prompt2"):
            query = "Why did Ashikka become a founding member of an AI startup at 23?"
            st.session_state.messages.append({"role": "user", "content": query})

            # Check for API key and make API call
            if not api_key or api_key == "your_api_key_here":
                error_msg = "❌ Please add your Perplexity API key to the .env file"
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
            else:
                try:
                    with st.spinner("ashiplexity is thinking...."):
                        response = ask_perplexity_with_context(query, api_key, documents)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )
            st.rerun()

    with col3:
        if st.button("Why Perplexity APM?", key="prompt3"):
            query = "Why did Ashikka choose Perplexity for APM?"
            st.session_state.messages.append({"role": "user", "content": query})

            # Check for API key and make API call
            if not api_key or api_key == "your_api_key_here":
                error_msg = "❌ Please add your Perplexity API key to the .env file"
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
            else:
                try:
                    with st.spinner("ashiplexity is thinking...."):
                        response = ask_perplexity_with_context(query, api_key, documents)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )
            st.rerun()

    with col4:
        if st.button("Beaches or mountains?", key="prompt4"):
            query = "What does Ashikka prefer, beaches or mountains?"
            st.session_state.messages.append({"role": "user", "content": query})

            # Check for API key and make API call
            if not api_key or api_key == "your_api_key_here":
                error_msg = "❌ Please add your Perplexity API key to the .env file"
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
            else:
                try:
                    with st.spinner("ashiplexity is thinking...."):
                        response = ask_perplexity_with_context(query, api_key, documents)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# Footer
st.markdown(
    """
<div style='text-align: center; color: #666; font-size: 12px;'>
    Built with ❤️ using Streamlit and Perplexity API
</div>
""",
    unsafe_allow_html=True,
)
