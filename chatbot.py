import streamlit as st
import os
import json
import uuid
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Configure page with enhanced styling
st.set_page_config(
    page_title="Akashsubramani - Conversational Bot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for attractive UI - FIXED VERSION
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
    }
    
    /* Main chat area */
    .main .block-container {
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat messages container - FIXED */
    .stChatMessage {
        background: transparent !important;
        margin: 0.8rem 0 !important;
        padding: 0 !important;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* User message styling - FIXED */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: transparent !important;
    }
    
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]) {
        animation: slideIn 0.3s ease-out;
    }
    
    /* User message content - FIXED */
    [data-testid="stChatMessage"] [data-testid="stChatMessageContent"] {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #1f2937 !important;
        padding: 1rem 1.2rem !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Specific styling for user messages */
    [data-testid="stChatMessage"]:nth-child(odd) [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        margin-left: 15%;
        border: none !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Specific styling for assistant messages */
    [data-testid="stChatMessage"]:nth-child(even) [data-testid="stChatMessageContent"] {
        background: rgba(255, 255, 255, 0.98) !important;
        color: #1f2937 !important;
        margin-right: 15%;
        border-left: 4px solid #667eea !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Avatar styling */
    [data-testid="stChatMessageAvatarContainer"] {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 50%;
        padding: 0.3rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Chat input styling - FIXED */
    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 25px;
        padding: 0.5rem;
    }
    
    [data-testid="stChatInput"] textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 20px !important;
        padding: 1rem 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        color: #1f2937 !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stChatInput"] textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border-left: 4px solid #10b981;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .stInfo {
        border-left-color: #3b82f6;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Custom title styling */
    .custom-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
        }
        to {
            text-shadow: 0 0 30px rgba(118, 75, 162, 0.8);
        }
    }
    
    /* Sidebar title styling */
    .sidebar-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.0rem;
        font-weight: 500;
        margin-bottom: 0.7rem;
    }
    
    /* Memory cards */
    .memory-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }
    
    .memory-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }
    
    /* Status indicators */
    .status-online {
        color: #10b981;
        font-weight: 600;
    }
    
    .status-offline {
        color: #ef4444;
        font-weight: 600;
    }
    
    /* Loading animation */
    .loading-dots {
        display: inline-block;
    }
    
    .loading-dots::after {
        content: "...";
        animation: loading 1.5s infinite;
    }
    
    @keyframes loading {
        0% { content: "."; }
        33% { content: ".."; }
        66% { content: "..."; }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            margin: 0.5rem;
            padding: 1rem;
        }
        
        .custom-title {
            font-size: 2rem;
        }
        
        [data-testid="stChatMessage"]:nth-child(odd) [data-testid="stChatMessageContent"],
        [data-testid="stChatMessage"]:nth-child(even) [data-testid="stChatMessageContent"] {
            margin-left: 0 !important;
            margin-right: 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# Enhanced global memory system
if "user_memory" not in st.session_state:
    st.session_state.user_memory = {
        "name": None,
        "title": None,
        "location": None,
        "facts": [],
        "qa_pairs": [],
        "last_updated": None
    }


if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
    
if "global_conversation_memory" not in st.session_state:
    st.session_state.global_conversation_memory = []
    
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None


# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ NVIDIA API key not found!")
        st.stop()
    
    return OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )


client = get_openai_client()


def extract_user_info(text):
    """Enhanced user information extraction"""
    text_lower = text.lower().strip()
    learned_info = []
    
    # Extract full name (improved)
    if "i am" in text_lower or "my name is" in text_lower:
        import re
        patterns = [
            r"i am ([a-zA-Z]+ [a-zA-Z]+)",
            r"my name is ([a-zA-Z]+ [a-zA-Z]+)",
            r"i am ([a-zA-Z]+)",
            r"my name is ([a-zA-Z]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                name = match.group(1).title()
                if len(name) > 2:
                    st.session_state.user_memory["name"] = name
                    learned_info.append(f"Name: {name}")
                    break
    
    # Extract title/role
    title_patterns = [
        r"i am (?:the )?([a-zA-Z\s]+) of ([a-zA-Z\s]+)",
        r"i am (?:a |an )?([a-zA-Z\s]+)",
    ]
    
    import re
    for pattern in title_patterns:
        match = re.search(pattern, text_lower)
        if match:
            if "of" in pattern:
                title = match.group(1).strip().title()
                location = match.group(2).strip().title()
                if title not in ["Am", "Is", "Are"] and len(title) > 2:
                    st.session_state.user_memory["title"] = title
                    st.session_state.user_memory["location"] = location
                    learned_info.append(f"Title: {title} of {location}")
            else:
                title = match.group(1).strip().title()
                if title not in ["Am", "Is", "Are"] and len(title) > 2:
                    st.session_state.user_memory["title"] = title
                    learned_info.append(f"Title: {title}")
            break
    
    return learned_info


def extract_qa_pairs(user_msg, bot_response):
    """Extract question-answer pairs for FAQ functionality"""
    user_lower = user_msg.lower().strip()
    
    question_indicators = ["who", "what", "where", "when", "why", "how", "?"]
    is_question = any(indicator in user_lower for indicator in question_indicators)
    
    if is_question and len(bot_response) > 10:
        qa_pair = {
            "question": user_msg,
            "answer": bot_response,
            "timestamp": datetime.now().isoformat()
        }
        
        existing = [qa["question"].lower() for qa in st.session_state.user_memory["qa_pairs"]]
        if user_lower not in existing:
            st.session_state.user_memory["qa_pairs"].append(qa_pair)
            st.session_state.user_memory["qa_pairs"] = st.session_state.user_memory["qa_pairs"][-10:]


def get_memory_context():
    """Get comprehensive memory context"""
    context = []
    
    if st.session_state.user_memory["name"]:
        context.append(f"User: {st.session_state.user_memory['name']}")
    
    if st.session_state.user_memory["title"]:
        if st.session_state.user_memory["location"]:
            context.append(f"Role: {st.session_state.user_memory['title']} of {st.session_state.user_memory['location']}")
        else:
            context.append(f"Role: {st.session_state.user_memory['title']}")
    
    if st.session_state.user_memory["facts"]:
        recent_facts = st.session_state.user_memory["facts"][-2:]
        for fact in recent_facts:
            context.append(f"Fact: {fact}")
    
    if st.session_state.user_memory["qa_pairs"]:
        context.append(f"Previous interactions: {len(st.session_state.user_memory['qa_pairs'])} Q&A pairs stored")
    
    return " | ".join(context) if context else ""


def search_qa_memory(question):
    """Search previous QA pairs for similar questions"""
    question_lower = question.lower().strip()
    
    for qa in st.session_state.user_memory["qa_pairs"]:
        qa_question_lower = qa["question"].lower().strip()
        
        if question_lower == qa_question_lower:
            return qa["answer"]
        
        q_words = set(question_lower.split())
        qa_words = set(qa_question_lower.split())
        
        common_words = {"the", "is", "are", "am", "i", "you", "a", "an", "and", "or", "but", "of", "to", "in", "on", "at"}
        q_words = q_words - common_words
        qa_words = qa_words - common_words
        
        if len(q_words) > 0 and len(qa_words) > 0:
            similarity = len(q_words & qa_words) / len(q_words | qa_words)
            if similarity > 0.7:
                return qa["answer"]
    
    return None


def create_system_prompt():
    """Create simple system prompt"""
    base = "You are a helpful AI assistant. Keep responses concise (2-3 sentences)."
    memory = get_memory_context()
    if memory:
        base += f" {memory}"
    return base


def create_new_chat():
    """Create new chat"""
    chat_id = str(uuid.uuid4())[:8]
    st.session_state.chat_history[chat_id] = {
        "title": "✨ New Conversation",
        "messages": [{"role": "system", "content": create_system_prompt()}],
        "created": datetime.now().strftime("%H:%M")
    }
    st.session_state.current_chat_id = chat_id
    return chat_id


def get_current_messages():
    """Get current chat messages"""
    if st.session_state.current_chat_id and st.session_state.current_chat_id in st.session_state.chat_history:
        return st.session_state.chat_history[st.session_state.current_chat_id]["messages"]
    return []


# Enhanced Sidebar
with st.sidebar:
    st.markdown('<h1 class="sidebar-title">🚀Convo BOT</h1>', unsafe_allow_html=True)
    
    if st.button("✨ New Conversation", use_container_width=True, key="new_chat_main"):
        create_new_chat()
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 💬 Recent Chats")
    if st.session_state.chat_history:
        for chat_id, chat_data in list(st.session_state.chat_history.items())[-5:]:
            col1, col2 = st.columns([4, 1])
            with col1:
                title = chat_data["title"][:20] + "..." if len(chat_data["title"]) > 20 else chat_data["title"]
                is_current = st.session_state.current_chat_id == chat_id
                button_key = f"chat_{chat_id}"
                
                if st.button(f"{'🟢 ' if is_current else '💬 '}{title}", key=button_key):
                    if not is_current:
                        st.session_state.current_chat_id = chat_id
                        st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{chat_id}", help="Delete chat"):
                    del st.session_state.chat_history[chat_id]
                    if st.session_state.current_chat_id == chat_id:
                        create_new_chat()
                    st.rerun()
    else:
        st.info("💡 Start your first conversation!")
    
    st.markdown("---")
    
    st.markdown("### 🧠 AI Memory")
    
    if st.session_state.user_memory["name"]:
        st.markdown(f"""
        <div class="memory-card">
            <h4>👤 Profile</h4>
            <p><strong>Name:</strong> {st.session_state.user_memory['name']}</p>
            {f'<p><strong>Title:</strong> {st.session_state.user_memory["title"]}</p>' if st.session_state.user_memory["title"] else ''}
            {f'<p><strong>Location:</strong> {st.session_state.user_memory["location"]}</p>' if st.session_state.user_memory["location"] else ''}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("💡 Tell me your name to personalize our chat!")
    
    if st.session_state.user_memory["qa_pairs"]:
        st.markdown("### ❓ Knowledge Base")
        st.caption("Questions you've asked before:")
        for i, qa in enumerate(st.session_state.user_memory["qa_pairs"][-3:], 1):
            with st.expander(f"💭 {qa['question'][:40]}{'...' if len(qa['question']) > 40 else ''}"):
                st.markdown(f"**Question:** {qa['question']}")
                st.markdown(f"**Answer:** {qa['answer']}")
                st.caption(f"⏰ {datetime.fromisoformat(qa['timestamp']).strftime('%Y-%m-%d %H:%M')}")
    else:
        st.markdown("### ❓ Knowledge Base")
        st.info("💡 Ask questions to build your personal knowledge base!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", help="Refresh memory"):
            st.rerun()
    with col2:
        if st.button("🗑️ Clear All", help="Clear all memory"):
            st.session_state.user_memory = {"name": None, "title": None, "location": None, "facts": [], "qa_pairs": [], "last_updated": None}
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 🔗 System Status")
    try:
        st.markdown('<p class="status-online">🟢 AI Service: Online</p>', unsafe_allow_html=True)
        st.markdown('<p class="status-online">🟢 Memory: Active</p>', unsafe_allow_html=True)
    except:
        st.markdown('<p class="status-offline">🔴 AI Service: Offline</p>', unsafe_allow_html=True)
    
    st.caption("⚡ Enhanced with memory & personalization")


# Main Content Area
if not st.session_state.current_chat_id:
    create_new_chat()


# Welcome message
current_messages = get_current_messages()
if len([m for m in current_messages if m["role"] != "system"]) == 0:
    st.markdown('<h1 class="custom-title">Welcome to ChatGPT Pro</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="memory-card">
            <h3>🧠 Smart Memory</h3>
            <p>I remember your name, preferences, and past conversations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="memory-card">
            <h3>💡 Instant Answers</h3>
            <p>Quick responses with fallback for reliability</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="memory-card">
            <h3>📚 Knowledge Base</h3>
            <p>Your questions become a searchable FAQ</p>
        </div>
        """, unsafe_allow_html=True)


# Display chat messages
for msg in current_messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# Chat Input
prompt = st.chat_input("💬 Ask me anything... I'll remember it!", key="main_chat_input")


if prompt:
    extract_user_info(prompt)
    current_messages[0]["content"] = create_system_prompt()
    current_messages.append({"role": "user", "content": prompt})
    
    user_msgs = [m for m in current_messages if m["role"] == "user"]
    if len(user_msgs) == 1:
        title = prompt[:30] + "..." if len(prompt) > 30 else prompt
        st.session_state.chat_history[st.session_state.current_chat_id]["title"] = title
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        response_text = ""
        
        def get_identity_response():
            name = st.session_state.user_memory['name']
            title = st.session_state.user_memory['title']
            location = st.session_state.user_memory['location']
            
            if name and title and location:
                return f"✨ You are {name}, {title} of {location}. How can I help you today?"
            elif name and title:
                return f"✨ You are {name}, {title}. What would you like to know?"
            elif name:
                return f"✨ Your name is {name}. Nice to meet you! What can I do for you?"
            else:
                return "🤔 I don't know your name yet. Please introduce yourself!"
        
        fallback_responses = {
            "who am i": get_identity_response(),
            "what is my name": get_identity_response(),
            "who i am": get_identity_response(),
            "my name": get_identity_response(),
            "hello": f"👋 Hello {st.session_state.user_memory['name']}! Great to see you again!" if st.session_state.user_memory['name'] else "👋 Hello there! I'm your AI assistant. What's your name?",
            "hi": f"👋 Hi {st.session_state.user_memory['name']}! What can I help you with?" if st.session_state.user_memory['name'] else "👋 Hi there! Nice to meet you!",
            "how are you": "🚀 I'm doing fantastic! Thanks for asking. How are you doing today?",
            "what can you do": "💡 I can chat with you, remember important details about our conversations, answer questions, and help with various tasks. I also build a knowledge base from our interactions!"
        }
        
        prompt_lower = prompt.lower().strip()
        identity_keywords = ["who am i", "what is my name", "who i am", "my name"]
        
        if any(keyword in prompt_lower for keyword in identity_keywords):
            response_text = get_identity_response()
            placeholder.write(response_text)
        else:
            qa_answer = search_qa_memory(prompt)
            if qa_answer:
                response_text = f"💡 I remember this! {qa_answer}"
                placeholder.write(response_text)
            elif prompt_lower in fallback_responses:
                response_text = fallback_responses[prompt_lower]
                placeholder.write(response_text)
            else:
                max_retries = 2
                for attempt in range(max_retries):
                    try:
                        thinking_messages = [
                            "🤔 Thinking...", 
                            "💭 Processing your request...", 
                            "✨ Generating response..."
                        ]
                        
                        retry_messages = [
                            f"🔄 Retrying connection... ({attempt + 1}/{max_retries})",
                            f"⚡ Attempting again... ({attempt + 1}/{max_retries})"
                        ]
                        
                        display_msg = thinking_messages[0] if attempt == 0 else retry_messages[attempt - 1]
                        placeholder.markdown(f'<div class="loading-dots">{display_msg}</div>', unsafe_allow_html=True)
                        
                        response = client.chat.completions.create(
                            model="nvidia/llama-3.3-nemotron-super-49b-v1",
                            messages=current_messages,
                            max_tokens=300,
                            temperature=0.7,
                            stream=True
                        )
                        
                        response_text = ""
                        for chunk in response:
                            try:
                                if chunk.choices[0].delta.content:
                                    response_text += chunk.choices[0].delta.content
                                    placeholder.write(response_text + "▌")
                            except:
                                break
                        
                        if response_text:
                            placeholder.write(response_text)
                            break
                        else:
                            raise Exception("Empty response")
                            
                    except Exception as e:
                        if attempt == max_retries - 1:
                            if st.session_state.user_memory['name']:
                                response_text = f"⚠️ Hi {st.session_state.user_memory['name']}! I'm having trouble connecting to my AI service right now. Please try again in a moment. Your memory and chat history are still intact!"
                            else:
                                response_text = "⚠️ I'm experiencing connectivity issues right now. Please try again in a moment. Don't worry, I'll remember our conversation!"
                            placeholder.write(response_text)
                        else:
                            import time
                            time.sleep(1)
        
        current_messages.append({"role": "assistant", "content": response_text})
        
        if response_text and len(response_text.strip()) > 5:
            qa_pair = {
                "question": prompt,
                "answer": response_text,
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.user_memory["qa_pairs"].append(qa_pair)
            if len(st.session_state.user_memory["qa_pairs"]) > 20:
                st.session_state.user_memory["qa_pairs"] = st.session_state.user_memory["qa_pairs"][-20:]


# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: rgba(255,255,255,0.7); font-size: 0.9rem;">⚡ Powered by NVIDIA AI • Built with ❤️ by Akash Subramani</p>', unsafe_allow_html=True)
