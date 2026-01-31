# This script simulates a bug where a required dependency is missing
import sys

print("--- RUNTIME QUEENS BUG REPRODUCER ---")
try:
    import colorama
    print("SUCCESS: Dependency 'colorama' found.")
except ImportError:
    print("FAILED: Critical dependency 'colorama' is missing from the environment!")
    sys.exit(1) # This tells Docker the run failed