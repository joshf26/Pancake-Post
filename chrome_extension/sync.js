function post_question(question) {
    database.collection('questions').add(question);
}

function post_answer(answer) {
    database.collection('answers').add(answer);
}

function delete_question(question) {
    // TODO: This should be a cloud function, since users could decide not to delete the answers.
    database.collection('answers').where('question', '==', database.collection('questions').doc(question)).get().then(collection => {
        collection.forEach(document => {
            document.ref.delete();
        });
    });

    database.collection('questions').doc(question).delete();
}

function delete_answer(answer) {
    database.collection('answers').doc(answer).delete();
}

function setup_listeners() {
    database.collection('questions').where('domain', '==', hostname).onSnapshot(document => {
        document.docChanges().forEach(change => {
            const question = change.doc;

            if (change.type === 'added') {
                add_question(question.id, question.data());

                database.collection('answers').where('question', '==', database.collection('questions').doc(question.id)).onSnapshot(document => {
                    document.docChanges().forEach(change => {
                        const answer = change.doc;

                        if (change.type === 'added') {
                            add_answer(question.id, answer.id, answer.data());
                        } else if (change.type === 'modified') {
                            // TODO
                        } else {
                            remove_answer(answer.id);
                        }
                    });
                })
            } else if (change.type === 'modified') {
                // TODO
            } else {
                remove_question(question.id);
            }
        });
    });
}
