const chatId = JSON.parse(document.getElementById('chat_id').textContent);
const messages = JSON.parse(document.getElementById('messages').textContent)
console.log(messages)

console.log('ws://'
    + window.location.host
    + '/ws/chat/'
    + chatId
    + '/');

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + chatId
    + '/'
);

//chatSocket.onmessage = function(e) {
//    const data = JSON.parse(e.data);
//    const newMessageContent = document.createElement('div');
//    newMessageContent.id = 'sender-message-content';
//    newMessageContent.className = 'chat-message-right pb-4';
//    newMessageContent.textContent = data.message;
//    const messages = document.getElementById('messages');
//    messages.appendChild(newMessageContent);
//};

function createMessageElement(messageData) {
    const messageContainer = document.createElement("div");
    messageContainer.className = "chat-message-right pb-4";

    const avatarDiv = document.createElement("div");

    const avatarImg = document.createElement("img");
    avatarImg.className = "rounded-circle me-1";
    avatarImg.alt = `${messageData.sender.first_name} ${messageData.sender.last_name}`;
    avatarImg.width = 40;
    avatarImg.height = 40;
    avatarImg.src = messageData.sender.avatar || "/static/img/posts/post_default.jpg"; // Дефолтний аватар
    avatarDiv.appendChild(avatarImg);

    const timeDiv = document.createElement("div");
    timeDiv.className = "text-muted small text-nowrap mt-2";
    timeDiv.textContent = messageData.sent_at; // Час у форматі "H:i"
    avatarDiv.appendChild(timeDiv);

    const messageTextContainer = document.createElement("div");
    messageTextContainer.className = "flex-shrink-1 bg-light rounded py-2 px-3 ms-3";

    const senderName = document.createElement("div");
    senderName.className = "font-weight-bold mb-1";
    senderName.textContent = `${messageData.sender} ${messageData.sender.last_name}`;
    messageTextContainer.appendChild(senderName);

    const messageText = document.createElement("div");
    messageText.textContent = messageData.text;
    messageTextContainer.appendChild(messageText);

    messageContainer.appendChild(avatarDiv);
    messageContainer.appendChild(messageTextContainer);

    return messageContainer;
}

function addMessageToChat(messageData) {
    const chatContainer = document.getElementById("messages");
    const messageElement = createMessageElement(messageData);
    chatContainer.appendChild(messageElement);

    // Прокрутка до низу
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data)
    addMessageToChat({
        'text': data.text,
    })
}

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#message-text').focus();
document.querySelector('#message-text').onkeyup = function(e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#message-submit').click();
    }
};

document.querySelector('#message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#message-text');
    const messageText = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'text': messageText,
    }));
    console.log('')
    messageInputDom.value = '';
};