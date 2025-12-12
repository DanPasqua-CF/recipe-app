// Get current visitor count from localStorage
function getVisitorCount() {
  const count = localStorage.getItem('visitorCount');
  return count ? parseInt(count) : 0;
}

// Increment and save visitor count
function incrementVisitorCount() {
  let count = getVisitorCount();
  count++;
  localStorage.setItem('visitorCount', count);
  return count;
}

// Update the counter
function updateCounterDisplay() {
  const counterElement = document.getElementById('visitor-count');
  if (counterElement) {
    const count = getVisitorCount();
    counterElement.textContent = count.toLocaleString();
  }
}

// Check for new visitors
function checkNewVisit() {
  const hasVisited = sessionStorage.getItem('hasVisitedThisSession');
  
  if (!hasVisited) {
    incrementVisitorCount();
    sessionStorage.setItem('hasVisitedThisSession', 'true');
  }
  
  updateCounterDisplay();
}

// Initialize counter when page loads
document.addEventListener('DOMContentLoaded', function() {
  checkNewVisit();
});
