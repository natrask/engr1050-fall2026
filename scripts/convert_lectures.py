import re
import os

# HTML Template
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - ENM5320</title>
    
    <!-- KaTeX CSS and JS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
    
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
        }}

        h1 {{
            color: #011F5B;
            border-bottom: 3px solid #990000;
            padding-bottom: 10px;
            margin-top: 30px;
        }}

        h2 {{
            color: #011F5B;
            margin-top: 30px;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 5px;
        }}

        h3 {{
            color: #011F5B;
            margin-top: 20px;
        }}

        h4 {{
            color: #011F5B;
            margin-top: 15px;
        }}

        p {{
            text-align: justify;
            margin-bottom: 15px;
        }}

        ul, ol {{
            margin-bottom: 15px;
        }}

        li {{
            margin-bottom: 8px;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}

        th, td {{
            border: 1px solid #e0e0e0;
            padding: 10px;
            text-align: left;
        }}

        th {{
            background: #f8f9fa;
            color: #011F5B;
            font-weight: bold;
        }}

        .katex-display {{
            margin: 1.5em 0;
            overflow-x: auto;
            overflow-y: hidden;
        }}

        .definition {{
            background: #f8f9fa;
            border-left: 4px solid #82AFD3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}

        .summary-box {{
            background: #fff3cd;
            border: 1px solid #F2C100;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}

        .example-box {{
            background: #e8f4f8;
            border-left: 4px solid #82AFD3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}

        .theorem-box {{
            background: #f0f0f0;
            border: 2px solid #011F5B;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}

        strong {{
            color: #011F5B;
        }}

        .back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #82AFD3;
            text-decoration: none;
        }}

        .back-link:hover {{
            text-decoration: underline;
        }}

        hr {{
            border: none;
            border-top: 1px solid #e0e0e0;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    <a href="../../index.html" class="back-link">← Back to Course Schedule</a>
    
{body}

    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            renderMathInElement(document.body, {{
                delimiters: [
                    {{left: "$$", right: "$$", display: true}},
                    {{left: "\\\\[", right: "\\\\]", display: true}},
                    {{left: "$", right: "$", display: false}},
                    {{left: "\\\\(", right: "\\\\)", display: false}}
                ],
                throwOnError: false
            }});
        }});
    </script>
</body>
</html>'''

def convert_markdown_to_html(md_content):
    """Convert markdown content to HTML body"""
    # This is a simplified converter - preserves markdown structure but wraps in HTML
    return md_content

def process_lecture(lecture_num, source_folder, dest_folder):
    """Process a single lecture markdown file to HTML"""
    md_path = os.path.join(source_folder, f'Lecture_{lecture_num}', f'Lecture_{lecture_num}.md')
    
    if not os.path.exists(md_path):
        print(f"❌ Lecture {lecture_num}: File not found")
        return False
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title_match = re.match(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else f"Lecture {lecture_num}"
    
    # Create HTML (using raw markdown for now - proper conversion would take longer)
    body = f"<pre>{content}</pre>"  # Placeholder - will be replaced with proper HTML
    
    html_content = HTML_TEMPLATE.format(title=title, body=body)
    
    # Write HTML file
    html_path = os.path.join(dest_folder, f'Lecture_{lecture_num}.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Lecture {lecture_num}: {title}")
    return True

# Main conversion
if __name__ == "__main__":
    base = r"c:\Users\nattr\OneDrive\Desktop\GitRepos\ENM5320-Spring2026\ENM5320-2026"
    source = os.path.join(base, "LectureConversion")
    
    # Lecture to folder mapping
    mappings = [
        (6, "Lecture05_Feb03"),
        (7, "Lecture06_Feb05"),
        (8, "Lecture07_Feb10"),
        (9, "Lecture08_Feb12"),
        (10, "Lecture09_Feb17"),
        (11, "Lecture10_Feb19"),
        (12, "Lecture11_Feb24"),
        (13, "Lecture12_Feb26"),
        (14, "Lecture13_Mar03"),
        (15, "Lecture14_Mar05"),
        (16, "Lecture16_Mar19"),
        (17, "Lecture17_Mar24"),
        (18, "Lecture18_Mar26"),
        (19, "Lecture19_Mar31"),
        (20, "Lecture20_Apr02")
    ]
    
    print("Starting conversion...")
    for lec_num, folder in mappings:
        dest = os.path.join(base, "NewMaterial", folder)
        if not os.path.exists(dest):
            print(f"⚠ Warning: Folder {folder} does not exist")
            continue
        process_lecture(lec_num, source, dest)
    
    print("\nConversion complete!")
