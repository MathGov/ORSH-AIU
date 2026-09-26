# Claude review of ORSH/AIU v1.7 core files

- FEEDBACK_v1_7.md: the full assessment (same content as the chat reply).
- reimpl_id1.py: independent reimplementation of the P01-ID1 source-off pilot from the P01 v1.2 protocol text (not GPT's code). Runs 5 x 96-unit replicates at n = 4 and 6, 60,000 units at n = 6 and 2,000 at n = 8 (about 7.5 minutes).
- factorial_id1.py: the 2x2 control (injection frame x frame in which the internal Hamiltonian is local), 20,000 paired units at n = 4 and 6 and 1,000 at n = 8 (about 5 minutes).
- factorial_neutral.py: adds a neutral third-frame dynamics comparator (n = 6, 6,000 units, about 1.5 minutes).
- PREDICTIONS_*.md with .sha256 files: predictions written and hashed before each run. The factorial prediction (locality effect near zero) was wrong, and is reported as wrong.
- *_stdout.txt and *.json: outputs as produced here; environment.txt lists versions.

Run with OPENBLAS_NUM_THREADS=1 from this folder: python3 reimpl_id1.py; python3 factorial_id1.py; python3 factorial_neutral.py
