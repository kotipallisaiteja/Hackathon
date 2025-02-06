// Wait for Gmail to load
setTimeout(() => {
    analyzeEmails();
}, 5000);

function analyzeEmails() {
    let emailBodies = document.querySelectorAll('.a3s');  // Class for Gmail email bodies
    emailBodies.forEach(email => {
        let emailText = email.innerText || email.textContent;
        let flagged = detectPhishing(emailText);

        if (flagged) {
            chrome.runtime.sendMessage({
                action: "phishing_detected"
            });
        }

        // Check links in emails for suspicious domains
        let links = email.querySelectorAll("a");
        if (checkSuspiciousLinks(links)) {
            chrome.runtime.sendMessage({
                action: "phishing_detected"
            });
        }
    });
}

// Basic phishing detection based on keywords
function detectPhishing(emailText) {
    let phishingKeywords = [
        "urgent action required",
        "verify your account",
        "click the link below",
        "update your payment info",
        "you won a prize",
        "suspicious activity detected"
    ];

    for (let keyword of phishingKeywords) {
        if (emailText.toLowerCase().includes(keyword)) {
            return true;
        }
    }
    return false;
}

// Check if the links in the email belong to suspicious domains
function checkSuspiciousLinks(links) {
    let suspiciousDomains = ["bit.ly", "tinyurl.com", "phishy.com"];
    for (let link of links) {
        let url = new URL(link.href);
        if (suspiciousDomains.includes(url.hostname)) {
            return true;
        }
    }
    return false;
}
// Log when the content script runs
console.log("Phishing Email Detector: content.js script is running");

// Wait for Gmail to load and check for emails
window.addEventListener('load', function () {
  console.log("Gmail is fully loaded");
  // Select email items (Gmail's email list items might have the class 'zA')
  const emails = document.querySelectorAll('.zA');
  console.log("Emails detected:", emails.length);

  emails.forEach(email => {
    // Get the subject of each email
    const subject = email.querySelector('.bog') ? email.querySelector('.bog').innerText : 'No subject';
    console.log("Email subject:", subject);
  });
});


// Add a MutationObserver to detect new emails as Gmail loads more emails dynamically
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList') {
        const emails = document.querySelectorAll('.zA');  // Gmail email list item selector
        console.log("New Emails Detected:", emails.length);
  
        emails.forEach(email => {
          const subject = email.querySelector('.bog') ? email.querySelector('.bog').innerText : 'No subject';
          console.log("New email subject:", subject);
        });
      }
    });
  });
  
  // Start observing changes in the body of Gmail's page
  observer.observe(document.body, { childList: true, subtree: true });