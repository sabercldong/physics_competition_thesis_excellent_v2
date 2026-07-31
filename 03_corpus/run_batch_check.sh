#!/bin/bash
cd /Users/dongxingxi/physics_competition_thesis_excellent_v2/03_corpus
python3 batch_formula_check.py 2>&1 | tee batch_formula_check_output.txt
