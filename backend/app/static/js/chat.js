const messages_element = document.getElementById('messages');

function add_message(from, message) {
    const message_element = document.createElement('div');
    message_element.innerHTML = '<b>' + from + '</b>: ' + message;
    messages_element.appendChild(message_element);
}
