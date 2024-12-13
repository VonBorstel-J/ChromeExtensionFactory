// /backend/templates/web_scraper/popup.js
document.getElementById('scrape-btn').addEventListener('click', () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { action: 'scrape' }, (response) => {
      console.log('Scraped Data:', response.data);
    });
  });
});
