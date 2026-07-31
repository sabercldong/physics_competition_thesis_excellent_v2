import subprocess, sys
result = subprocess.run(["python3", "batch_text_check.py"], cwd="/Users/dongxingxi/physics_competition_thesis_excellent_v2/03_corpus", capture_output=True, text=True, timeout=300)
print("STDOUT:", result.stdout[-10000:] if len(result.stdout) > 10000 else result.stdout)
print("STDERR:", result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr)
print("RC:", result.returncode)
