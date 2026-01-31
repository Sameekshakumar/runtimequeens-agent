import subprocess
import tempfile
import shutil
import json
import os

from agent.agent_brain import BugAnalysisAgent

print("\n🚀 RuntimeQueens Autonomous Bug Pipeline\n")

repo_url = input("🔗 GitHub Repo URL: ").strip()
if not repo_url:
    print("❌ Repo URL required")
    exit(1)

tmp_dir = tempfile.mkdtemp(prefix="rq_repo_")

try:
    print("\n📥 Cloning repository...")
    subprocess.run(["git", "clone", repo_url, tmp_dir], check=True)

    print("\n🐳 Running in clean Docker environment...")
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{tmp_dir}:/workspace",
        "rq-verifier"
    ]

    proc = subprocess.run(
        docker_cmd,
        capture_output=True,
        text=True
    )

    logs = proc.stdout + proc.stderr
    print("\n📄 Execution Logs:\n")
    print(logs)

    agent = BugAnalysisAgent()
    analysis = agent.analyze_logs(logs)

    with open("agent_output.json", "w") as f:
        json.dump(analysis, f, indent=2)

    print("\n🧠 Agent Verdict")
    print(json.dumps(analysis, indent=2))

    print("\n✅ Pipeline complete")

finally:
    shutil.rmtree(tmp_dir, ignore_errors=True)
