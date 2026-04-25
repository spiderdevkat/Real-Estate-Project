with open("scraper.py", "r", encoding="utf-8") as f:
    content = f.read()

count = content.count("upload_to_s3")
print(f"upload_to_s3 appears {count} times\n")

# Show all line numbers
for i, line in enumerate(content.split("\n"), 1):
    if "upload_to_s3" in line:
        print(f"  Line {i}: {line.strip()}")