import sys, os, io
os.chdir("/Users/dongxingxi/physics_competition_thesis_excellent_v2/03_corpus")

old_stdout = sys.stdout
sys.stdout = captured = io.StringIO()
sys.argv = ["batch_text_check.py"]
exec(open("batch_text_check.py").read())
sys.stdout = old_stdout
output = captured.getvalue()

with open("/tmp/check_result.txt", "w") as f:
    f.write(output)

print(f"Total output: {len(output)} chars")
print()
for line in output.split('\n'):
    if '=> 结论:' in line:
        print(line.strip())
