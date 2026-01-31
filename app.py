import streamlit as st
import subprocess
import os
import shutil

st.set_page_config(
    page_title="RuntimeQueens",
    page_icon="🐞",
    layout="wide"
)

st.title("🐞 RuntimeQueens – Autonomous Bug Verification")
st.caption("Paste a GitHub repo. We verify failures in a clean environment.")

st.divider()

# -----------------------------
# UI INPUT
# -----------------------------

repo_url = st.text_input(
    "🔗 GitHub Repository URL",
    placeholder="https://github.com/owner/repo"
)

run_btn = st.button("🚀 Analyze Repository", type="primary")

output_placeholder = st.empty()

# -----------------------------
# PIPELINE RUNNER
# -----------------------------

def run_pipeline(repo_url):
    """
    Runs the existing CLI pipeline and captures output
    """
    process = subprocess.Popen(
        ["python", "run_pipeline.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Send repo URL to stdin
    process.stdin.write(repo_url + "\n")
    process.stdin.flush()

    logs = ""
    for line in process.stdout:
        logs += line
        yield logs

    process.wait()


# -----------------------------
# UI LOGIC
# -----------------------------

if run_btn:
    if not repo_url:
        st.warning("Please enter a GitHub repository URL.")
    else:
        with st.spinner("Running autonomous verification..."):
            log_box = st.code("", language="bash")

            for logs in run_pipeline(repo_url):
                log_box.code(logs[-4000:], language="bash")

        st.success("Pipeline complete ✅")

        # Display agent output if exists
        if os.path.exists("agent_output.json"):
            st.divider()
            st.subheader("🧠 Agent Diagnosis")

            import json
            with open("agent_output.json") as f:
                data = json.load(f)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Bug Type", data.get("bug_type", "N/A"))
                st.metric("Priority", data.get("priority", "N/A"))

            with col2:
                st.metric("Recommended Action", data.get("recommended_action", "N/A"))

            st.markdown("### 📝 Summary")
            st.write(data.get("bug_summary", "N/A"))

            st.markdown("### 🛠 Suggested Fix")
            st.write(data.get("fix_strategy", "N/A"))

        else:
            st.warning("No agent_output.json found.")
