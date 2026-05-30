# Technical Reference: Publisher HTML Content Structure

## File Metadata

| Filename | Title | Content Type | File Size Category | Document Count |
|----------|-------|--------------|-------------------|-----------------|
| Page815.htm | Minutes | Document Links | Large (161 KB) | 40+ |
| Page929.htm | Procedures | Document Links | Large | 15+ |
| Page1658.htm | Reports | Document Links | Large | 50+ |
| Page1861.htm | Manuals | Document Links | Medium | 5-10 |
| Page1347.htm | Bylaws | Document Links | Large | 10+ |
| Page1322.htm | Swimming Pool | Document Links | Small-Medium | 3-5 |
| Page592.htm | Contacts | Contact Info | Small-Medium | 5+ |
| Page563.htm | External Links | External Links | Small-Medium | 10+ |
| Page449.htm | About Us | Navigation | Small | Navigation |
| Page2193.htm | Minutes Archive | Document Links | Large | 50+ |
| Page2054.htm | External Links | External Links | Small | 5+ |

---

## HTML Structure Analysis

### Common Publisher HTML Patterns

#### 1. VML Graphics (Ignored in extraction)
```html
<v:shape id="_x0000_s1674" type="#_x0000_t202">
  <!-- Used for navigation buttons, backgrounds, decorative elements -->
</v:shape>

<v:rect id="_x0000_s1790" href="Page929.htm">
  <!-- Clickable navigation elements -->
</v:rect>
```

#### 2. MSO Office Styles (Ignored in extraction)
```html
<style>
  p.MsoNormal { ... }
  p.MsoOrganizationName { ... }
  p.MsoTagline { ... }
  h4 { font-family:"Arial Black"; }
</style>
```

#### 3. Title Declaration
```html
<title>Minutes</title>
```
- Extracted from each file
- Provides page identification

#### 4. Navigation Links (Extracted)
```html
<v:rect id="_x0000_s1782" href="../index.htm" style='position:absolute;...'/>
<v:rect id="_x0000_s1785" href="Page449.htm" style='position:absolute;...'/>
```
- Links to other pages in the site
- Consistent across all pages

#### 5. Content Links (Extracted - Primary Focus)
```html
<p class=MsoNormal>
  <a href="documents/minutes/2026/2026-02-04%20Strata%20Council%20Meeting%20Minutes.pdf" 
     target="_blank" rel="noopener noreferrer">
    <span lang=en-US style='...'>2026-02-04 Meeting Minutes</span>
  </a>
</p>
```

#### 6. Image Map Navigation (Extracted)
```html
<map name="ImageMap1">
  <area shape=Rect coords="0, 370, 167, 403" href="Page2193.htm">
  <area shape=Rect coords="0, 336, 167, 370" href="Page2054.htm">
  <!-- Maps image coordinates to navigation links -->
</map>
```

#### 7. Table-Based Content (Extracted)
```html
<table v:shapes="_x0000_s2341" cellpadding=0 cellspacing=0 width=345>
  <tr>
    <td width=345 height=38 valign=Top>
      <p class=MsoNormal>
        <span lang=en-US style='font-weight:bold;'>Notices</span>
      </p>
    </td>
  </tr>
  <!-- Content organized in table cells -->
</table>
```

---

## Extraction Methodology

### Step 1: Title Extraction
```regex
<title>([^<]+)</title>
```
- Captures page title for identification
- Used for content_type determination

### Step 2: Link Extraction
```regex
<a\s+href=["\']([^"\']*)["\'][^>]*?>([^<]+)<
```
- Extracts all hyperlinks and their visible text
- Filters by content type (documents/ vs external)
- Distinguishes between navigation and content links

### Step 3: Content Type Classification
- **document_links**: Links to documents/directory (>3 docs)
- **external_links**: Links to http/https URLs
- **contact_information**: Email, phone, address data
- **navigation**: Links primarily to other .htm files
- **text_content**: Narrative or descriptive text

### Step 4: Structure Extraction
- Headings and sections identified by context
- Table headers captured as section markers
- Document groupings inferred from href patterns

---

## Document Directory Structure

```
index_files/documents/
├── minutes/
│   ├── 2026/
│   │   ├── 2026-02-04 Strata Council Meeting Minutes.pdf
│   │   ├── 2026-03-06 Strata Council Meeting Minutes.pdf
│   │   └── ...
│   ├── 2025/
│   │   ├── 2025-01-16-SGM-Minutes.pdf
│   │   ├── 2025-11-13-AGM-Minutes.pdf
│   │   └── ...
│   ├── 2024/
│   ├── 2023/
│   ├── 2012/
│   ├── 2010/
│   └── ... (earlier years)
├── procedures/
│   ├── Welcome Package 2007.pdf
│   ├── Fire Safety Plan.pdf
│   ├── Roof Fan Timer Change Procedure.pdf
│   ├── Pool Rules and Regulations.pdf
│   └── ... (15+ procedure documents)
├── manuals/
│   ├── BowFlexXtremeSEOwnersManual.pdf
│   ├── Rain Bird ESP-LX.pdf
│   ├── Rain Bird E-Class.pdf
│   └── ...
├── reports/
│   ├── Financial Reports (multiple by year)
│   ├── Audit Reports (multiple)
│   └── Special Reports
├── contacts/
│   └── EMERGENCY CONTACT LIST.pdf
├── goverment documents/
│   └── Guide12 - CRF and Special Levies.pdf
└── bylaws/
    ├── 2025-Oct-16 Bylaws Strata NW2050.pdf (CURRENT)
    ├── 2023-Dec-04 Bylaws Strata NW2050.v2.pdf
    ├── 2022-Dec-07 Bylaws Strata NW2050.pdf
    └── ... (back to 2006)
```

---

## Page-to-Page Navigation Map

```
All pages link to:
├─ Page815.htm (Minutes) ◄──►
├─ Page929.htm (Procedures) ◄──►
├─ Page1658.htm (Reports) ◄──►
├─ Page1861.htm (Manuals) ◄──►
├─ Page1347.htm (Bylaws) ◄──►
├─ Page1322.htm (Swimming Pool) ◄──►
├─ Page592.htm (Contacts) ◄──►
├─ Page563.htm (External Links) ◄──►
├─ Page449.htm (About Us) ◄──►
├─ Page2193.htm (Minutes Archive) ◄──►
└─ Page2054.htm (External Links) ◄──►
```

Each page includes a left-side navigation menu with image map and clickable rectangles.

---

## Link Pattern Analysis

### Document Links Pattern
```
href="documents/[category]/[filename].pdf"
Examples:
- documents/minutes/2026/2026-02-04%20Strata%20Council%20Meeting%20Minutes.pdf
- documents/procedures/Fire%20Safety%20Plan.pdf
- documents/manuals/BowFlexXtremeSEOwnersManual.pdf
```

### External Links Pattern
```
href="http[s]://[domain]/[path]"
Examples:
- http://www.choa.bc.ca
- http://www.bclaws.ca/EPLibraries/bclaws_new/document/ID/freeside/98043_01
- https://calendar.google.com/calendar/embed?src=...
```

### Internal Navigation Pattern
```
href="Page[number].htm"
Examples:
- Page815.htm
- Page929.htm
- ../index.htm (parent directory)
```

### Email Pattern
```
href="mailto:[email]?subject=[subject]"
Examples:
- mailto:cypresspointnw2050@gmail.com?subject=Cypress%20Point%20Office%20email
```

---

## Content Statistics

### By Page Type
- **Document Link Pages:** 8 (Pages 815, 929, 1658, 1861, 1347, 1322, 592, 2193)
- **External Link Pages:** 2 (Pages 563, 2054)
- **Navigation Pages:** 1 (Page 449)

### Total Estimated Documents
- Minutes: 100+
- Procedures: 15+
- Reports: 50+
- Manuals: 5+
- Bylaws: 10+
- Contacts: 5+
- External Resources: 15+

### Archive Depth
- Minutes Archive: 2010-2026 (16 years)
- Bylaws Archive: 2006-2025 (19 years)
- Historical Data: Maintained for 15+ years

---

## Technical Implementation Notes

### HTML Generation
- Source: Microsoft Publisher (VML-based)
- Encoding: windows-1252 (Windows Latin-1)
- Parser: HTML 4.0 compatible
- Features: VML shapes, image maps, embedded styles

### Browser Compatibility
- Uses MSO (Microsoft Office) extensions
- Includes fallback styles for non-MS browsers
- Image maps for navigation (requires bitmap images)

### File Encoding Handling
```python
# Proper way to read these files:
with open(filepath, 'r', encoding='windows-1252', errors='ignore') as f:
    content = f.read()
```

### Content Extraction Challenges
1. VML markup must be stripped (graphical elements)
2. MSO styles must be ignored (formatting metadata)
3. URL encoding in href attributes (spaces as %20)
4. Nested span elements with multiple style attributes
5. Image maps separate from actual content links

---

## Recommendations for Modernization

### 1. Remove VML Graphics
- Replace with CSS/SVG alternatives
- Clean HTML structure

### 2. Simplify Navigation
- Remove image maps
- Use standard CSS-based navigation

### 3. Reorganize Content
- Create structured data files (JSON/YAML)
- Link to document management system

### 4. Update Encoding
- Convert to UTF-8
- Remove windows-1252 dependency

### 5. Improve Accessibility
- Add proper heading hierarchy
- Improve semantic HTML
- Update ARIA labels

---

## Files Generated by This Extraction

1. **PUBLISHER_CONTENT_EXTRACTION.json**
   - Structured JSON format
   - All 11 pages documented
   - Sample links and sections

2. **PUBLISHER_EXTRACTION_SUMMARY.md**
   - Human-readable markdown
   - Organized by page
   - Key findings and patterns

3. **TECHNICAL_REFERENCE.md** (this file)
   - Technical specifications
   - HTML pattern analysis
   - Extraction methodology

---

## Related Files in Repository

- `index_files/` - All Publisher HTML files
- `index_files/documents/` - Document archives
- `extract_content.py` - Original extraction script
- `extract_full_content.py` - Enhanced extraction script
- `extract_publisher_content.py` - Comprehensive extraction

---

Generated: 2025 (Current Session)  
Source: Publisher HTML files from Cypress Point Strata website
