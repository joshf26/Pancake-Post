let messages_element = document.getElementById('messages');

function add_message(message) {
    let message_element = document.createElement('p');
    message_element.innerText = message;
    messages_element.appendChild(message_element);
}
