function post_question(question) {
    database.collection('questions').add(question);
}

function post_answer(answer) {
    database.collection('answers').add(answer);
}

function delete_question(question) {
    database.collection('questions').doc(question).delete();
}

function setup_listeners() {
    database.collection('questions').where('domain', '==', hostname).onSnapshot(document => {
        document.forEach(question => {
            add_question(question.id, question.data());

            database.collection('answers').where('question', '==', database.collection('questions').doc(question.id)).onSnapshot(document => {
                document.forEach(answer => {
                    add_answer(question.id, answer.id, answer.data());
                });
            })
        });
    });
}
