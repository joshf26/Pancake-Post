const config = {
    apiKey: "AIzaSyBOIvx_mOcVdCItZF1kCDXxYOu85REmZgo",
    authDomain: "pancake-post.firebaseapp.com",
    databaseURL: "https://pancake-post.firebaseio.com",
    projectId: "pancake-post",
    storageBucket: "pancake-post.appspot.com",
    messagingSenderId: "713387718919"
};
firebase.initializeApp(config);

const database = firebase.firestore();

let hostname;

get_hostname(() => {
    do_auth(() => {
        setup_listeners();
    });
});

