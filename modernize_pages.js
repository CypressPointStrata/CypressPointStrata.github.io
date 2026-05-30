#!/usr/bin/env node
/**
 * Generate modern HTML5 versions of Publisher website pages
 * for CypressPointStrata.github.io
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// Page configuration
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

function getNavTitle(page) {
  return (pageConfig[page] || { title: page }).title;
}

function extractPageContent(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  
  // Extract title
  const titleMatch = content.match(/<title>([^<]+)<\/title>/i);
  const title = titleMatch ? titleMatch[1] : "Page";
  
  // Extract links using regex
  const linkRegex = /<a[^>]*href="([^"]*)"[^>]*>([^<]*)<\/a>/gi;
  const links = [];
  let match;
  
  while ((match = linkRegex.exec(content)) !== null) {
    const href = match[1].trim();
    const text = match[2].trim().replace(/\s+/g, ' ');
    // Skip empty links and navigation links
    if (text && !text.includes('lang=') && text.length > 2) {
      links.push([text, href]);
    }
  }
  
  return { title, links };
}

function generateModernHtml(title, contentLinks, pageFilename) {
  // Generate navigation items
  let navItems = '';
  for (const page of navPages) {
    if (page !== pageFilename) {
      const navTitle = getNavTitle(page);
      navItems += `                <li><a href="${page}">${navTitle}</a></li>\n`;
    }
  }
  
  // Generate content HTML
  let contentHtml = '';
  if (contentLinks && contentLinks.length > 0) {
    contentHtml = '<section class="content-section">\n';
    
    // Group by year
    const years = {};
    for (const [text, href] of contentLinks) {
      const yearMatch = text.match(/20\d{2}/) || href.match(/20\d{2}/);
      const year = yearMatch ? yearMatch[0] : "Other";
      
      if (!years[year]) {
        years[year] = [];
      }
      years[year].push([text, href]);
    }
    
    // Generate HTML for each year
    for (const year of Object.keys(years).sort().reverse()) {
      contentHtml += `<div class="year-section">\n`;
      contentHtml += `<h2>${year}</h2>\n`;
      contentHtml += '<ul class="document-list">\n';
      for (const [text, href] of years[year]) {
        if (href.trim()) {
          contentHtml += `<li><a href="${href}" target="_blank">${text}</a></li>\n`;
        }
      }
      contentHtml += '</ul>\n</div>\n';
    }
    
    contentHtml += '</section>\n';
  }
  
  const config = pageConfig[pageFilename] || { description: title };
  
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="${config.description}">
    <title>${title} - Cypress Point Strata</title>
    <style>
        * {
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
        
        .year-section {
            margin-bottom: 3rem;
        }
        
        .year-section h2 {
            color: #d699ad;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
            border-bottom: 2px solid #efd7df;
            padding-bottom: 0.5rem;
        }
        
        .document-list {
            list-style: none;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
        }
        
        .document-list li {
            background-color: #f8f9fa;
            border-left: 4px solid #d699ad;
            padding: 1rem;
            border-radius: 4px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .document-list li:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .document-list a {
            color: #903333;
            text-decoration: none;
            font-weight: 500;
            word-break: break-word;
        }
        
        .document-list a:hover {
            color: #d699ad;
            text-decoration: underline;
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
            
            .document-list {
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
        }
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
${navItems}        </ul>
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

// Main execution
const basePath = path.join(__dirname, 'index_files');
const pagesToProcess = Object.keys(pageConfig);

console.log('Starting modernization of Publisher pages...\n');

for (const pageFile of pagesToProcess) {
  const pagePath = path.join(basePath, pageFile);
  
  if (!fs.existsSync(pagePath)) {
    console.log(`✗ ${pageFile} - file not found`);
    continue;
  }
  
  try {
    const { title, links } = extractPageContent(pagePath);
    const modernHtml = generateModernHtml(title, links, pageFile);
    
    // Save to output file
    const outputFile = pageFile.replace('.htm', '_modern.html');
    const outputPath = path.join(__dirname, outputFile);
    fs.writeFileSync(outputPath, modernHtml, 'utf8');
    
    console.log(`✓ ${pageFile}`);
    console.log(`  Title: ${title}`);
    console.log(`  Documents: ${links.length}`);
    console.log(`  Output: ${outputFile}\n`);
  } catch (error) {
    console.log(`✗ ${pageFile} - Error: ${error.message}\n`);
  }
}

console.log('Done!');
