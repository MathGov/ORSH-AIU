# Data map

All paths below are relative to `publication/`. Original file hashes appear in
`provenance/source-inventory.json`; data is retained as supplied, not regenerated
silently for publication. The protocols and source code define the observables.

| Location | Contents | Use and limits |
|---|---|---|
| `pilot/config.json` | Original configuration and master seed | Defines the source-off pilot; preserve the accompanying pre-execution receipt |
| `data/pilot_run/model_inputs.json` | Retained sampled inputs | Reconstruct the delivered pilot models |
| `data/pilot_run/per_unit.json`, `per_unit_summary.csv` | Unit-level measures | Respect pairing and independent model-unit counts |
| `data/pilot_run/results.json` | Pilot summaries and intervals | Original primary estimand, not the later factorial contrast |
| `data/pilot_run/trajectories_n4.npz`, `trajectories_n6.npz` | Retained pilot trajectory arrays | Inspect keys/shapes before analysis; do not assume raw quantum states are included |
| `data/reviewer_replay/` | Reimplementation, factorial and neutral-control arrays and receipts | Same-project, model-assisted review evidence, not independent-team replication |
| `data/factorial_analysis/` | Cell summaries and finite-family intervals | Recomputed from retained factorial arrays by `analyze_factorial.py` |
| `data/review_additions/` | Sign tests, transport checks and initial-floor diagnostics | Secondary analyses; distinguish them from the predeclared primary |
| `figures/` | Supplied PNG and SVG figures | Prefer SVG for scaling; cite the associated work and version |

Read compressed NumPy arrays without pickle execution:

```python
from pathlib import Path
import numpy as np
path = Path('publication/data/reviewer_replay/factorial_n6.npz')
with np.load(path, allow_pickle=False) as archive:
    for key in archive.files:
        print(key, archive[key].shape, archive[key].dtype)
    print(archive['columns'])
```

Column-labelled factorial matrices contain per-unit observables, not all
time-resolved quantum states. Use the accompanying analysis code for the exact
initial/post-window conventions and the injection/dynamics pairing. Do not treat
multiple arms or time points as independent experimental units.
