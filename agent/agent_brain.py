
"""
RuntimeQueens Agent Brain
Reasoning-only agent (Hackathon-Optimal)
"""

import os
import json
import re
from dotenv import load_dotenv

# Optional Gemini import
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# -------------------------------------------------
# ENV SETUP
# -------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


# -------------------------------------------------
# AGENT
# -------------------------------------------------

class BugAnalysisAgent:
    def __init__(self):
        print("🔧 Initializing RuntimeQueens Agent Brain...")

        self.model = None

        if GEMINI_AVAILABLE and API_KEY:
            try:
                genai.configure(api_key=API_KEY)
                self.model = genai.GenerativeModel("gemini-1.5-flash")
                print("✅ Gemini connected")
            except Exception as e:
                print(f"⚠️ Gemini init failed: {e}")
        else:
            print("⚠️ Gemini unavailable → fallback mode")

    # ---------------------------------------------

    def analyze_issue(self, issue_text):
        print("\n" + "=" * 70)
        print("🤖 RUNTIMEQUEENS – AGENT REASONING")
        print("=" * 70)

        print("\n🔍 Issue Summary:")
        print(issue_text.strip())

        reasoning = self._reason(issue_text)
        self._display(reasoning)
        self._save(reasoning)

        return reasoning

    # ---------------------------------------------

    def _reason(self, issue_text):
        if self.model:
            try:
                return self._call_gemini(issue_text)
            except Exception as e:
                print(f"⚠️ Gemini error: {e}")

        return self._fallback(issue_text)

    def _call_gemini(self, issue_text):
        prompt = f"""
Analyze this GitHub issue and return ONLY valid JSON.

Issue:
{issue_text}

Required JSON fields:
bug_summary
bug_type
root_cause_hypothesis
files_to_inspect
reproduction_plan
test_command
environment_hints
fix_strategy
priority
"""

        response = self.model.generate_content(prompt)
        text = response.text.strip()

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("Invalid Gemini output")

        return json.loads(match.group())

    # ---------------------------------------------

    def _fallback(self, issue_text):
        lower = issue_text.lower()
        test_cmd = "pytest" if "test" in lower else "python main.py"

        return {
            "bug_summary": "Likely missing dependency causing runtime failure",
            "bug_type": "dependency_issue",
            "root_cause_hypothesis": "Required package not installed",
            "files_to_inspect": ["requirements.txt", "README.md"],
            "reproduction_plan": [
                "Install dependencies",
                "Run test command in clean environment"
            ],
            "test_command": test_cmd,
            "environment_hints": "Python 3.x, clean virtual environment",
            "fix_strategy": "Add missing dependency to requirements.txt",
            "priority": "HIGH"
        }

    # ---------------------------------------------

    def _display(self, r):
        print("\n🧠 Agent Reasoning:")
        print("-" * 60)
        print("Bug Type:", r["bug_type"])
        print("Priority:", r["priority"])
        print("Summary:", r["bug_summary"])
        print("\nFiles to inspect:")
        for f in r["files_to_inspect"]:
            print(" •", f)
        print("\nTest Command:", r["test_command"])
        print("Fix Strategy:", r["fix_strategy"])
        print("-" * 60)

    def _save(self, data):
        with open("agent_output.json", "w") as f:
            json.dump(data, f, indent=2)
        print("\n💾 agent_output.json saved")


# -------------------------------------------------
# DEMO
# -------------------------------------------------

if __name__ == "__main__":
    issue_text = """
Tests fail on fresh installation

Error:
ModuleNotFoundError: No module named 'flask'
"""

    agent = BugAnalysisAgent()
    agent.analyze_issue(issue_text)
