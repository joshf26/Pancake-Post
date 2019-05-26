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

    document.getElementById(question_id).appendChild(answer_element);
}

function create_question() {
    post_question({
        text: question_textarea.value,
        created_by: firebase.auth().currentUser.uid,
        created_on: firebase.firestore.Timestamp.fromDate(new Date()),
        domain: hostname
    })
}

function create_answer(question_element) {
    post_answer({
        text: question_element.querySelector('textarea').value,
        created_by: firebase.auth().currentUser.uid,
        created_on: firebase.firestore.Timestamp.fromDate(new Date()),
        question: database.collection('questions').doc(question_element.id)
    });
}

document.getElementById('post-question-button').addEventListener('click', create_question);