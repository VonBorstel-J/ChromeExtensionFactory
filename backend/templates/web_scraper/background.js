// /backend/templates/web_scraper/background.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'scrape') {
    // Implement scraping logic here
    const data = { title: document.title, url: window.location.href };
    sendResponse({ data });
  }
});
