"""
X-Amplify: The Stijn Method Content Generator
Main Streamlit application.
"""

import streamlit as st
from logic.scraper import smart_input_parser, is_valid_url
from logic.engine import GeminiEngine
from config.prompts import FORMAT_DISPLAY_NAMES

# Page configuration
st.set_page_config(
    page_title="X-Amplify | The Stijn Method",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for premium UI
st.markdown("""
<style>
    /* Dark theme overrides */
    .stApp {
        background: #050505;
    }
    
    /* Card styling */
    .post-card {
        background: #0c0d0f;
        border: 1px solid #1a1a1a;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .post-card:hover {
        border-color: #4fb7a0;
        transform: translateY(-2px);
    }
    
    .post-header {
        font-size: 1.1rem;
        font-weight: 800;
        color: #4fb7a0;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #1a1a1a;
        text-transform: uppercase;
        font-family: 'Outfit', sans-serif;
    }
    
    .post-content {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #ffffff;
        white-space: pre-wrap;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Thesis display */
    .thesis-box {
        background: rgba(79, 183, 160, 0.05);
        border: 1px solid #4fb7a0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .thesis-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #4fb7a0;
        font-weight: 900;
        margin-bottom: 0.5rem;
    }
    
    .thesis-text {
        font-size: 1.25rem;
        font-weight: 600;
        color: #ffffff;
        font-style: italic;
    }
    
    /* Input styling */
    .stTextArea textarea {
        background: #0c0d0f !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #4fb7a0 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: #4fb7a0 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 20px rgba(79, 183, 160, 0.4) !important;
    }
    
    /* Header styling */
    h1 {
        font-weight: 900;
        font-style: italic;
        text-transform: uppercase;
        color: #ffffff;
    }
    
    h1 span {
        color: #4fb7a0;
    }
    
    /* Copy button in card */
    .copy-btn {
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #a78bfa;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .copy-btn:hover {
        background: rgba(99, 102, 241, 0.4);
    }
</style>
""", unsafe_allow_html=True)


def get_char_count_badge(content: str) -> str:
    """Return a styled badge showing character count vs X limit."""
    char_count = len(content)
    if char_count <= 280:
        color = "#22c55e"  # green
        status = "✓"
    elif char_count <= 350:
        color = "#eab308"  # yellow  
        status = "⚠"
    else:
        color = "#ef4444"  # red
        status = "✗"
    
    return f'<span style="font-size: 0.75rem; color: {color}; float: right;">{status} {char_count}/280</span>'


def render_post_card(format_key: str, content: str, col_index: int):
    """Render a single post card with copy functionality."""
    display_name = FORMAT_DISPLAY_NAMES.get(format_key, format_key)
    char_badge = get_char_count_badge(content)
    
    # Create unique key for this card's copy button
    copy_key = f"copy_{format_key}_{col_index}"
    
    # Escape content for HTML display
    import html
    escaped_content = html.escape(content)
    
    st.markdown(f"""
    <div class="post-card">
        <div class="post-header">{display_name} {char_badge}</div>
        <div class="post-content">{escaped_content}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Copy button using Streamlit's native approach
    if st.button("📋 Copy", key=copy_key, use_container_width=True):
        st.session_state[f"copied_{format_key}"] = True
        # JavaScript injection for clipboard - properly escape the content
        escaped_js = content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
        st.components.v1.html(f"""
        <script>
            navigator.clipboard.writeText(`{escaped_js}`);
        </script>
        """, height=0)
        st.success("Copied!", icon="✅")


def main():
    """Main application logic."""
    
    # Navigation
    st.markdown("""
    <div style="display: flex; gap: 15px; margin-bottom: 20px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
        <a href="https://brain.tonyreviewsthings.com" style="color: #70757a; text-decoration: none; font-size: 10px; font-weight: 900; letter-spacing: 2px;">🧠 BRAIN</a>
        <a href="https://post.tonyreviewsthings.com" style="color: #70757a; text-decoration: none; font-size: 10px; font-weight: 900; letter-spacing: 2px;">📊 ANALYTICS</a>
        <a href="https://amplify.tonyreviewsthings.com" style="color: #4fb7a0; text-decoration: none; font-size: 10px; font-weight: 900; letter-spacing: 2px;">⚡ AMPLIFY</a>
        <a href="https://status.tonyreviewsthings.com" style="color: #70757a; text-decoration: none; font-size: 10px; font-weight: 900; letter-spacing: 2px;">🛡️ STATUS</a>
    </div>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("# ⚡ X-Amplify")
    st.markdown("*Transform any idea into 10 viral X posts using The Stijn Method*")
    
    # Debug Toggle in Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        debug_mode = st.toggle("Debug Mode", value=False, help="Show technical logs and raw data.")
        if st.button("🗑️ Clear Cache"):
            st.session_state.clear()
            st.rerun()

    st.divider()
    
    # Smart Input Section
    st.markdown("### 💡 Your Raw Idea")
    st.caption("Paste a URL to extract content, or type your idea directly.")
    
    user_input = st.text_area(
        label="Input",
        placeholder="Paste a URL (https://...) or describe your idea, product, or insight...",
        height=120,
        label_visibility="collapsed",
    )
    
    # Input type indicator
    if user_input:
        if is_valid_url(user_input):
            st.info("🔗 URL detected. Will scrape and analyze content.", icon="🌐")
        else:
            st.info("📝 Text input detected. Will analyze directly.", icon="✍️")
    
    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_clicked = st.button(
            "⚡ Generate 10 Posts",
            use_container_width=True,
            disabled=not user_input,
        )
    
    # Generation logic
    if generate_clicked and user_input:
        # Clear previous results and errors
        st.session_state.pop("posts", None)
        st.session_state.pop("thesis", None)
        st.session_state.pop("error", None)
        st.session_state.pop("debug_logs", None)
        st.session_state["debug_logs"] = []
        
        def log_debug(msg):
            if "debug_logs" not in st.session_state:
                st.session_state["debug_logs"] = []
            st.session_state["debug_logs"].append(msg)
            print(f"DEBUG: {msg}")

        log_debug(f"Starting generation for input: {user_input[:50]}...")
        
        # Parse input
        try:
            with st.spinner("🔮 Analyzing your input..."):
                input_type, content = smart_input_parser(user_input)
                log_debug(f"Input parsed as {input_type}. Content length: {len(content)}")
        except Exception as e:
            st.error(f"❌ Failed to parse input: {str(e)}")
            log_debug(f"ERROR: Scraper failed: {str(e)}")
            st.stop()
        
        # Generate posts
        try:
            with st.spinner("⚡ Generating 10 posts... (this takes 10-20 seconds)"):
                engine = GeminiEngine()
                log_debug(f"Using model: {engine.model}")
                
                thesis, posts = engine.generate_content(user_input, input_type, content)
                
                # Store in session state
                st.session_state["thesis"] = thesis
                st.session_state["posts"] = posts
                log_debug("Generation successful. 10 posts received.")
                
        except ValueError as e:
            st.error(f"❌ 🔑 Configuration Error: {str(e)}")
            log_debug(f"ERROR: Configuration: {str(e)}")
            st.info("💡 **Tip:** Make sure GEMINI_API_KEY is set in your Streamlit secrets.")
            st.stop()
        except Exception as e:
            st.error(f"❌ Generation failed: {str(e)}")
            log_debug(f"ERROR: Engine failed: {str(e)}")
            # Show more details if in debug mode
            if debug_mode:
                st.exception(e)
            st.stop()
    
    # Debug Console
    if debug_mode:
        with st.expander("🛠️ Debug Console", expanded=True):
            st.markdown("#### Execution Logs")
            if "debug_logs" in st.session_state and st.session_state["debug_logs"]:
                for log in st.session_state["debug_logs"]:
                    st.code(log)
            else:
                st.write("No logs yet. Try generating posts.")
            
            if "posts" in st.session_state:
                st.markdown("#### Raw Output Data")
                st.json(st.session_state["posts"])

    # Show any stored errors (from previous runs)
    if "error" in st.session_state:
        st.error(f"❌ {st.session_state['error']}")
    
    # Display posts grid (also show thesis here if we have results but didn't just generate)
    if "posts" in st.session_state and st.session_state["posts"]:
        # Show thesis if we have it (persisted from previous generation)
        if "thesis" in st.session_state:
            st.markdown(f"""
            <div class="thesis-box">
                <div class="thesis-label">The Core Thesis</div>
                <div class="thesis-text">"{st.session_state['thesis']}"</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### 📱 Your 10 Posts")
        st.caption("Click copy to grab any post for X. Green = under 280 chars, Yellow = close, Red = over limit.")
        
        posts = st.session_state["posts"]
        
        # Create 2-column grid for 10 cards
        format_keys = list(FORMAT_DISPLAY_NAMES.keys())
        
        for i in range(0, 10, 2):
            col1, col2 = st.columns(2)
            
            with col1:
                if i < len(format_keys):
                    key = format_keys[i]
                    if key in posts:
                        render_post_card(key, posts[key], i)
            
            with col2:
                if i + 1 < len(format_keys):
                    key = format_keys[i + 1]
                    if key in posts:
                        render_post_card(key, posts[key], i + 1)
        
        # Export all button
        st.divider()
        if st.button("📥 Export All as JSON", use_container_width=True):
            import json
            json_str = json.dumps(posts, indent=2, ensure_ascii=False)
            st.download_button(
                label="💾 Download JSON",
                data=json_str,
                file_name="x_amplify_posts.json",
                mime="application/json",
            )


if __name__ == "__main__":
    main()
