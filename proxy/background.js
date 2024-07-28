chrome.webRequest.onBeforeSendHeaders.addListener(
    function(details) {
      var randomIP = [
        Math.floor(Math.random() * 256),
        Math.floor(Math.random() * 256),
        Math.floor(Math.random() * 256),
        Math.floor(Math.random() * 256)
      ].join('.');
      var headers = details.requestHeaders;
  
      headers.push({name: "X-Forwarded-For", value: randomIP});
  
      return {requestHeaders: headers};
    },
    {urls: ["<all_urls>"]},
    ["blocking", "requestHeaders"]
  );
  