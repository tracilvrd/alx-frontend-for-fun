#!/usr/bin/python3

import sys
import os
import re

def convert_markdown_to_html(input_file, output_file):
    # Check the number of arguments
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    # Check if the input file exists
    if not os.path.exists(input_file) or not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # Read the Markdown file and convert it to HTML
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

        # Convert headings
        md_content = re.sub(r'^#\s(.+)$', r'<h1>\1</h1>', md_content, flags=re.M)
        md_content = re.sub(r'^##\s(.+)$', r'<h2>\1</h2>', md_content, flags=re.M)
        md_content = re.sub(r'^###\s(.+)$', r'<h3>\1</h3>', md_content, flags=re.M)
        md_content = re.sub(r'^####\s(.+)$', r'<h4>\1</h4>', md_content, flags=re.M)
        md_content = re.sub(r'^#####\s(.+)$', r'<h5>\1</h5>', md_content, flags=re.M)
        md_content = re.sub(r'^######\s(.+)$', r'<h6>\1</h6>', md_content, flags=re.M)

        # Convert unordered lists
        md_content = re.sub(r'^-\s(.+)$', r'<ul>\n    <li>\1</li>\n</ul>', md_content, flags=re.M)

        # Convert ordered lists
        md_content = re.sub(r'^\*\s(.+)$', r'<ol>\n    <li>\1</li>\n</ol>', md_content, flags=re.M)

        # Convert paragraphs
        md_content = re.sub(r'^(?!<)[^\n]+$', r'<p>\n    \1\n</p>', md_content, flags=re.M)
        md_content = re.sub(r'\n\n', r'\n    <br />\n\n', md_content, flags=re.M)

        # Convert bold
        md_content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', md_content)
        md_content = re.sub(r'__(.+?)__', r'<em>\1</em>', md_content)

        # Convert MD5 and remove 'c' (case-insensitive)
        md5_content = re.sub(r'\[\[(.+?)\]\]', lambda x: hashlib.md5(x.group(1).encode('utf-8')).hexdigest(), md_content)
        no_c_content = re.sub(r'\(\(([^cC]+)\)\)', lambda x: x.group(1).replace('c', '').replace('C', ''), md5_content)

    # Write the HTML output to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md5_content)

    # Exit with a successful status code
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_markdown_to_html(input_file, output_file)
