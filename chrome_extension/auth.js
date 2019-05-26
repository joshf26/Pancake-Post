var config = {
    apiKey: "AIzaSyBOIvx_mOcVdCItZF1kCDXxYOu85REmZgo",
    authDomain: "pancake-post.firebaseapp.com",
    databaseURL: "https://pancake-post.firebaseio.com",
    projectId: "pancake-post",
    storageBucket: "pancake-post.appspot.com",
    messagingSenderId: "713387718919"
};
firebase.initializeApp(config);

function startAuth(interactive) {
    // Request an OAuth token from the Chrome Identity API.
    chrome.identity.getAuthToken({interactive: !!interactive}, function (token) {
        if (chrome.runtime.lastError && !interactive) {
            console.log('It was not possible to get a token programmatically.');
        } else if (chrome.runtime.lastError) {
            console.error(chrome.runtime.lastError);
        } else if (token) {
            // Authorize Firebase with the OAuth Access Token.
            var credential = firebase.auth.GoogleAuthProvider.credential(null, token);
            firebase.auth().signInAndRetrieveDataWithCredential(credential).catch(function (error) {
                // The OAuth token might have been invalidated. Lets' remove it from cache.
                if (error.code === 'auth/invalid-credential') {
                    chrome.identity.removeCachedAuthToken({token: token}, function () {
                        startAuth(interactive);
                    });
                }
            });
        } else {
            console.error('The OAuth Token was null');
        }
    });
}

function signOut() {
    // TODO: Make sure to allow the user to change accounts.
    firebase.auth().signOut();
}

window.onload = () => {
    firebase.auth().onAuthStateChanged((user) => {
        if (user) {
            add_message(firebase.auth().currentUser.displayName);
        }
        else {
            startAuth(true);
        }
    });

    if (!firebase.auth().currentUser) {
        startAuth(true);
    }

    document.getElementById('sign-out-button').addEventListener('click', signOut);
};