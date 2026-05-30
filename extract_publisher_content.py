#!/usr/bin/env python3
"""
Extract content from Publisher HTML files
"""

import os
import re
import json
from pathlib import Path
from html.parser import HTMLParser
from typing import Dict, List, Any

class ContentExtractor(HTMLParser):
    """Extract text content and links from HTML, ignoring VML and MSO styles"""
    
    def __init__(self):
        super().__init__()
        self.in_vml = False
        self.in_style = False
        self.in_script = False
        self.text_content = []
        self.links = []
        self.title = ""
        self.sections = []
        self.heading_text = ""
        self.in_heading = False
        self.skip_depth = 0
    
    def handle_starttag(self, tag, attrs):
        # Skip VML and Office markup
        if tag in ['v:shape', 'v:rect', 'v:line', 'v:path', 'o:p', 'w:p']:
            self.in_vml = True
            self.skip_depth += 1
            return
        
        if tag == 'style' or tag == 'script':
            self.skip_depth += 1
            return
        
        if self.skip_depth > 0:
            return
        
        attrs_dict = {k: v for k, v in attrs}
        
        # Capture title
        if tag == 'title':
            self.in_heading = True
            return
        
        # Extract headings
        if tag.startswith('h') and tag[1].isdigit():
            self.in_heading = True
            self.heading_text = ""
            return
        
        # Extract links
        if tag == 'a' and 'href' in attrs_dict:
            href = attrs_dict['href']
            if href and href.strip():  # Only non-empty hrefs
                self.links.append({'href': href, 'text': ''})
        
        # Track paragraphs
        if tag == 'p':
            self.text_content.append('\n')
    
    def handle_endtag(self, tag):
        if tag in ['v:shape', 'v:rect', 'v:line', 'v:path', 'o:p', 'w:p']:
            self.skip_depth = max(0, self.skip_depth - 1)
            self.in_vml = False
            return
        
        if tag in ['style', 'script']:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        
        if self.skip_depth > 0:
            return
        
        # Capture heading content
        if tag.startswith('h') and tag[1].isdigit():
            if self.heading_text.strip():
                self.sections.append(self.heading_text.strip())
            self.in_heading = False
            self.heading_text = ""
            return
        
        # Capture title
        if tag == 'title':
            self.in_heading = False
            return
    
    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        
        text = data.strip()
        if not text:
            return
        
        # Capture title
        if self.title == "" and len(self.text_content) == 0:
            self.title = text
            return
        
        # Add to heading text
        if self.in_heading:
            self.heading_text += text + " "
            return
        
        # Add regular text
        if len(text) > 5:  # Only significant text
            self.text_content.append(text)
        
        # Update link text for the most recent link
        if self.links and not self.links[-1]['text']:
            self.links[-1]['text'] = text

def extract_file_content(filepath: str) -> Dict[str, Any]:
    """Extract content from a single HTML file"""
    
    filename = os.path.basename(filepath)
    
    try:
        with open(filepath, 'r', encoding='windows-1252', errors='ignore') as f:
            html_content = f.read()
    except Exception as e:
        return {
            'filename': filename,
            'error': str(e)
        }
    
    # Extract title from <title> tag using regex
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    title = title_match.group(1) if title_match else "Unknown"
    
    # Parse with our custom parser
    parser = ContentExtractor()
    try:
        parser.feed(html_content)
    except Exception as e:
        pass  # Continue even if parsing fails
    
    # Clean up the title if the parser also found one
    if parser.title and parser.title != title:
        # Use the explicit title tag value
        pass
    
    # Extract unique links (remove duplicates)
    unique_links = []
    seen_hrefs = set()
    for link in parser.links:
        if link['href'] and link['href'] not in seen_hrefs:
            seen_hrefs.add(link['href'])
            unique_links.append(link)
    
    # Determine content type
    content_type = "text_content"
    if len(unique_links) > 5 and any('documents' in link['href'] for link in unique_links):
        content_type = "document_links"
    elif len(unique_links) > 0 and all(link['href'].endswith('.htm') for link in unique_links if link['href']):
        content_type = "navigation"
    
    # Get text preview
    raw_text = ' '.join(parser.text_content[:500]).strip()
    if len(raw_text) > 500:
        raw_text = raw_text[:500] + "..."
    
    return {
        'filename': filename,
        'title': title,
        'content_type': content_type,
        'links': unique_links[:20],  # Limit to 20 most relevant links
        'sections': list(dict.fromkeys(parser.sections))[:10],  # Remove duplicates, limit to 10
        'raw_text_preview': raw_text,
        'link_count': len(unique_links)
    }

def main():
    # List of files to process
    files_to_process = [
        'Page815.htm',    # Minutes
        'Page929.htm',    # Procedures
        'Page1658.htm',   # Reports
        'Page1861.htm',   # Manuals
        'Page1347.htm',   # Bylaws
        'Page1322.htm',   # Pool
        'Page592.htm',    # Community
        'Page563.htm',    # Events
        'Page449.htm',    # News
        'Page2193.htm',   # Contact
        'Page2054.htm',   # Links
    ]
    
    index_files_dir = 'index_files'
    results = []
    
    for filename in files_to_process:
        filepath = os.path.join(index_files_dir, filename)
        if os.path.exists(filepath):
            print(f"Processing {filename}...")
            result = extract_file_content(filepath)
            results.append(result)
        else:
            print(f"File not found: {filepath}")
    
    # Output results
    print("\n" + "="*80)
    print("EXTRACTED CONTENT SUMMARY")
    print("="*80 + "\n")
    
    for result in results:
        print(f"File: {result['filename']}")
        print(f"Title: {result.get('title', 'Unknown')}")
        print(f"Content Type: {result.get('content_type', 'Unknown')}")
        print(f"Number of Links: {result.get('link_count', 0)}")
        print(f"Sections Found: {len(result.get('sections', []))}")
        
        if result.get('links'):
            print(f"\nTop Links:")
            for i, link in enumerate(result['links'][:5], 1):
                text = link['text'][:50] if link['text'] else "(no text)"
                print(f"  {i}. {link['href']} - {text}")
        
        if result.get('sections'):
            print(f"\nSections:")
            for section in result['sections'][:5]:
                print(f"  - {section[:70]}")
        
        if result.get('raw_text_preview'):
            preview = result['raw_text_preview'][:150]
            print(f"\nText Preview: {preview}...")
        
        print("\n" + "-"*80 + "\n")
    
    # Save as JSON
    with open('extracted_content.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to extracted_content.json")

if __name__ == '__main__':
    main()
