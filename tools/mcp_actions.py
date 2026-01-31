import os

# Absolute path to repo root (parent of tools/)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def list_files(path=REPO_ROOT):
    print(f"📂 Listing files in {path}")
    try:
        for f in os.listdir(path):
            print(" -", f)
    except Exception as e:
        print("Error listing files:", e)

def read_file(filename):
    print(f"\n📄 Reading file: {filename}")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("File not found")

def run_command(cmd):
    print(f"\n▶️ Running command: {cmd}")
    print("(command execution simulated)")
    print("✔️ Command completed")

if __name__ == "__main__":
    print("🤖 MCP Tool Actions Starting...\n")

    list_files()  # 👈 NO ".." anymore
    read_file(os.path.join(REPO_ROOT, "README.md"))
    run_command("pytest")

    print("\n🤖 MCP Tool Actions Finished")
