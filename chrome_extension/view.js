const messages_container = document.getElementById('messages');
const questions_container = document.getElementById('questions');
const question_textarea = document.getElementById('question-textarea');

function get_hostname(callback) {
    chrome.tabs.query({
        active: true,
        currentWindow: true
    }, tabs => {
        hostname = new URL(tabs[0].url).hostname;

        // TEMP
        hostname = 'pancakepost.com';

        callback();
    });
}

function format_date(date) {
    const day = date.getDate();
    const month = date.getMonth();
    const year = date.getFullYear();
    const hour = date.getHours();
    const minute = date.getMinutes();

    return `${month}/${day}/${year} ${hour}:${minute}`;
}

function add_message(message) {
    const message_element = document.createElement('p');
    message_element.innerText = message;
    messages_container.appendChild(message_element);
}

function add_question(id, question) {
    const question_element = document.createElement('div');
    question_element.className = 'question';
    question_element.id = id;

    const question_text_element = document.createElement('h6');
    question_element.innerText = question['text'];

    const question_info_element = document.createElement('p');
    question_info_element.innerText = format_date(question['created_on'].toDate());

    const question_answer_element = document.createElement('textarea');
    const question_answer_button = document.createElement('button');

    question_answer_button.innerText = 'Answer';
    question_answer_button.addEventListener('click', () => {
        create_answer(question_element);
    });

    if (question.created_by === firebase.auth().currentUser.uid) {
        const delete_button = document.createElement('button');
        delete_button.innerText = 'Delete';
        delete_button.addEventListener('click', () => {
            delete_question(id);
        });
        question_element.appendChild(delete_button);
    }

    question_element.appendChild(question_info_element);
    question_element.appendChild(question_text_element);
    question_element.appendChild(question_answer_element);
    question_element.appendChild(question_answer_button);

    questions_container.appendChild(question_element);
}

function add_answer(question_id, id, answer) {
    const answer_element = document.createElement('p');
    answer_element.innerText = answer.text;
    answer_element.id = id;

    if (answer.created_by === firebase.auth().currentUser.uid) {
        const delete_button = document.createElement('button');
        delete_button.innerText = 'Delete';
        delete_button.addEventListener('click', () => {
            delete_answer(id);
        });
        answer_element.appendChild(delete_button);
    }

    document.getElementById(question_id).appendChild(answer_element);
}

function remove_question(id) {
    const question_element = document.getElementById(id);
    question_element.parentElement.removeChild(question_element);
}

function remove_answer(id) {
    const answer_element = document.getElementById(id);

    // The answer element could be null if the question containing the answer was deleted.
    if (answer_element)
        answer_element.parentElement.removeChild(answer_element);
}

function create_question() {
    post_question({
        text: question_textarea.value,
        created_by: firebase.auth().currentUser.uid,
        created_on: firebase.firestore.Timestamp.fromDate(new Date()),
        domain: hostname
    });

    question_textarea.value = '';
}

function create_answer(question_element) {
    const answer_textarea = question_element.querySelector('textarea');

    post_answer({
        text: answer_textarea.value,
        created_by: firebase.auth().currentUser.uid,
        created_on: firebase.firestore.Timestamp.fromDate(new Date()),
        question: database.collection('questions').doc(question_element.id)
    });

    answer_textarea.value = '';
}

document.getElementById('post-question-button').addEventListener('click', create_question);