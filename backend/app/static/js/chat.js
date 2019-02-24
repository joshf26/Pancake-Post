// var io = require('socket.io')(80);

var socket = io.connect('http://localhost');
const nickname = document.getElementById('nickname');
console.log(nickname);
socket.on('connect', () => {
	console.log("connected");
});

socket.on('message', function(data) {
  add_message(nickname, message_input_element.value);
});

const messages_element = document.getElementById('messages');

const message_input_element = document.getElementById('message-input');
message_input_element.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        // TODO: Replace the following line with a call to the server to send the message to everyone.
        
        socket.emit('message', {msg: message_input_element.value});
        message_input_element.value = '';
    }
});

function add_message(from, message) {
    const message_element = document.createElement('div');
    message_element.innerHTML = '<b>' + from + '</b>: ' + message;
    messages_element.appendChild(message_element);
}
