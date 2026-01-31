```
import os

def list_files(repo_path):
    print(f"📂 Listing files in {repo_path}")
    try:
        for f in os.listdir(repo_path):
            print(" -", f)
    except Exception as e:
        print("Error listing files:", e)

def read_file(repo_path, filename):
    path = os.path.join(repo_path, filename)
    print(f"\n📄 Reading file: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("File not found")

def run_command(cmd):
    print(f"\n▶️ Running command: {cmd}")
    print("(command execution simulated)")
    print("✔️ Command completed")

if __name__ == "__main__":
    print("🤖 MCP Tool Actions Starting...\n")

    # Controlled input (for demo)
    TARGET_REPO = "./target_repo"

    list_files(TARGET_REPO)
    read_file(TARGET_REPO, "README.md")
    run_command("pytest")

    print("\n🤖 MCP Tool Actions Finished")

```