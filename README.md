# God Variable (GV) — The Hub

God Variable (GV) is a proposed scalar framework modeling **constraint strain and survivability dynamics** across engineered and physical systems.

GV operates at two layers:

1. **Operational Layer** — AI safety, CI enforcement, runtime monitoring  
2. **Theoretical Layer** — constraint-driven dynamics in cosmology and field theory  

This repository is the one-click hub for the entire ecosystem.

---

## Start Here (2 minutes)

### 1) See GV detect drift before tests fail (fastest proof)
➡️ **GV Drift Demo**  
https://github.com/willshacklett/gv-drift-demo

### 2) Install survivability-aware CI scoring (real pipeline value)
➡️ **GodScore CI (GitHub Action)**  
https://github.com/willshacklett/godscore-ci

### 3) Monitor live runtime strain in agent systems
➡️ **GvAI Safety Systems**  
https://github.com/willshacklett/gvai-safety-systems

---

## One-Click: Run the Ecosystem in Codespaces

1) Click **Code → Codespaces → Create codespace on main**  
2) Run:

```bash
make demo
```

---

## The Ecosystem Map

| Repo | What it is | Why it matters |
|------|------------|----------------|
| **gv-drift-demo** | Minimal proof: GV flags drift early | Shows value in minutes |
| **godscore-ci** | CI trust score + optional enforcement | Turns GV into a real gate |
| **gvai-safety-systems** | Runtime monitoring for AI/agents | GV in production contexts |
| **gv-engine** | Core scoring / signal primitives | Shared logic layer |
| **gv-watchdog** | CLI guardrail tool | Operational adoption |
| **cft-cancer-sim** | Bio simulation direction | Cross-domain survivability |

---

## Quantitative Program

To elevate GV from conceptual unification to predictive framework:

### 1. Define GV flow equation

∂ₜ GV = −∇·J_GV + S(GV)

Where:
- J_GV encodes constraint-gradient transport
- S(GV) captures curvature-driven source dynamics

---

### 2. Embed in FLRW Cosmology

H² = (8πG / 3) ρ_eff(GV)

Test:
- w(z)
- Λ(z)
- Structure growth

---

### 3. Quantum Field Embedding

Derive GV-modified EFT:

- Higgs loop corrections
- UV → IR suppression factor
- Strong CP θ-dynamics under gradient relaxation

---

### 4. Black Hole Sector

Derive:
- Horizon GV saturation condition
- Entropy scaling from bounded gradients
- Evaporation spectrum vs Hawking

---

### 5. Inflation / Early Universe

Compute:
- Spectral tilt n_s
- Tensor-to-scalar ratio r
- Non-Gaussianity f_NL

---

## GV Experiment 001: upstream inference

The repository now includes a small one-dimensional upstream-inference experiment in [src/gv_experiment_001.py](src/gv_experiment_001.py). The workflow is:

1. generate several Gaussian source pulses,
2. evolve them with an advection-diffusion forward model,
3. observe the downstream state,
4. reconstruct the hidden source with a regularized inverse filter,
5. report reconstruction error, Pearson correlation, correlation retention, and a spectral information-loss score.

This experiment is a toy linear inverse problem for benchmarking reconstruction behavior under controlled assumptions. It is not evidence for a cosmological claim and should not be interpreted as such.

### Reconstruction conditions

- Oracle: reconstruction uses the true forward model and therefore provides an upper-bound reference.
- Model mismatch: reconstruction uses a deliberately incorrect forward model to test sensitivity to model error.
- Blind inference: the source is reconstructed while the forward parameters are jointly inferred from the observation with a bounded search over plausible values.
- Baseline: a simple shift-based reconstruction that serves as a naive non-invertive baseline.

### Metric definitions

- RMSE: $\mathrm{RMSE}(s, \hat{s}) = \sqrt{\frac{1}{N}\sum_i (s_i - \hat{s}_i)^2}$
- Correlation: the Pearson correlation coefficient between the true source and the reconstruction.
- Correlation retention: $r^2$, where $r$ is the Pearson correlation coefficient between source and reconstruction.
- Spectral information retention: a normalized spectral-entropy similarity score between the source and the reconstruction, defined as $1 - |H_\mathrm{norm}(s) - H_\mathrm{norm}(\hat{s})|$, where $H_\mathrm{norm}(x)$ is the Shannon entropy of the normalized power spectrum of $x$ divided by $\log N$.
- Spectral information loss: its complement, $1 - \mathrm{spectral\_information\_retention}$.

The experiment can be run via:

```bash
python - <<'PY'
from src.gv_experiment_001 import run_experiment, run_sensitivity_analysis
run_experiment(output_dir='outputs', save_plots=True)
run_sensitivity_analysis(output_dir='outputs', save_plots=True)
PY
```

## Theory (Preserved)

The full theoretical foundation has been preserved verbatim and moved here:

➡️ **THEORY.md**

---

## Coherence Eternal ⭐

If a system must run longer than its designers,  
it needs constraints that outlive intent.

---

## License

MIT (unless otherwise specified per-repo)
