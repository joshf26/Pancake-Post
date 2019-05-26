const database = firebase.firestore();

// database.collection('domains').doc('pancakepost.com').collection('questions').onSnapshot(function(doc) {
//     console.log(doc.docs[0].data());
// });

// domain.hostname
database.collection('domains').doc('pancakepost.com').collection('questions').onSnapshot(document => {
    document.forEach(question => {
        console.log(question.data());
        add_question(question.data());
    });
});