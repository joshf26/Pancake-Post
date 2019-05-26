const messages_container = document.getElementById('messages');
const questions_container = document.getElementById('questions');

function add_message(message) {
    const message_element = document.createElement('p');
    message_element.innerText = message;
    messages_container.appendChild(message_element);
}

function add_question(question) {
    const question_element = document.createElement('div');
    question_element.className = 'question';

    const question_text_element = document.createElement('h6');
    question_element.innerText = question['text'];

    const question_info_element = document.createElement('p');
    question_info_element.innerText = format_date(question['createdon'].toDate());

    question_element.appendChild(question_info_element);
    question_element.appendChild(question_text_element);

    questions_container.appendChild(question_element);
}