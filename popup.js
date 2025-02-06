document.addEventListener("DOMContentLoaded", function () {
    chrome.storage.local.get(["phishingEmails"], function (data) {
        let statusElement = document.getElementById("status");
        if (data.phishingEmails && data.phishingEmails.length > 0) {
            statusElement.innerText = "⚠ Phishing Emails Detected!";
        } else {
            statusElement.innerText = "✅ No Phishing Emails Found";
        }
    });
});
