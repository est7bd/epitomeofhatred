#!/usr/bin/env node
/**
 * build-index.js — epitomeofhatred.com
 */

const fs   = require('fs');
const path = require('path');

const BLOG_DIR  = path.join(__dirname, 'blog');
const ROOT_HTML = path.join(__dirname, 'index.html');
const BLOG_HTML = path.join(BLOG_DIR, 'index.html');

// ── 1. Read all blog post files ──────────────────────────────────────────────
const files = fs.readdirSync(BLOG_DIR)
  .filter(f => f.endsWith('.html') && f !== 'index.html');

console.log(`Found ${files.length} blog post files`);

// ── 2. Extract metadata from each file ──────────────────────────────────────
function extractMeta(filename) {
  const slug    = filename.replace('.html', '');
  const content = fs.readFileSync(path.join(BLOG_DIR, filename), 'utf8');

  const get = (pattern) => {
    const m = content.match(pattern);
    return m ? m[1].trim() : '';
  };

  const rawTitle = get(/<title>([^<]+)<\/title>/);
  const title    = rawTitle.replace(/\s*[—–-]+\s*Epitome of Hatred\s*$/i, '').trim();
  const desc     = get(/name="description"[^>]*content="([^"]+)"/) || get(/content="([^"]+)"[^>]*name="description"/);
  const ogDesc   = get(/property="og:description"[^>]*content="([^"]+)"/) || get(/content="([^"]+)"[^>]*property="og:description"/);
  const dateSpan = get(/<span class="post-date">([^<]+)<\/span>/);
  const dataDate = get(/data-date="([^"]+)"/);
  const tagMatches = [...content.matchAll(/<span class="post-tag">([^<]+)<\/span>/g)];
  const tags     = tagMatches.map(m => m[1].trim());
  const topics   = get(/data-topics="([^"]+)"/);
  const search   = get(/data-search="([^"]+)"/);
  const deck     = get(/<p class="deck">([^<]+(?:<[^<]+>[^<]*<\/[^<]+>[^<]*)*)<\/p>/).replace(/<[^>]+>/g, '').trim() || ogDesc || desc;

  let sortDate = dataDate || '';
  if (!sortDate && dateSpan) {
    const parsed = new Date(dateSpan);
    if (!isNaN(parsed)) sortDate = parsed.toISOString().split('T')[0];
    else {
      const yearMatch = dateSpan.match(/(\d{4})/);
      if (yearMatch) sortDate = yearMatch[1] + '-01-01';
    }
  }

  return { slug, title, desc, deck: deck || desc, tags, topics, search, dateSpan, sortDate };
}

const posts = files.map(extractMeta)
  .filter(p => p.title) 
  .sort((a, b) => {
    if (a.sortDate > b.sortDate) return -1;
    if (a.sortDate < b.sortDate) return  1;
    return a.slug.localeCompare(b.slug);
  });

console.log(`Parsed ${posts.length} posts`);

// ── 3. Generate post-item HTML entries ───────────────────────────────────────
function postItemHTML(p) {
  const tagsHTML = p.tags.map(t => `<span class="post-item-tag">${t}</span>`).join('');
  const dateDisplay = p.dateSpan || p.sortDate || '';
  const topics = p.topics || p.tags.map(t => t.toLowerCase().replace(/\s+/g,'-')).join(' ');
  const search = p.search || `${p.title} ${p.desc}`.toLowerCase();
  const deck   = (p.deck || p.desc || '').replace(/"/g, '&quot;');

  return `      <a href="/blog/${p.slug}" class="post-item" data-date="${p.sortDate}" data-topics="${topics}" data-search="${search.toLowerCase()}">
        <span class="post-item-date">${dateDisplay}</span>
        <div class="post-item-content">
          <div class="post-item-tags">${tagsHTML}</div>
          <div class="post-item-title">${p.title}</div>
          <div class="post-item-deck">${deck}</div>
        </div>
      </a>`;
}

const allPostItems = posts.map(postItemHTML).join('\n\n');

// ── 4. Update blog/index.html ────────────────────────────────────────────────
let blogIndex = fs.readFileSync(BLOG_HTML, 'utf8');
const listStart = blogIndex.indexOf('<div class="post-list" id="post-list">');
const listEnd   = blogIndex.indexOf('</div>', listStart) + 6;

if (listStart !== -1) {
  blogIndex = blogIndex.slice(0, listStart) +
    `<div class="post-list" id="post-list">\n\n${allPostItems}\n\n    </div>` +
    blogIndex.slice(listEnd);

  blogIndex = blogIndex.replace(
    /placeholder="Search \d+ posts\.\.\."/,
    `placeholder="Search ${posts.length} posts..."`
  );
  fs.writeFileSync(BLOG_HTML, blogIndex);
  console.log(`✅ blog/index.html updated — ${posts.length} posts`);
}

// ── 5. Update root/index.html (The Critical Fix) ────────────────────────────
let rootHTML = fs.readFileSync(ROOT_HTML, 'utf8');

// 5a. Fix the "Damage Counter" strip (Big red number)
// Looks for the dc-num span followed by "Sourced, documented posts"
rootHTML = rootHTML.replace(
  /(<span class="dc-num">)[\s\S]*?(<\/span>\s*\n\s*<span class="dc-label">Sourced, documented posts)/,
  `$1${posts.length}$2`
);

// 5b. Fix the "View All" link at the bottom
// Replaces the entire span content to prevent nesting
rootHTML = rootHTML.replace(
  /(all <span data-post-count>)[\s\S]*?(<\/span> posts →)/g,
  `$1${posts.length}$2`
);

fs.writeFileSync(ROOT_HTML, rootHTML);
console.log(`✅ root/index.html updated — counter set to ${posts.length}`);

// ── 6. Update sitemap.xml ─────────────────────────────────────────────────────
const SITEMAP = path.join(__dirname, 'sitemap.xml');
if (fs.existsSync(SITEMAP)) {
  let sitemap = fs.readFileSync(SITEMAP, 'utf8');
  const existingSlugs = new Set([...sitemap.matchAll(/epitomeofhatred\.com\/blog\/([^<]+)/g)].map(m => m[1]));
  const newEntries = posts
    .filter(p => !existingSlugs.has(p.slug))
    .map(p => `  <url>
    <loc>https://epitomeofhatred.com/blog/${p.slug}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>`).join('\n');

  if (newEntries) {
    sitemap = sitemap.replace('</urlset>', newEntries + '\n\n</urlset>');
    fs.writeFileSync(SITEMAP, sitemap);
    console.log(`✅ sitemap.xml updated`);
  }
}

console.log(`\n🎉 Done! ${posts.length} posts indexed.`);
