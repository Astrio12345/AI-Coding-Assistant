from pathlib import Path

FILES = [
    "app/__init__.py",
    "app/main.py",
    "app/llm.py",
    "templates/index.html",
    "static/style.css",
    "static/script.js",
    "requirements.txt",
    ".env",
    ".gitignore",
]

for f in FILES:
    p = Path(f)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.touch(exist_ok=True)
    print(f"Created {f}")

print("\nDone! Now paste the code into each file.")