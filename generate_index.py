#!/usr/bin/env python3
"""
Generate a clean landing page for index.md.
Blog posts are available at /writing/ via the MkDocs blog plugin.
"""

def generate_index():
    index_content = """![Prabha Arivalagan](https://avatars.githubusercontent.com/u/3776681){ .homepage-avatar }

# Prabha Arivalagan

AI Engineer building with agents, LLMs, and cloud infrastructure.

[GitHub](https://github.com/prabha-git) · [Twitter](https://twitter.com/prabhatweet) · [Medium](https://medium.com/@prabhakaran_arivalagan){ .homepage-social }

---

[Read my blog →](/writing/){ .md-button .md-button--primary }

---

## Contact

- Email: prabhakaran.mails@gmail.com
- [Github](https://github.com/prabha-git)
- [Medium Blog](https://medium.com/@prabhakaran_arivalagan)
- [x / Twitter](https://twitter.com/prabhatweet)
"""

    with open('docs/index.md', 'w', encoding='utf-8') as f:
        f.write(index_content)

    print("Generated clean landing page index.md")

if __name__ == '__main__':
    generate_index()
