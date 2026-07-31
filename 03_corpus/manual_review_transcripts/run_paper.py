#!/usr/bin/env python3
"""Run only the paper page analysis."""
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

result = subprocess.run([sys.executable, "/Users/dongxingxi/physics_competition_thesis_excellent_v2/03_corpus/manual_review_transcripts/vl_paper_only.py"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:500])
