#!/usr/bin/env python3
"""
Extract content from Publisher HTML files (VML format)
"""
import re
import html
from pathlib import Path
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.in_script = False
        self.in_style = False
        self.in_v_shape = False
        
    def handle_starttag(self, tag, attrs):
        if tag.lower() in ['script', 'style']:
            setattr(self, f'in_{tag.lower()}', True)
        elif tag.lower() == 'v:shape' or tag.lower().startswith('v:'):
            self.in_v_shape = True
            
    def handle_endtag(self, tag):
        if tag.lower() in ['script', 'style']:
            setattr(self, f'in_{tag.lower()}', False)
        elif tag.lower() == 'v:shape' or tag.lower().startswith('v:'):
            self.in_v_shape = False
            
    def handle_data(self, data):
        if not self.in_script and not self.in_style and not self.in_v_shape:
            text = data.strip()
            if text and len(text) > 1:
                self.text_parts.append(text)

def extract_title_and_content(filepath):
    """Extract title and main content from Publisher HTML"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else "Page"
    
    # Extract text content using HTML parser
    parser = TextExtractor()
    try:
        parser.feed(content)
    except:
        pass
    
    text_content = ' '.join(parser.text_parts)
    
    # Clean up the extracted text
    # Remove excessive whitespace and common Publisher artifacts
    text_content = re.sub(r'\s+', ' ', text_content)
    text_content = re.sub(r'lang=en-US', '', text_content)
    text_content = re.sub(r'\[.*?\]', '', text_content)
    text_content = text_content.strip()
    
    return title, text_content

# Test with Page815
page_path = Path("c:/Users/g_i_f/OneDrive/Documents/GitHub/Git_Visual_Studio_Code/CypressPointStrata.github.io.worktrees/agents-publisher-website-improvements/index_files/Page815.htm")

if page_path.exists():
    title, content = extract_title_and_content(str(page_path))
    print(f"Title: {title}")
    print(f"\nContent Preview (first 500 chars):")
    print(content[:500])
    print(f"\n... (total length: {len(content)} chars)")
else:
    print(f"File not found: {page_path}")
