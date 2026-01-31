import os
import subprocess
import shutil
import re

from agent.agent_brain import BugAnalysisAgent
from tools.mcp_actions import list_files

RUNTIME_REPO = "./runtime_repo"


def clone_repo(repo_url):
    if os.path.exists(RUNTIME_REPO):
        shutil.rmtree(RUNTIME_REPO)

    print(f"\n📥 Cloning repo: {repo_url}")
    subprocess.run(["git", "clone", repo_url, RUNTIME_REPO], check=True)


def run_docker_and_capture():
    print("\n🐳 Running Docker verification...\n")

    result = subprocess.run(
        [
            "docker", "run",
            "-v", f"{os.path.abspath(RUNTIME_REPO)}:/workspace",
            "rq-verifier"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    logs = result.stdout + "\n" + result.stderr
    return logs


def try_auto_fix(logs):
    """
    Very safe auto-fix:
    Only handles ModuleNotFoundError
    """
    match = re.search(r"No module named ['\"]([^'\"]+)['\"]", logs)
    if not match:
        return False

    missing_module = match.group(1)
    req_file = os.path.join(RUNTIME_REPO, "requirements.txt")

    if not os.path.exists(req_file):
        print("⚠️ No requirements.txt found → skipping auto-fix")
        return False

    print(f"\n🛠 Auto-fix triggered: adding '{missing_module}' to requirements.txt")

    with open(req_file, "a") as f:
        f.write(f"\n{missing_module}\n")

    return True


def main():
    print("\n🚀 RuntimeQueens Autonomous Bug Discovery Pipeline\n")

    repo_url = input("🔗 GitHub Repo URL: ").strip()

    # 1️⃣ Clone
    clone_repo(repo_url)

    # 2️⃣ Explore
    print("\n🧰 Exploring repository...\n")
    list_files(RUNTIME_REPO)

    # 3️⃣ First run
    logs = run_docker_and_capture()
    print("\n📄 Failure logs:\n")
    print(logs[:1500])

    # 4️⃣ Agent diagnosis
    agent = BugAnalysisAgent()
    analysis = agent.analyze_issue(logs)

    # 5️⃣ Auto-fix (once)
    fixed = try_auto_fix(logs)

    if fixed:
        print("\n🔁 Re-running Docker after auto-fix...\n")
        rerun_logs = run_docker_and_capture()
        print("\n📄 Re-run logs:\n")
        print(rerun_logs[:1500])

    print("\n✅ Pipeline complete")


if __name__ == "__main__":
    main()
