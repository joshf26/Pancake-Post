var socket = io.connect(window.location.href);
const nickname = document.getElementById('nickname');


const messages_element = document.getElementById('messages');
const message_input_element = document.getElementById('message-input');


socket.on('message', function(data) {
  add_message(data['from'], data['msg']);
});


message_input_element.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        socket.emit('message', {msg: message_input_element.value});
        message_input_element.value = '';
    }
});

function add_message(from, message) {
    const message_element = document.createElement('div');
    message_element.innerHTML = '<b>' + from + '</b>: ' + message;
    messages_element.appendChild(message_element);
}
