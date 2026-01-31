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

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


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

    def analyze_issue(self, issue_text):
        print("\n🤖 AGENT REASONING STARTED\n")
        reasoning = self._reason(issue_text)
        self._display(reasoning)

        with open("agent_output.json", "w") as f:
            json.dump(reasoning, f, indent=2)

        print("\n💾 agent_output.json saved")
        return reasoning

    def _reason(self, issue_text):
        if self.model:
            try:
                return self._call_gemini(issue_text)
            except Exception as e:
                print("⚠️ Gemini error:", e)

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
recommended_action
"""

        response = self.model.generate_content(prompt)
        text = response.text.strip()

        match = re.search(r"\{{.*\}}", text, re.DOTALL)
        if not match:
            raise ValueError("Invalid Gemini output")

        return json.loads(match.group())

    def _fallback(self, issue_text):
        return {
            "bug_summary": "Tests fail due to missing dependency in clean environment",
            "bug_type": "dependency_issue",
            "root_cause_hypothesis": "Dependency installed locally but missing in clean env",
            "files_to_inspect": ["requirements.txt", "setup.py", "README.md"],
            "reproduction_plan": [
                "Run tests in clean container"
            ],
            "test_command": "pytest",
            "environment_hints": "Python 3.x, no extra packages",
            "fix_strategy": "Add missing dependency to requirements.txt",
            "priority": "HIGH",
            "recommended_action": "dependency_fix"
        }

    def _display(self, r):
        print("-" * 70)
        print("Bug Type:", r["bug_type"])
        print("Priority:", r["priority"])
        print("Summary:", r["bug_summary"])
        print("Fix Strategy:", r["fix_strategy"])
        print("-" * 70)
