def analyze_issue(issue_text):
    print("🔍 Reading GitHub issue...")
    print(f"Issue says: {issue_text}")

    print("🧠 I think the problem is related to environment or dependencies.")
    print("📂 I should look at files like:")
    print("- README.md")
    print("- requirements.txt")
    print("- Dockerfile")
    print("🧪 I should try running tests to reproduce the bug.")

if __name__ == "__main__":
    sample_issue = "Tests fail when running on Python 3.12"
    analyze_issue(sample_issue)
