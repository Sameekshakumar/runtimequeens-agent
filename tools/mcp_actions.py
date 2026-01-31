import os

def list_files(repo_path):
    print(f"\n📂 Listing files in {repo_path}")
    try:
        for f in os.listdir(repo_path):
            print(" -", f)
    except Exception as e:
        print("Error:", e)

def read_file(repo_path, filename):
    path = os.path.join(repo_path, filename)
    print(f"\n📄 Reading {filename}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            print(f.read()[:800])
    except FileNotFoundError:
        print("File not found")
