import os
import xlsxwriter
from datetime import datetime

COMMITS_FOLDER = 'git_commits_text_files'
OUTPUT_FILE = 'data/dataset.xlsx'

all_dates = []
all_authors = []
all_commits = []
all_messages = []
all_files_changed = []
all_insertions = []
all_deletions = []

def parse_commit_file(filepath):
    print(f"Processing: {os.path.basename(filepath)}")

    with open(filepath, 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()

    date = author = commit_id = None
    message_lines = []
    in_message = False
    current_files = '0'
    current_insertions = '0'
    current_deletions = '0'

    for line in lines:
        line = line.rstrip('\n')

        if not line.strip():
            continue

        first_char = line[0]

        if first_char == 'c' and line.startswith('commit '):
            if commit_id is not None:
                all_dates.append(date or '')
                all_authors.append(author or '')
                all_commits.append(commit_id)
                all_messages.append(' '.join(message_lines).strip())
                all_files_changed.append(current_files)
                all_insertions.append(current_insertions)
                all_deletions.append(current_deletions)

            commit_id = line.split(' ', 1)[1]
            date = author = None
            message_lines = []
            in_message = False
            current_files = current_insertions = current_deletions = '0'

        elif first_char == 'A' and line.startswith('Author:'):
            author = line.split(' ', 1)[1]

        elif first_char == 'D' and line.startswith('Date:'):
            date = line.split(' ', 1)[1].strip()

        elif line.startswith('    '):
            in_message = True
            message_lines.append(line.strip())

        elif first_char == ' ' and ',' in line and any(x in line.lower() for x in ['file', 'insertion', 'deletion']):
            parts = [p.strip() for p in line.split(',')]
            current_files = '0'
            current_insertions = '0'
            current_deletions = '0'

            for part in parts:
                if 'file' in part:
                    current_files = part.split()[0]
                elif 'insertion' in part:
                    current_insertions = part.split()[0]
                elif 'deletion' in part:
                    current_deletions = part.split()[0]

    if commit_id is not None:
        all_dates.append(date or '')
        all_authors.append(author or '')
        all_commits.append(commit_id)
        all_messages.append(' '.join(message_lines).strip())
        all_files_changed.append(current_files)
        all_insertions.append(current_insertions)
        all_deletions.append(current_deletions)


txt_files = [f for f in os.listdir(COMMITS_FOLDER) if f.endswith('.txt')]

for txt_file in txt_files:
    file_path = os.path.join(COMMITS_FOLDER, txt_file)
    parse_commit_file(file_path)

print(f"Total commits parsed: {len(all_commits)}")

# Create Excel file
print("Writing to dataset.xlsx...")
workbook = xlsxwriter.Workbook(OUTPUT_FILE)
worksheet = workbook.add_worksheet()

# Write headers
headers = ['DATE', 'AUTHOR', 'COMMIT', 'COMMIT MESSAGE', 'FILES CHANGED', 'INSERTIONS', 'DELETIONS']
for col, header in enumerate(headers):
    worksheet.write(0, col, header)

# Write data
for row_idx in range(len(all_commits)):
    worksheet.write(row_idx + 1, 0, all_dates[row_idx])
    worksheet.write(row_idx + 1, 1, all_authors[row_idx])
    worksheet.write(row_idx + 1, 2, all_commits[row_idx])
    worksheet.write(row_idx + 1, 3, all_messages[row_idx])

    # --- Convert these three to integers ---
    try:
        files_changed = int(all_files_changed[row_idx]) if all_files_changed[row_idx] else 0
    except (ValueError, TypeError):
        files_changed = 0

    try:
        insertions = int(all_insertions[row_idx]) if all_insertions[row_idx] else 0
    except (ValueError, TypeError):
        insertions = 0

    try:
        deletions = int(all_deletions[row_idx]) if all_deletions[row_idx] else 0
    except (ValueError, TypeError):
        deletions = 0

workbook.close()
print(f"Done! Saved {len(all_commits)} commits to '{OUTPUT_FILE}'")
