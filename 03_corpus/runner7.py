import sys, os

root = "/Users/dongxingxi/physics_competition_thesis_excellent_v2/03_corpus"
os.chdir(root)
sys.path.insert(0, root)

# Import and run main directly
import importlib.util
spec = importlib.util.spec_from_file_location("checker", os.path.join(root, "batch_text_check.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
results = mod.main()

print("\n=== SUMMARY ===")
for mid, r in results.items():
    print(f"{mid}: {r['status']} (PASS={r['pass']}, REV={r['needs']}, UNC={r['uncertain']})")
