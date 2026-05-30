#!/usr/bin/env python3
"""Extract content from Publisher HTML files and create modern HTML5 versions."""

import os
import re
from pathlib import Path
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    """Extract clean text from Publisher HTML."""
    
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_body = False
        self.skip_tags = {'style', 'script', 'v:*', 'o:*'}
        
    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True
            
    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False
            
    def handle_data(self, data):
        if self.in_body:
            text = data.strip()
            if text and len(text) > 2:  # Skip tiny fragments
                self.text.append(text)

def extract_title_from_file(content):
    """Extract title from HTML."""
    match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    return match.group(1) if match else "Cypress Point Strata"

def extract_text(content):
    """Extract clean text from Publisher HTML."""
    # Remove VML and Office-specific markup
    content = re.sub(r'<!--\[if[^>]*>.*?<!\[endif\]-->', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<v:[^>]*>.*?</v:[^>]*>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<o:[^>]*>.*?</o:[^>]*>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'style=["\'](?:[^"\'\\]|\\.)*["\']', '', content)
    
    parser = TextExtractor()
    try:
        parser.feed(content)
    except:
        pass
    
    # Clean up text
    texts = []
    for item in parser.text:
        item = item.strip()
        if item and len(item) > 1:
            texts.append(item)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_texts = []
    for text in texts:
        if text not in seen and text.lower() not in [t.lower() for t in seen]:
            seen.add(text)
            unique_texts.append(text)
    
    return unique_texts

def create_modern_html(title, content_paragraphs, page_id):
    """Create a modern HTML5 version."""
    # Build content sections
    content_html = ""
    if content_paragraphs:
        content_html = "\n        ".join(f"<p>{para}</p>" for para in content_paragraphs[:20])  # Limit to first 20 paragraphs
    
    nav_link_mapping = {
        'Page815': ('Minutes', '../index_files/Page815.htm'),
        'Page929': ('Procedures', '../index_files/Page929.htm'),
        'Page1658': ('Reports', '../index_files/Page1658.htm'),
        'Page1861': ('Manuals', '../index_files/Page1861.htm'),
        'Page1347': ('Bylaws', '../index_files/Page1347.htm'),
        'Page1322': ('Pool', '../index_files/Page1322.htm'),
    }
    
    # Build navigation
    nav_items = [
        '<li><a href="../index.htm">Home</a></li>',
        '<li><a href="../index.htm#about">About Us</a></li>',
    ]
    
    for page_key, (link_title, link_href) in nav_link_mapping.items():
        if page_key != page_id:
            nav_items.append(f'<li><a href="{link_href}">{link_title}</a></li>')
    
    nav_items.append('<li><a href="../index.htm#contact">Contact</a></li>')
    nav_html = "\n                    ".join(nav_items)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Cypress Point Strata NW2050 - {title}">
    <meta name="theme-color" content="#d699ad">
    <title>{title} - Cypress Point Strata NW2050</title>
    <link rel="icon" href="../favicon.ico" type="image/x-icon">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary-color: #d699ad;
            --secondary-color: #903333;
            --accent-color: #efd7df;
            --text-dark: #333;
            --text-light: #666;
            --bg-light: #f9f9f9;
            --border-color: #ddd;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: #fff;
        }}

        /* Header & Navigation */
        header {{
            background: linear-gradient(135deg, var(--primary-color) 0%, #c984a0 100%);
            color: white;
            padding: 2rem 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        header .container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 2rem;
        }}

        .logo-section {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .logo-section img {{
            height: 50px;
            width: auto;
        }}

        .logo-text h1 {{
            font-size: 1.5rem;
            font-weight: 600;
            margin: 0;
        }}

        .logo-text p {{
            font-size: 0.85rem;
            opacity: 0.95;
            margin: 0.25rem 0 0 0;
        }}

        nav ul {{
            list-style: none;
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            justify-content: flex-end;
        }}

        nav a {{
            color: white;
            text-decoration: none;
            padding: 0.4rem 0.8rem;
            border-radius: 4px;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }}

        nav a:hover {{
            background-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }}

        nav a:focus {{
            outline: 2px solid white;
            outline-offset: 2px;
        }}

        /* Container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        /* Main Content */
        main {{
            min-height: calc(100vh - 200px);
            padding: 3rem 0;
        }}

        .page-header {{
            background: linear-gradient(135deg, var(--accent-color) 0%, #f5e5f0 100%);
            padding: 2rem 0;
            margin-bottom: 2rem;
            border-radius: 8px;
        }}

        .page-header h1 {{
            font-size: 2rem;
            color: var(--text-dark);
            margin-bottom: 0.5rem;
        }}

        .page-header p {{
            color: var(--text-light);
            font-size: 1rem;
        }}

        .content {{
            background: var(--bg-light);
            padding: 2rem;
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
        }}

        .content p {{
            margin-bottom: 1rem;
            color: var(--text-light);
            line-height: 1.7;
        }}

        .content p:last-child {{
            margin-bottom: 0;
        }}

        /* Footer */
        footer {{
            background: var(--text-dark);
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            font-size: 0.9rem;
        }}

        footer a {{
            color: var(--primary-color);
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        /* Back to Home */
        .back-link {{
            margin-bottom: 2rem;
            text-align: center;
        }}

        .back-link a {{
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
        }}

        .back-link a:hover {{
            color: var(--secondary-color);
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .container {{
                padding: 0 1rem;
            }}

            header .container {{
                flex-direction: column;
                gap: 1rem;
            }}

            nav ul {{
                flex-direction: row;
                gap: 0.3rem;
                justify-content: center;
            }}

            nav a {{
                padding: 0.3rem 0.6rem;
                font-size: 0.85rem;
            }}

            .page-header h1 {{
                font-size: 1.5rem;
            }}

            main {{
                padding: 1.5rem 0;
            }}
        }}

        /* Accessibility */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
                scroll-behavior: auto !important;
            }}
        }}

        /* Print Styles */
        @media print {{
            nav, footer, .back-link {{
                display: none;
            }}

            body {{
                background: white;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="logo-section">
                <a href="../index.htm" style="display: flex; align-items: center; gap: 1rem; text-decoration: none; color: white;">
                    <img src="../index_files/image748.jpg" alt="Cypress Point Strata Logo" width="50" height="50">
                    <div class="logo-text">
                        <h1>Cypress Point Strata</h1>
                        <p>NW2050</p>
                    </div>
                </a>
            </div>
            <nav>
                <ul>
                    {nav_html}
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <div class="back-link">
                <a href="../index.htm">&larr; Back to Home</a>
            </div>

            <section class="page-header">
                <h1>{title}</h1>
                <p>Cypress Point Strata NW2050</p>
            </section>

            <section class="content">
                {content_html}
            </section>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 Cypress Point Strata NW2050. All rights reserved.</p>
            <p><a href="../index.htm">Back to Home</a></p>
        </div>
    </footer>
</body>
</html>'''
    
    return html

def main():
    """Process all Publisher pages."""
    index_files_dir = Path('index_files')
    if not index_files_dir.exists():
        print("index_files directory not found")
        return
    
    pages = {
        'Page815.htm': 'Minutes',
        'Page929.htm': 'Procedures',
        'Page1658.htm': 'Reports',
        'Page1861.htm': 'Manuals',
        'Page1347.htm': 'Bylaws',
        'Page1322.htm': 'Pool',
        'Page592.htm': 'Additional Information',
        'Page563.htm': 'More Resources',
        'Page449.htm': 'Documentation',
        'Page2193.htm': 'Archives',
        'Page2054.htm': 'References',
    }
    
    for filename, default_title in pages.items():
        filepath = index_files_dir / filename
        if not filepath.exists():
            print(f"⊘ {filename} not found")
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            title = extract_title_from_file(content)
            if not title or title.lower() == 'home':
                title = default_title
            
            paragraphs = extract_text(content)
            
            # Filter out very short paragraphs and duplicates
            paragraphs = [p for p in paragraphs if len(p) > 20 and len(p) < 500]
            
            page_id = filename.replace('.htm', '')
            modern_html = create_modern_html(title, paragraphs, page_id)
            
            # Write modernized version
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(modern_html)
            
            print(f"✓ Modernized {filename} ({title}) - {len(paragraphs)} paragraphs extracted")
            
        except Exception as e:
            print(f"✗ Error processing {filename}: {str(e)}")

if __name__ == '__main__':
    main()
