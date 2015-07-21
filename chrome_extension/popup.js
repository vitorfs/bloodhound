function getCurrentTabUrl(callback) {
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    var tab = tabs[0];
    var url = tab.url;
    console.assert(typeof url == 'string', 'tab.url should be a string');
    callback(url);
  });
}

function getProduct(url, callback, errorCallback) {
  if (url.indexOf('verkkokauppa.com/') != -1 && url.indexOf('/product/') != -1) {
    var productCode = url.split('product/')[1].split('/')[0];
    var searchUrl = 'https://bloodhound.me/api/product/' +
      '?code=' + encodeURIComponent(productCode);

    var x = new XMLHttpRequest();
    x.open('GET', searchUrl);

    x.onload = function() {
      var response = x.response;
      callback(response);
    };

    x.onerror = function() {
      errorCallback('Network error.');
    };

    x.send();
  }
  else {
    errorCallback('No product found in this page.');
    return;
  }
}

function renderStatus(statusText) {
  document.getElementById('main').textContent = statusText;
}

document.addEventListener('DOMContentLoaded', function() {
  getCurrentTabUrl(function(url) {

    renderStatus('Loading ' + url);

    getProduct(url, function(priceHistory) {
      var main = document.getElementById('main');
      main.innerHTML = priceHistory;
    }, function(errorMessage) {
      renderStatus('Cannot display image. ' + errorMessage);
    });
  });
});
