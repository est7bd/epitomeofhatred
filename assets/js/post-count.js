/**
 * post-count.js
 * Automatically counts blog posts and syncs the counter on any page that includes it.
 *
 * HOW IT WORKS:
 * - Fetches /blog/index.html (already loaded in memory on the blog page, fetched on others)
 * - Counts elements with class="post-item"
 * - Updates any element with data-post-count attribute OR the specific dc-num counter
 *
 * HOW TO USE ON A NEW POST:
 * 1. Add the HTML file to /blog/
 * 2. Add it to blog/index.html (the post-item entry)
 * 3. Add it to sitemap.xml
 * That's it. This script handles the counter automatically on page load.
 *
 * TO ADD THE COUNTER TO ANY PAGE:
 * Add this to the HTML: <span data-post-count>...</span>
 * The script will replace the content with the live count.
 */

(function() {
  async function getPostCount() {
    try {
      // If we're already on the blog index, count from the DOM
      if (window.location.pathname === '/blog' || window.location.pathname === '/blog/') {
        const items = document.querySelectorAll('.post-item');
        if (items.length > 0) return items.length;
      }
      // Otherwise fetch the blog index and count
      const res = await fetch('/blog/', { cache: 'no-store' });
      if (!res.ok) throw new Error('fetch failed');
      const text = await res.text();
      const matches = text.match(/class="post-item"/g);
      return matches ? matches.length : null;
    } catch(e) {
      return null;
    }
  }

  async function updateCounters() {
    const count = await getPostCount();
    if (!count) return;

    // Update any element with data-post-count attribute
    document.querySelectorAll('[data-post-count]').forEach(el => {
      el.textContent = count.toLocaleString();
    });

    // Update the specific damage-counter dc-num that precedes the "posts" label
    document.querySelectorAll('.dc-label').forEach(label => {
      if (label.textContent.toLowerCase().includes('posts on this site')) {
        const num = label.previousElementSibling;
        if (num && num.classList.contains('dc-num')) {
          num.textContent = count.toLocaleString();
        }
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateCounters);
  } else {
    updateCounters();
  }
})();
