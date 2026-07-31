import subprocess
result = subprocess.run(
    ["python3", "batch_text_check.py"],
    cwd="/Users/dongxingxi/physics_competition_thesis_excellent_v2/03_corpus",
    capture_output=True, text=True, timeout=600
)
with open("/tmp/check_result.txt", "w") as f:
    f.write("STDOUT:\n" + result.stdout)
    f.write("\n\nSTDERR:\n" + result.stderr)
    f.write(f"\n\nRC: {result.returncode}")
print("Done. Output written to /tmp/check_result.txt")
print(f"Stdout size: {len(result.stdout)} bytes")
print(f"Stderr size: {len(result.stderr)} bytes")
