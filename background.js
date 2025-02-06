
chrome.runtime.onInstalled.addListener(() => {
    console.log("Phishing Email Detector: Service Worker Installed");
  });
  
  // Listen for messages from the content script (e.g., when checking for phishing emails)
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Background received message:", message);
  
    if (message.action === "checkPhishing") {
      console.log("Checking phishing for subject:", message.emailSubject);
      sendResponse({ result: "safe" });  // Dummy response for now
    }
  });