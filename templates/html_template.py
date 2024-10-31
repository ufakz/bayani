css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
}

.chat-message.user {
    background-color: #2b313e;
}

.chat-message.bot {
    background-color: #475063;
}

.chat-message .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 1rem;
    flex-shrink: 0;
}

.chat-message .content {
    flex-grow: 1;
    overflow-x: auto;
}

.source-info {
    font-size: 0.8rem;
    color: #a8a8a8;
    margin-top: 0.5rem;
}

.usage-stats {
    font-size: 0.8rem;
    color: #a8a8a8;
    margin-top: 1rem;
    padding: 0.5rem;
    background-color: #2b313e;
    border-radius: 0.3rem;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png">
    </div>
    <div class="content">
        {{MSG}}
    </div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
    </div>
    <div class="content">
        {{MSG}}
    </div>
</div>
'''