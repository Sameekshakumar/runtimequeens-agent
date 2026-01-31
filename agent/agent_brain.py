import os
import json
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


class BugAnalysisAgent:
    def __init__(self):
        print("🔧 Initializing RuntimeQueens Agent Brain...")
        self.client = None

        if not API_KEY:
            print("⚠️ GEMINI_API_KEY not set → fallback mode")
            return

        try:
            self.client = genai.Client(api_key=API_KEY)
            print("✅ Gemini connected (google.genai)")
        except Exception as e:
            print("⚠️ Gemini init failed:", e)

    # --------------------------------------------------

    def analyze_logs(self, logs: str):
        if self.client:
            try:
                return self._ai_reason(logs)
            except Exception as e:
                print("⚠️ Gemini reasoning failed:", e)

        return self._fallback_reason(logs)

    # --------------------------------------------------

    def _ai_reason(self, logs: str):
        prompt = f"""
You are a senior software reliability engineer.

Analyze the execution logs and return ONLY valid JSON with these fields:
bug_type
summary
root_cause
human_explanation
confidence
recommended_action

Execution logs:
{logs}
"""

        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        text = response.text.strip()
        match = re.search(r"\{{.*\}}", text, re.DOTALL)

        if not match:
            raise ValueError("Invalid Gemini output")

        return json.loads(match.group())

    # --------------------------------------------------

    def _fallback_reason(self, logs: str):
        logs_lower = logs.lower()

        if "no tests ran" in logs_lower or "collected 0 items" in logs_lower:
            return {
                "bug_type": "no_tests_detected",
                "summary": "No tests were found in the repository",
                "root_cause": "Repository is documentation or example-based",
                "human_explanation": (
                    "This project does not define automated tests, "
                    "so there is nothing to verify in a clean environment."
                ),
                "confidence": 0.95,
                "recommended_action": "skip_verification"
            }

        if "modulenotfounderror" in logs_lower:
            return {
                "bug_type": "packaging_or_dependency_issue",
                "summary": "Tests failed due to missing module",
                "root_cause": "Local package is not installable in a clean environment",
                "human_explanation": (
                    "The tests assume a local module is available, "
                    "but the project is not packaged or installed correctly. "
                    "This works locally but fails in clean environments."
                ),
                "confidence": 0.9,
                "recommended_action": "make_package_installable"
            }

        if "failed" in logs_lower or "assert" in logs_lower:
            return {
                "bug_type": "test_failure",
                "summary": "One or more tests failed",
                "root_cause": "Bug detected by failing assertions",
                "human_explanation": (
                    "The tests executed successfully but reported failures, "
                    "indicating incorrect logic or unexpected behavior in the code."
                ),
                "confidence": 0.85,
                "recommended_action": "inspect_failing_tests"
            }

        return {
            "bug_type": "no_failure_detected",
            "summary": "Execution completed successfully",
            "root_cause": "No issues detected",
            "human_explanation": (
                "The project ran successfully in a clean environment, "
                "and no errors were detected."
            ),
            "confidence": 0.99,
            "recommended_action": "none"
        }
