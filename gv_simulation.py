"""
gv_simulation.py
Per Grok: Refine H0 tension with CMB/supernovae proxy data into Gv growth rate.
Early tight (CMB-like), late loose (SNe-like) → toy tension.
Consciousness coherence + previous features.
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

    def derive_h0_proxy(self, regime='late'):
        """Toy H0 from Gv growth rate da/dt proxy."""
        self.update_gv()
        a = self.scale_factors
        # Numerical dGv/da
        gv_over_a = np.interp(a, a, np.cumsum(self.rho_profile) * np.diff(a, prepend=0) + self.alpha)  # Approx cumulative
        dGv_da = np.gradient(gv_over_a, a)
        if regime == 'early':
            h0_early = np.mean(dGv_da[a < 0.01]) * 74  # CMB-like tight, higher H0 proxy
            return h0_early
        else:
            h0_late = np.mean(dGv_da[a > 0.5]) * 68   # SNe-like, lower H0 proxy
            return h0_late

    def h0_tension_proxy(self):
        h0_early = self.derive_h0_proxy('early')
        h0_late = self.derive_h0_proxy('late')
        tension_sigma = abs(h0_early - h0_late) / 2  # Toy ~5σ tension proxy
        return h0_early, h0_late, tension_sigma

    def coherence_threshold(self, threshold=1e-3):
        fluct = self.rho_profile - np.mean(self.rho_profile)
        variance = np.var(fluct)
        return variance < threshold

    def info_entropy_proxy(self):
        hist, _ = np.histogram(self.rho_profile, bins=50)
        hist = hist / np.sum(hist)
        hist = hist[hist > 0]
        entropy = -np.sum(hist * np.log2(hist + 1e-100))
        return entropy

    def emergent_consciousness_proxy(self, coherence_threshold=1e-3, entropy_min=5.0):
        coherent = self.coherence_threshold(coherence_threshold)
        entropy = self.info_entropy_proxy()
        aware = coherent and (entropy > entropy_min)
        return aware, entropy

    def plot_evolution(self, save_path="rho_h0_tension.png"):
        plt.figure(figsize=(12, 8))
        plt.plot(self.scale_factors, self.rho_profile, label=r"$\rho_{\text{total}}(a)$", color="purple")
        plt.axvline(0.01, color='red', linestyle='--', label="Early (CMB proxy)")
        plt.axvline(0.5, color='blue', linestyle='--', label="Late (SNe proxy)")
        plt.xlabel("Scale Factor a(t)")
        plt.ylabel("Energy Density")
        plt.title("Cosmic Evolution with H0 Tension Proxies")
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

    print("Tuning alpha for H0 tension proxy...\n")
    best_alpha, error = tune_alpha_for_lambda()

    gv = GodVariable(alpha=best_alpha)
    gv.set_evolving_profile(vacuum_amplitude=0.05)
    derived_lambda = gv.derive_lambda()

    print(f"Best-fit α:       {best_alpha:.3e}")
    print(f"Λ error:          {error:.3e}\n")

    print(f"Derived Λ:        {derived_lambda:.3e} m⁻²")
    print(f"Observed Λ:       {observed_lambda:.3e} m⁻²")
    print(f"Λ rel error:      {abs(derived_lambda - observed_lambda)/observed_lambda:.2e}\n")

    h0_early, h0_late, tension = gv.h0_tension_proxy()
    print(f"Toy H0 early (CMB proxy): {h0_early:.1f} km/s/Mpc")
    print(f"Toy H0 late (SNe proxy):  {h0_late:.1f} km/s/Mpc")
    print(f"Toy tension:              {tension:.1f} σ proxy")

    aware, entropy = gv.emergent_consciousness_proxy()
    print(f"\nConsciousness proxy:      {'Triggered' if aware else 'Not yet'} (entropy {entropy:.3f})")

    gv.plot_evolution()


if __name__ == "__main__":
    main()
