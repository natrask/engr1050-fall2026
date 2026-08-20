import re
import os
import sys

def convert_md_to_html(md_path, html_path, lecture_num):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title_match = re.match(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else f"Lecture {lecture_num}"
    
    # Extract reference
    ref_match = re.search(r'\*\*Reference:\*\*\s+\[([^\]]+)\]\(([^)]+)\)', content)
    reference = f'<p><strong>Reference:</strong> <a href="{ref_match.group(2)}">{ref_match.group(1)}</a></p>' if ref_match else ""
    
    # Extract topics
    topics_match = re.search(r'\*\*Topics:\*\*\s+(.+)', content)
    topics = f'<p><strong>Topics:</strong> {topics_match.group(1)}</p>' if topics_match else ""
    
    print(f"Processing Lecture {lecture_num}: {title}")
    return title, reference, topics

# Test
if len(sys.argv) > 1:
    md_path = sys.argv[1]
    if os.path.exists(md_path):
        title, ref, topics = convert_md_to_html(md_path, "", "")
        print(f"Title: {title}")
    else:
        print(f"File not found: {md_path}")
