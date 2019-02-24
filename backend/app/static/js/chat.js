var socket = io.connect(window.location.href);
const nickname = document.getElementById('nickname');


const chats_element = document.getElementById('chats');
const chat_input_element = document.getElementById('chat-input');


socket.on('chat', function(data) {
  add_chat(data['from'], data['msg']);
});


chat_input_element.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        socket.emit('chat', {msg: chat_input_element.value},);
        chat_input_element.value = '';
    }
});

function add_chat(from, chat) {
    const chat_element = document.createElement('div');
    chat_element.innerHTML = '<b>' + from + '</b>: ' + chat;
    chats_element.appendChild(chat_element);
}
