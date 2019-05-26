const config = {
    apiKey: "AIzaSyBOIvx_mOcVdCItZF1kCDXxYOu85REmZgo",
    authDomain: "pancake-post.firebaseapp.com",
    databaseURL: "https://pancake-post.firebaseio.com",
    projectId: "pancake-post",
    storageBucket: "pancake-post.appspot.com",
    messagingSenderId: "713387718919"
};
firebase.initializeApp(config);

let domain;

chrome.tabs.query({
    active: true,
    currentWindow: true
}, tabs => {
    domain = new URL(tabs[0].url);
});
