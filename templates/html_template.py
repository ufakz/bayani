css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}

/* Add styles for chat container */
[data-testid="stVerticalBlock"] {
    max-height: 70vh;
    overflow-y: auto;
    padding-bottom: 100px;
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;     /* Firefox */
}

/* Hide Webkit scrollbar (Chrome, Safari, newer Edge) */
[data-testid="stVerticalBlock"]::-webkit-scrollbar {
    display: none;
}

/* Updated input container styles */
[data-testid="stTextInput"] {
    position: fixed;
    bottom: 3rem;
    padding: 1rem;
    z-index: 100;
    right: 2rem;
}

/* Target Streamlit's main content area */
.main {
    padding-bottom: 100px;
}

/* Adjust input position based on sidebar state */
.sidebar-collapsed [data-testid="stTextInput"] {
    left: 3rem;
}

[data-testid="stSidebar"][aria-expanded="true"] ~ [data-testid="stTextInput"] {
    left: calc(1rem);  /* sidebar width (24rem) + padding */
}

[data-testid="stSidebar"][aria-expanded="false"] ~ [data-testid="stTextInput"] {
    left: calc(1rem);  /* collapsed width + padding */
}

/* Make sure input background extends full width */
.stTextInput > div {
    width: 100%;
    padding: 0.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://www.iconarchive.com/download/i143626/iconarchive/robot-avatar/Blue-2-Robot-Avatar.256.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="message">{{MSG}}</div>
    <div class="avatar">
        <img src="https://cdn.pixabay.com/photo/2020/07/01/12/58/icon-5359553_1280.png">
    </div>    
</div>
'''