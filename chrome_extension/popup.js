chrome.tabs.query({
    active: true,
    currentWindow: true
}, function(tabs) {
    let tabURL = new URL(tabs[0].url);

    const frame = document.createElement('iframe');
    frame.width = '800';
    frame.height = '600';

    frame.src = 'http://localhost?domain=' + tabURL.host;
    document.body.appendChild(frame);
});
