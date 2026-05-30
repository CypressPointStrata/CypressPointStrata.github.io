#!/usr/bin/env python3
"""
Generate modern HTML5 versions of Publisher website pages
for CypressPointStrata.github.io
"""
import re
from pathlib import Path
from html.parser import HTMLParser
from html import unescape

class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.links = []  # List of (text, href) tuples
        self.current_link_text = ""
        self.in_link = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag.lower() == 'title':
            pass
        elif tag.lower() == 'a':
            self.in_link = True
            self.current_link_href = attrs_dict.get('href', '')
            
    def handle_endtag(self, tag):
        if tag.lower() == 'a' and self.in_link:
            self.in_link = False
            if self.current_link_text.strip() and self.current_link_href:
                self.links.append((self.current_link_text.strip(), self.current_link_href))
            self.current_link_text = ""
            
    def handle_data(self, data):
        if self.in_link:
            self.current_link_text += data

def extract_page_content(filepath):
    """Extract title and links from a Publisher HTML page"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else "Page"
    
    # Extract links
    extractor = ContentExtractor()
    try:
        extractor.feed(content)
    except:
        pass
    
    return title, extractor.links

# Page mappings with titles and descriptions
page_config = {
    "Page815.htm": {"title": "Minutes", "description": "Board and shareholder meeting minutes"},
    "Page929.htm": {"title": "Procedures", "description": "Governing procedures and policies"},
    "Page1658.htm": {"title": "Reports", "description": "Financial and operational reports"},
    "Page1861.htm": {"title": "Manuals", "description": "Building and operation manuals"},
    "Page1347.htm": {"title": "Bylaws", "description": "Corporation bylaws and governance"},
    "Page1322.htm": {"title": "Pool", "description": "Pool facilities and information"},
    "Page592.htm": {"title": "Community", "description": "Community information and announcements"},
    "Page563.htm": {"title": "Events", "description": "Community events and activities"},
    "Page449.htm": {"title": "News", "description": "Latest news and updates"},
    "Page2193.htm": {"title": "Contact", "description": "Contact information and support"},
    "Page2054.htm": {"title": "Links", "description": "Useful external links and resources"},
}

# Navigation pages for menu
nav_pages = ["Page449.htm", "Page815.htm", "Page929.htm", "Page1658.htm", 
             "Page1861.htm", "Page1347.htm", "Page1322.htm", "Page592.htm", 
             "Page563.htm", "Page2193.htm", "Page2054.htm"]

def get_nav_title(page):
    """Get navigation title for a page"""
    return page_config.get(page, {}).get("title", page)

def generate_modern_html(title, content_links, page_filename):
    """Generate modern HTML5 for a page"""
    
    nav_items = ""
    for page in nav_pages:
        if page != page_filename:
            nav_title = get_nav_title(page)
            nav_items += f'                <li><a href="{page}">{nav_title}</a></li>\n'
    
    # Generate content table/list from links
    content_html = ""
    if content_links:
        content_html = '<section class="content-section">\n'
        
        # Group by year for organization
        years = {}
        for text, href in content_links:
            # Try to extract year from text or href
            year_match = re.search(r'20\d{2}', text) or re.search(r'20\d{2}', href)
            year = year_match.group(0) if year_match else "Other"
            
            if year not in years:
                years[year] = []
            years[year].append((text, href))
        
        # Generate HTML for each year
        for year in sorted(years.keys(), reverse=True):
            content_html += f'<div class="year-section">\n'
            content_html += f'<h2>{year}</h2>\n'
            content_html += '<ul class="document-list">\n'
            for text, href in years[year]:
                if href.strip():  # Only include if href is not empty
                    content_html += f'<li><a href="{href}" target="_blank">{text}</a></li>\n'
            content_html += '</ul>\n</div>\n'
        
        content_html += '</section>\n'
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{page_config.get(page_filename, {}).get('description', title)}">
    <title>{title} - Cypress Point Strata</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }}
        
        /* Header */
        header {{
            background: linear-gradient(135deg, #d699ad 0%, #903333 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        
        header h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        header p {{
            font-size: 1rem;
            opacity: 0.95;
        }}
        
        /* Navigation */
        nav {{
            background-color: #903333;
            padding: 0;
        }}
        
        nav ul {{
            list-style: none;
            display: flex;
            flex-wrap: wrap;
        }}
        
        nav li {{
            margin: 0;
        }}
        
        nav a {{
            display: block;
            padding: 1rem 1.5rem;
            color: white;
            text-decoration: none;
            transition: background-color 0.3s ease;
            white-space: nowrap;
        }}
        
        nav a:hover {{
            background-color: #d699ad;
        }}
        
        /* Main container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        main {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            padding: 2rem;
            margin-bottom: 2rem;
        }}
        
        main h1 {{
            color: #903333;
            margin-bottom: 2rem;
            font-size: 2rem;
        }}
        
        /* Content sections */
        .content-section {{
            margin: 2rem 0;
        }}
        
        .year-section {{
            margin-bottom: 3rem;
        }}
        
        .year-section h2 {{
            color: #d699ad;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
            border-bottom: 2px solid #efd7df;
            padding-bottom: 0.5rem;
        }}
        
        .document-list {{
            list-style: none;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
        }}
        
        .document-list li {{
            background-color: #f8f9fa;
            border-left: 4px solid #d699ad;
            padding: 1rem;
            border-radius: 4px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .document-list li:hover {{
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        
        .document-list a {{
            color: #903333;
            text-decoration: none;
            font-weight: 500;
            word-break: break-word;
        }}
        
        .document-list a:hover {{
            color: #d699ad;
            text-decoration: underline;
        }}
        
        /* Footer */
        footer {{
            background-color: #333;
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            font-size: 0.9rem;
        }}
        
        footer a {{
            color: #d699ad;
            text-decoration: none;
        }}
        
        footer a:hover {{
            text-decoration: underline;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            header h1 {{
                font-size: 1.5rem;
            }}
            
            nav ul {{
                flex-direction: column;
            }}
            
            nav li {{
                flex: 1;
            }}
            
            nav a {{
                padding: 0.75rem 1rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .container {{
                padding: 1rem;
            }}
            
            main {{
                padding: 1.5rem;
            }}
            
            main h1 {{
                font-size: 1.5rem;
            }}
            
            .document-list {{
                grid-template-columns: 1fr;
            }}
        }}
        
        @media (max-width: 480px) {{
            header {{
                padding: 1rem;
            }}
            
            header h1 {{
                font-size: 1.25rem;
            }}
            
            header p {{
                font-size: 0.9rem;
            }}
            
            .container {{
                padding: 0.5rem;
            }}
            
            main {{
                padding: 1rem;
            }}
            
            main h1 {{
                font-size: 1.25rem;
            }}
        }}
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
{nav_items}        </ul>
    </nav>
    
    <div class="container">
        <main>
            <h1>{title}</h1>
{content_html}        </main>
    </div>
    
    <footer>
        <p>&copy; 2024 Cypress Point Strata. All rights reserved.</p>
        <p><a href="../index.htm">Back to Home</a></p>
    </footer>
</body>
</html>"""
    
    return html

# Test with Page815.htm first
base_path = Path("c:/Users/g_i_f/OneDrive/Documents/GitHub/Git_Visual_Studio_Code/CypressPointStrata.github.io.worktrees/agents-publisher-website-improvements/index_files")

page_path = base_path / "Page815.htm"
if page_path.exists():
    title, links = extract_page_content(str(page_path))
    modern_html = generate_modern_html(title, links, "Page815.htm")
    
    # Save to output file
    output_path = base_path.parent / "Page815_modernized.html"
    with open(str(output_path), 'w', encoding='utf-8') as f:
        f.write(modern_html)
    
    print(f"✓ Generated modernized Page815.htm")
    print(f"  Title: {title}")
    print(f"  Documents found: {len(links)}")
    print(f"  Output: {output_path}")
    print(f"\nFirst few links:")
    for text, href in links[:5]:
        print(f"    - {text[:60]}")
else:
    print(f"File not found: {page_path}")
