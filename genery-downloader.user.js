// ==UserScript==
// @name        Genery Downloader
// @namespace   Violentmonkey Scripts
// @match       *://genery.io/*
// @grant       none
// @version     1.0
// @author      dharmik2319
// @description 2/3/2025, 9:28:10 pm
// ==/UserScript==

var originalOpen = XMLHttpRequest.prototype.open;

XMLHttpRequest.prototype.open = function(method, url) {
    if (url.startsWith('https://genery.io/api/search/metadata/')) {
        // Intercepting the response
        this.addEventListener('load', function () {
            let interceptedResult = this.responseText;
            const obj = JSON.parse(interceptedResult);
          const url = obj.scene.urlSet.hls;
          const title = obj.title +" - "+ obj.caption;
          fetch("http://localhost:2319/youtube-dl", {
  method: "POST",
  body: JSON.stringify({
    url: url,
    title: title
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
});

          //alert("yt-dlp \"" + url + "\" -o " + "\""+loc+"\"");

        });
    }
    // Make the original `open` call with the correct arguments
    originalOpen.apply(this, arguments);
};

