# RuntimeQueens Agent

## Problem
Fixing GitHub bugs is slow because developers must first:
- understand the issue
- find relevant files
- set up environments
- reproduce the bug

## Our Solution
An AI agent that:
1. Reads a GitHub issue
2. Explains what it thinks is wrong
3. Explores the repository using tools (MCP-style)
4. Reproduces the bug in a clean Docker environment
5. Verifies behavior before and after a fix

## Demo Flow
1. Paste a GitHub issue
2. Run the agent → show reasoning
3. Show file exploration logs
4. Run Docker → reproduce bug
5. Explain verification
