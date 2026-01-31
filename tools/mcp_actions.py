import os
import subprocess

def list_repo_files(repo_path):
    return os.listdir(repo_path)

def read_file(repo_path, filename):
    path = os.path.join(repo_path, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def run_command(repo_path, command):
    result = subprocess.run(
        command,
        shell=True,
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr
