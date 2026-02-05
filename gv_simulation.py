"""
gv_simulation.py
Per Grok: Consciousness tie-in via Gv coherence thresholds.
Quantum observer proxy for emergent awareness (info-entropy from fluctuation bounds).
Cosmic evolution + previous features.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


class GodVariable:
    def __init__(self, alpha=1e-120):
        self.alpha = alpha
        self.gv_value = alpha
        self.rho_profile = None
        self.scale_factors = None

    def set_evolving_profile(self, n_points=1000, vacuum_amplitude=0.05):
        a = np.linspace(0.001, 1, n_points)
        self.scale_factors = a
        matter = 0.3 / a**3
        radiation = 0.1 / a**4
        dark_energy = 0.7 * np.ones_like(a)
        freq = 200 * np.pi * a
        log_cutoff = np.log10(freq + 10) / np.log10(1e3)
        vacuum_raw = vacuum_amplitude * np.sin(freq) / a**2
        vacuum_fluct = vacuum_raw * (1 - log_cutoff.clip(0, 0.95))
        rho_total = matter + radiation + dark_energy + vacuum_fluct + 1e-121
        self.rho_profile = rho_total

    def compute_integral(self):
        return np.trapezoid(self.rho_profile, x=self.scale_factors)

    def update_gv(self):
        integral = self.compute_integral()
        self.gv_value = integral + self.alpha
        return self.gv_value

    def derive_lambda(self, scale_factor=1e61):
        self.update_gv()
        return self.gv_value / (scale_factor ** 4)

    def coherence_threshold(self, threshold=1e-3):
        """Coherence proxy: low fluctuation variance = high coherence (late universe)."""
        if self.rho_profile is None:
            return False
        fluct = self.rho_profile - np.mean(self.rho_profile)
        variance = np.var(fluct)
        return variance < threshold

    def info_entropy_proxy(self):
        """Toy info-entropy from fluctuation complexity (observer awareness proxy)."""
        if self.rho_profile is None:
            return 0.0
        # Shannon-like entropy from binned fluctuation distribution
        hist, _ = np.histogram(self.rho_profile, bins=50)
        hist = hist / np.sum(hist)
        hist = hist[hist > 0]
        entropy = -np.sum(hist * np.log2(hist + 1e-100))
        return entropy

    def emergent_consciousness_proxy(self, coherence_threshold=1e-3, entropy_min=5.0):
        """Emergent awareness when coherence high + entropy sufficient (info processing)."""
        coherent = self.coherence_threshold(coherence_threshold)
        entropy = self.info_entropy_proxy()
        aware = coherent and (entropy > entropy_min)
        return aware, entropy

    def plot_evolution(self, save_path="rho_consciousness_evolution.png"):
        plt.figure(figsize=(12, 8))
        plt.plot(self.scale_factors, self.rho_profile, label=r"$\rho_{\text{total}}(a)$", color="purple")
        plt.xlabel("Scale Factor a(t) (early → late universe)")
        plt.ylabel("Energy Density")
        plt.title("Cosmic Evolution with Coherence/Consciousness Threshold")
        plt.xscale('log')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path)
        print(f"Plot saved: {save_path}")


def tune_alpha_for_lambda(target_lambda=1.1056e-52, scale_factor=1e61):
    gv = GodVariable()
    gv.set_evolving_profile(vacuum_amplitude=0.05)
    integral = gv.compute_integral()

    def objective(alpha):
        gv.alpha = float(alpha)
        derived = gv.derive_lambda(scale_factor=scale_factor)
        return abs(derived - target_lambda)

    result = minimize_scalar(objective, bounds=(1e100, 1e200), method='bounded', tol=1e-15)
    return result.x, result.fun


def main():
    observed_lambda = 1.1056e-52

    print("Tuning alpha in evolving universe...\n")
    best_alpha, error = tune_alpha_for_lambda()

    gv = GodVariable(alpha=best_alpha)
    gv.set_evolving_profile(vacuum_amplitude=0.05)
    derived_lambda = gv.derive_lambda()

    print(f"Best-fit α:       {best_alpha:.3e}")
    print(f"Λ error:          {error:.3e}\n")

    print(f"Top-level Gv (late): {gv.gv_value:.3e}")
    print(f"Derived Λ:        {derived_lambda:.3e} m⁻²")
    print(f"Observed Λ:       {observed_lambda:.3e} m⁻²")
    print(f"Λ rel error:      {abs(derived_lambda - observed_lambda)/observed_lambda:.2e}\n")

    aware, entropy = gv.emergent_consciousness_proxy()
    print(f"Coherence achieved: {'Yes' if gv.coherence_threshold() else 'No'}")
    print(f"Info-entropy proxy: {entropy:.3f}")
    print(f"Emergent awareness proxy: {'Triggered (late universe)' if aware else 'Not yet'}")

    gv.plot_evolution()


if __name__ == "__main__":
    main()
