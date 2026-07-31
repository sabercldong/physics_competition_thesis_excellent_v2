#!/usr/bin/env python3
import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
r = subprocess.run([sys.executable, "-u", "/Users/dongxingxi/physics_competition_thesis_excellent_v2/03_corpus/manual_review_transcripts/test_api.py"], capture_output=True, text=True)
print(r.stdout)
if r.stderr:
    print("STDERR:", r.stderr[:500])
