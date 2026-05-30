#!/usr/bin/env python3
"""
Comprehensive extraction of content from Publisher HTML files
"""

import os
import re
import json
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict

class PublisherParser(HTMLParser):
    """Extract meaningful content from Publisher-generated HTML"""
    
    def __init__(self):
        super().__init__()
        self.title = ""
        self.links = []
        self.text_content = []
        self.sections = defaultdict(list)
        self.current_section = None
        self.skip_vml = False
        self.skip_style = False
        self.skip_script = False
        self.in_table_cell = False
        self.cell_content = ""
        self.link_cache = {}
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = {k: v for k, v in attrs}
        
        # Track navigation
        if tag in ['v:shape', 'v:rect', 'v:line']:
            self.skip_vml = True
            return
        
        if tag == 'style':
            self.skip_style = True
            return
        
        if tag == 'script':
            self.skip_script = True
            return
        
        if self.skip_vml or self.skip_style or self.skip_script:
            return
        
        # Extract links
        if tag == 'a' and 'href' in attrs_dict:
            href = attrs_dict['href'].strip()
            if href:
                self.link_cache['current_href'] = href
        
        # Track table cells
        if tag == 'td':
            self.in_table_cell = True
            self.cell_content = ""
        
        # Track headings as sections
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.current_section = f"Heading-{tag}"
    
    def handle_endtag(self, tag):
        if tag == 'v:shape' or tag == 'v:rect' or tag == 'v:line':
            self.skip_vml = False
        elif tag == 'style':
            self.skip_style = False
        elif tag == 'script':
            self.skip_script = False
        elif tag == 'td':
            if self.cell_content.strip():
                if 'current_href' in self.link_cache:
                    self.links.append({
                        'text': self.cell_content.strip(),
                        'href': self.link_cache.pop('current_href')
                    })
                else:
                    self.text_content.append(self.cell_content.strip())
            self.in_table_cell = False
            self.cell_content = ""
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.current_section = None
    
    def handle_data(self, data):
        text = data.strip()
        
        if not text or len(text) < 2:
            return
        
        if self.skip_vml or self.skip_style or self.skip_script:
            return
        
        # Collect text
        if self.in_table_cell:
            self.cell_content += " " + text
        elif len(text) > 5:
            self.text_content.append(text)
            if self.current_section:
                self.sections[self.current_section].append(text)

def extract_links_from_href(filepath):
    """Extract all href links and their context"""
    try:
        with open(filepath, 'r', encoding='windows-1252', errors='ignore') as f:
            content = f.read()
    except:
        return []
    
    # Find all <a href...> tags with actual content
    pattern = r'<a\s+href=["\']([^"\']*)["\'][^>]*?>([^<]+)<'
    matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
    
    links = []
    for href, text in matches:
        href = href.strip()
        text = text.strip()
        if href and len(text) > 2:  # Only meaningful links
            links.append({'href': href, 'text': text[:100]})
    
    return links

def extract_from_file(filepath):
    """Extract all useful content from a Publisher HTML file"""
    
    filename = os.path.basename(filepath)
    
    try:
        with open(filepath, 'r', encoding='windows-1252', errors='ignore') as f:
            html_content = f.read()
    except Exception as e:
        return {'filename': filename, 'error': str(e)}
    
    # Extract title
    title_match = re.search(r'<title>([^<]+)</title>', html_content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "Untitled"
    
    # Extract all links
    links = extract_links_from_href(filepath)
    
    # Parse HTML for structure
    parser = PublisherParser()
    try:
        parser.feed(html_content)
    except:
        pass
    
    # Determine content type
    content_type = "navigation"
    doc_links = [l for l in links if 'documents' in l['href'].lower()]
    page_links = [l for l in links if l['href'].endswith('.htm')]
    
    if len(doc_links) > 3:
        content_type = "document_links"
    elif len(page_links) > 5:
        content_type = "navigation"
    elif len(parser.text_content) > 10:
        content_type = "text_content"
    
    # Get sections/headings
    sections = []
    for section_type, content_list in parser.sections.items():
        for item in content_list[:3]:
            if len(item) > 5:
                sections.append(item)
    
    # Compile results
    result = {
        'filename': filename,
        'title': title,
        'content_type': content_type,
        'total_links': len(links),
        'document_count': len(doc_links),
        'navigation_links': len(page_links),
        'links': links[:15],  # Top 15 links
        'sections': sections[:8],
        'text_sample': ' '.join(parser.text_content[:300]).strip()[:300]
    }
    
    return result

def main():
    files_to_process = {
        'Page815.htm': 'Minutes',
        'Page929.htm': 'Procedures',
        'Page1658.htm': 'Reports',
        'Page1861.htm': 'Manuals',
        'Page1347.htm': 'Bylaws',
        'Page1322.htm': 'Swimming Pool',
        'Page592.htm': 'Contacts (Community)',
        'Page563.htm': 'External Links (Events)',
        'Page449.htm': 'About Us (News)',
        'Page2193.htm': 'Minutes Archive (Contact)',
        'Page2054.htm': 'External Links',
    }
    
    index_files_dir = 'index_files'
    results = []
    
    print("\n" + "="*100)
    print("PUBLISHER HTML CONTENT EXTRACTION")
    print("="*100 + "\n")
    
    for filename, description in files_to_process.items():
        filepath = os.path.join(index_files_dir, filename)
        if os.path.exists(filepath):
            print(f"Processing {filename} ({description})...", end=" ")
            result = extract_from_file(filepath)
            results.append(result)
            print("✓")
        else:
            print(f"NOT FOUND: {filepath}")
    
    # Display summary
    print("\n" + "="*100)
    print("EXTRACTION SUMMARY")
    print("="*100 + "\n")
    
    for result in results:
        print(f"\n{'='*80}")
        print(f"File: {result['filename']}")
        print(f"Title: {result['title']}")
        print(f"Content Type: {result['content_type']}")
        print(f"Total Links: {result['total_links']} (Documents: {result['document_count']}, Navigation: {result['navigation_links']})")
        
        if result.get('links'):
            print(f"\nTop Links:")
            for i, link in enumerate(result['links'][:5], 1):
                text_display = link['text'][:50] if link['text'] else "(no text)"
                print(f"  {i}. href: {link['href']}")
                print(f"     text: {text_display}")
        
        if result.get('sections'):
            print(f"\nSections:")
            for section in result['sections'][:5]:
                print(f"  • {section[:70]}")
        
        if result.get('text_sample'):
            print(f"\nText Sample:")
            print(f"  {result['text_sample'][:100]}...")
    
    # Save as JSON
    with open('extracted_content.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*100}")
    print(f"✓ Results saved to extracted_content.json")
    print(f"✓ Processed {len(results)} files")

if __name__ == '__main__':
    main()
