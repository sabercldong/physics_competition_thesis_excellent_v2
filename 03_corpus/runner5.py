import sys, os, io
os.chdir("/Users/dongxingxi/physics_competition_thesis_excellent_v2/03_corpus")

# Capture output
old_stdout = sys.stdout
sys.stdout = captured = io.StringIO()

sys.argv = ["batch_text_check.py"]
exec(open("batch_text_check.py").read())

sys.stdout = old_stdout
output = captured.getvalue()

# Save to file
with open("/tmp/check_result.txt", "w") as f:
    f.write(output)

# Print key summary lines
for line in output.split('\n'):
    if any(kw in line for kw in ['汇总报告', '通过无需修订', '需修订', '待核实', '总CSV', '总PASS', 'Material', '---', '====', '===']):
        print(line)

# Also print conclusion lines for each material
for line in output.split('\n'):
    if '=> 结论:' in line:
        print(line.strip())
