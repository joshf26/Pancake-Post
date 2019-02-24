function logTabs(tabs) {
	alert("HI I AM HERE")
	let tab = tabs[0]; // Safe to assume there will only be one result
	// alert(tab.url);
	document.getElementById('test').innerHTML = tab.url;
}

function onError(err){
	console.error(err);
	alert(err);
}

browser.tabs.query({currentWindow: true, active: true}).then(logTabs, onError);