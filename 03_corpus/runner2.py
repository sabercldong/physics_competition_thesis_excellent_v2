import sys, subprocess, os

os.chdir("/Users/dongxingxi/physics_competition_thesis_excellent_v2/03_corpus")
result = subprocess.run(
    [sys.executable, "batch_text_check.py"],
    capture_output=True, text=True, timeout=600
)
with open("/tmp/check_result.txt", "w") as f:
    f.write("STDOUT:\n" + result.stdout)
    f.write("\n\nSTDERR:\n" + result.stderr)
    f.write(f"\n\nRC: {result.returncode}")
print("Done. Results saved to /tmp/check_result.txt")
print(f"Output size: {len(result.stdout)} chars, {len(result.stderr)} stderr chars")
