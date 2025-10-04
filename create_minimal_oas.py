#!/usr/bin/env python3
"""
Create a minimal OpenAPI spec by keeping only essential operations
"""

# Key sections to keep (line numbers from original file)
essential_sections = [
    # Keep header (1-90)
    (1, 90),

    # Keep tickets section (approximately lines 2000-5000)
    (2000, 5000),

    # Keep users section (approximately lines 14000-16000)
    (14000, 16000),

    # Keep organizations section (approximately lines 7000-9000)
    (7000, 9000),

    # Keep components section (from line 15000 to end, but truncated)
    (15000, 25000),
]

def extract_sections():
    with open('oas-backup.yaml', 'r') as f:
        lines = f.readlines()

    extracted_lines = []

    for start, end in essential_sections:
        if start <= len(lines):
            actual_end = min(end, len(lines))
            extracted_lines.extend(lines[start-1:actual_end])
            extracted_lines.append('\n')  # Add separator

    # Write minimal version
    with open('oas-minimal.yaml', 'w') as f:
        f.writelines(extracted_lines)

    print(f"Created minimal OpenAPI spec with {len(extracted_lines)} lines")

if __name__ == '__main__':
    extract_sections()