#!/usr/bin/env node
/**
 * Generate modern HTML5 versions of all Publisher website pages
 * Based on extracted content from PUBLISHER_CONTENT_EXTRACTION.json
 */

const fs = require('fs');
const path = require('path');

// Read the extracted content
const extractionData = JSON.parse(
  fs.readFileSync('PUBLISHER_CONTENT_EXTRACTION.json', 'utf8')
);

// Page configuration for navigation and descriptions
const pageConfig = {
  "Page815.htm": { title: "Minutes", description: "Board and shareholder meeting minutes" },
  "Page929.htm": { title: "Procedures", description: "Governing procedures and policies" },
  "Page1658.htm": { title: "Reports", description: "Financial and operational reports" },
  "Page1861.htm": { title: "Manuals", description: "Building and operation manuals" },
  "Page1347.htm": { title: "Bylaws", description: "Corporation bylaws and governance" },
  "Page1322.htm": { title: "Pool", description: "Pool facilities and information" },
  "Page592.htm": { title: "Community", description: "Community information and announcements" },
  "Page563.htm": { title: "Events", description: "Community events and activities" },
  "Page449.htm": { title: "News", description: "Latest news and updates" },
  "Page2193.htm": { title: "Contact", description: "Contact information and support" },
  "Page2054.htm": { title: "Links", description: "Useful external links and resources" },
};

const navPages = [
  "Page449.htm", "Page815.htm", "Page929.htm", "Page1658.htm",
  "Page1861.htm", "Page1347.htm", "Page1322.htm", "Page592.htm",
  "Page563.htm", "Page2193.htm", "Page2054.htm"
];

const CSS = `        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }
        
        /* Header */
        header {
            background: linear-gradient(135deg, #d699ad 0%, #903333 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        header h1 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        header p {
            font-size: 1rem;
            opacity: 0.95;
        }
        
        /* Navigation */
        nav {
            background-color: #903333;
            padding: 0;
        }
        
        nav ul {
            list-style: none;
            display: flex;
            flex-wrap: wrap;
        }
        
        nav li {
            margin: 0;
        }
        
        nav a {
            display: block;
            padding: 1rem 1.5rem;
            color: white;
            text-decoration: none;
            transition: background-color 0.3s ease;
            white-space: nowrap;
        }
        
        nav a:hover {
            background-color: #d699ad;
        }
        
        /* Main container */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        main {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            padding: 2rem;
            margin-bottom: 2rem;
        }
        
        main h1 {
            color: #903333;
            margin-bottom: 2rem;
            font-size: 2rem;
        }
        
        /* Content sections */
        .content-section {
            margin: 2rem 0;
        }
        
        .year-section, .section-group {
            margin-bottom: 3rem;
        }
        
        .year-section h2, .section-group h2 {
            color: #d699ad;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
            border-bottom: 2px solid #efd7df;
            padding-bottom: 0.5rem;
        }
        
        .document-list, .content-list {
            list-style: none;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
        }
        
        .document-list li, .content-list li {
            background-color: #f8f9fa;
            border-left: 4px solid #d699ad;
            padding: 1rem;
            border-radius: 4px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .document-list li:hover, .content-list li:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .document-list a, .content-list a {
            color: #903333;
            text-decoration: none;
            font-weight: 500;
            word-break: break-word;
        }
        
        .document-list a:hover, .content-list a:hover {
            color: #d699ad;
            text-decoration: underline;
        }
        
        .intro-text {
            background-color: #efd7df;
            padding: 1.5rem;
            border-radius: 4px;
            margin-bottom: 2rem;
            border-left: 4px solid #903333;
        }
        
        /* Footer */
        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            font-size: 0.9rem;
        }
        
        footer a {
            color: #d699ad;
            text-decoration: none;
        }
        
        footer a:hover {
            text-decoration: underline;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            header h1 {
                font-size: 1.5rem;
            }
            
            nav ul {
                flex-direction: column;
            }
            
            nav li {
                flex: 1;
            }
            
            nav a {
                padding: 0.75rem 1rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .container {
                padding: 1rem;
            }
            
            main {
                padding: 1.5rem;
            }
            
            main h1 {
                font-size: 1.5rem;
            }
            
            .document-list, .content-list {
                grid-template-columns: 1fr;
            }
        }
        
        @media (max-width: 480px) {
            header {
                padding: 1rem;
            }
            
            header h1 {
                font-size: 1.25rem;
            }
            
            header p {
                font-size: 0.9rem;
            }
            
            .container {
                padding: 0.5rem;
            }
            
            main {
                padding: 1rem;
            }
            
            main h1 {
                font-size: 1.25rem;
            }
        }`;

function getNavTitle(page) {
  return (pageConfig[page] || { title: page }).title;
}

function generateNavMenu(currentPage) {
  let nav = '';
  for (const page of navPages) {
    if (page !== currentPage) {
      nav += `            <li><a href="${page}">${getNavTitle(page)}</a></li>\n`;
    }
  }
  return nav;
}

function generateContentHtml(pageData) {
  if (!pageData || !pageData.sample_links) {
    return '<section class="intro-text"><p>Content information coming soon.</p></section>';
  }
  
  let html = '<section class="content-section">\n';
  
  // Group links by year or section
  const grouped = {};
  
  if (Array.isArray(pageData.sample_links)) {
    pageData.sample_links.forEach(link => {
      const text = link.text || link;
      const href = link.href || link;
      const yearMatch = text.match(/20\d{2}/) || href.match(/20\d{2}/);
      const key = yearMatch ? yearMatch[0] : 'Other';
      
      if (!grouped[key]) {
        grouped[key] = [];
      }
      grouped[key].push({ text, href });
    });
  } else if (typeof pageData.sample_links === 'string') {
    return `<section class="intro-text"><p>${pageData.sample_links}</p></section>`;
  }
  
  // Generate HTML for each year/section
  Object.keys(grouped).sort().reverse().forEach(key => {
    html += `  <div class="year-section">\n`;
    html += `    <h2>${key}</h2>\n`;
    html += '    <ul class="document-list">\n';
    
    grouped[key].forEach(item => {
      if (item.href && item.href.trim()) {
        const displayText = item.text.length > 80 ? 
          item.text.substring(0, 77) + '...' : 
          item.text;
        html += `      <li><a href="${item.href}" target="_blank">${displayText}</a></li>\n`;
      }
    });
    
    html += '    </ul>\n  </div>\n';
  });
  
  html += '</section>';
  return html;
}

function generateModernHtml(pageData, filename) {
  const title = pageData.title || 'Page';
  const description = pageData.description || pageConfig[filename]?.description || title;
  const contentHtml = generateContentHtml(pageData);
  const navMenu = generateNavMenu(filename);
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="${description}">
    <title>${title} - Cypress Point Strata</title>
    <style>
${CSS}
    </style>
</head>
<body>
    <header>
        <h1>Cypress Point Strata</h1>
        <p>Community Management &amp; Information</p>
    </header>
    
    <nav>
        <ul>
            <li><a href="../index.htm">Home</a></li>
${navMenu}        </ul>
    </nav>
    
    <div class="container">
        <main>
            <h1>${title}</h1>
${contentHtml}        </main>
    </div>
    
    <footer>
        <p>&copy; 2024 Cypress Point Strata. All rights reserved.</p>
        <p><a href="../index.htm">Back to Home</a></p>
    </footer>
</body>
</html>`;
}

// Generate HTML for all pages
console.log('🚀 Generating modernized HTML5 pages...\n');

let generated = 0;
let failed = 0;

extractionData.forEach(pageData => {
  const filename = pageData.filename;
  const outputFile = filename.replace('.htm', '_modern.html');
  
  try {
    const modernHtml = generateModernHtml(pageData, filename);
    fs.writeFileSync(outputFile, modernHtml, 'utf8');
    
    console.log(`✓ ${filename}`);
    console.log(`  Title: ${pageData.title}`);
    console.log(`  Output: ${outputFile}`);
    if (pageData.sample_links && Array.isArray(pageData.sample_links)) {
      console.log(`  Documents: ${pageData.sample_links.length}\n`);
    } else {
      console.log('');
    }
    generated++;
  } catch (error) {
    console.log(`✗ ${filename} - Error: ${error.message}\n`);
    failed++;
  }
});

console.log(`\n📊 Summary: ${generated} pages generated${failed > 0 ? `, ${failed} failed` : ''}`);
console.log('\n✨ All modern HTML pages are ready for deployment!');
