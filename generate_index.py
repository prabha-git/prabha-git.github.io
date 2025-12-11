#!/usr/bin/env python3
"""
Generate index.md with the latest 5 blog posts.
This script scans all posts in docs/writing/posts/ and creates a homepage
with the most recent posts including title, date, tags, and excerpt.
"""

import os
import glob
import re
import yaml
from datetime import datetime, date

def extract_frontmatter_and_content(file_path):
    """Extract YAML frontmatter and content from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match frontmatter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        return None, content

    frontmatter_text = match.group(1)
    markdown_content = match.group(2)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return None, markdown_content

    return frontmatter, markdown_content

def extract_excerpt(content, max_length=200):
    """Extract an excerpt from markdown content."""
    # Remove markdown headers
    content = re.sub(r'^#+\s+.*$', '', content, flags=re.MULTILINE)
    # Remove markdown links but keep text
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
    # Remove markdown formatting
    content = re.sub(r'[*_`]', '', content)
    # Remove extra whitespace
    content = re.sub(r'\s+', ' ', content).strip()

    # Get first meaningful content
    if len(content) > max_length:
        content = content[:max_length].rsplit(' ', 1)[0] + '...'

    return content

def parse_date(date_value):
    """Parse date from various formats to datetime object."""
    if isinstance(date_value, datetime):
        return date_value
    if isinstance(date_value, date):
        # Convert date to datetime for consistent handling
        return datetime.combine(date_value, datetime.min.time())
    if isinstance(date_value, str):
        try:
            return datetime.strptime(date_value, '%Y-%m-%d')
        except ValueError:
            pass
    return None

def format_date(date_obj):
    """Format datetime object to readable string."""
    if date_obj:
        return date_obj.strftime('%B %d, %Y')
    return ''

def generate_post_url(date_obj, slug):
    """Generate URL for a blog post based on date and slug."""
    if date_obj and slug:
        return f"/writing/{date_obj.year}/{date_obj.month:02d}/{date_obj.day:02d}/{slug}/"
    return "/writing/"

def generate_index():
    """Generate the index.md file with the latest 5 blog posts."""
    posts_dir = 'docs/writing/posts'
    post_files = glob.glob(f'{posts_dir}/*.md')

    posts = []
    for file_path in post_files:
        frontmatter, content = extract_frontmatter_and_content(file_path)
        if not frontmatter:
            continue  # Skip posts without frontmatter

        # Skip drafts
        if frontmatter.get('draft') is True:
            continue

        # Extract metadata
        date_obj = parse_date(frontmatter.get('date'))
        slug = frontmatter.get('slug', '')
        tags = frontmatter.get('tags', [])

        # Try to get title from content (first # header)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else os.path.basename(file_path).replace('.md', '')

        # Get excerpt
        excerpt = extract_excerpt(content, max_length=180)

        posts.append({
            'title': title,
            'date': date_obj,
            'slug': slug,
            'tags': tags,
            'excerpt': excerpt,
        })

    # Sort by date (newest first), handling None dates
    posts.sort(key=lambda x: x['date'] if x['date'] else datetime.min, reverse=True)

    # Take top 5
    recent_posts = posts[:5]

    # Generate index.md content
    index_content = """# Prabha Arivalagan

AI Engineer writing about agents, LLMs, and cloud infrastructure

## Recent Writing

"""

    for post in recent_posts:
        date_str = format_date(post['date'])
        tags_str = ', '.join(post['tags']) if post['tags'] else ''
        post_url = generate_post_url(post['date'], post['slug'])

        # Post title (linked)
        index_content += f"### [{post['title']}]({post_url})\n"

        # Date and tags
        index_content += f"**{date_str}**"
        if tags_str:
            index_content += f" • {tags_str}"
        index_content += "\n\n"

        # Excerpt
        if post['excerpt']:
            index_content += f"{post['excerpt']}\n\n"

        # Read more link
        index_content += f"[Read more →]({post_url})\n\n"

        # Add visual separator between posts
        index_content += "---\n\n"

    # Footer with link to all posts and contact info
    index_content += """
[View all posts →](/writing/)

## Contact

- Email: prabhakaran.mails@gmail.com
- [Github](https://github.com/prabha-git)
- [Medium Blog](https://medium.com/@prabhakaran_arivalagan)
- [x / Twitter](https://twitter.com/prabhatweet)
"""

    # Write to docs/index.md
    with open('docs/index.md', 'w', encoding='utf-8') as f:
        f.write(index_content)

    print(f"✅ Generated index.md with {len(recent_posts)} recent posts")
    for post in recent_posts:
        print(f"   - {post['title']} ({format_date(post['date'])})")

if __name__ == '__main__':
    generate_index()
