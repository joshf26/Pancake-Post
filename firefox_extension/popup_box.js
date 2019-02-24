function logTabs(tabs) {
  for (let tab of tabs) {
    // tab.url requires the `tabs` permission
    console.log(tab.url);
  }
}

function onError(error) {
  console.log(`Error: ${error}`);
}

var querying = browser.tabs.query({currentWindow: true, active: true});
querying.then(function(value) {
    console.log(value);
    //let tabUrl = new URL(value)
});

const frame = document.createElement('iframe');
frame.width = '775';
frame.height = '560';

console.log(querying);
frame.src = 'http://pancakepost.com?domain=' + querying.url;
document.body.appendChild(frame);
