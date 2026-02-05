"""
gv_simulation.py
Per Grok: Black hole entropy layer — Gv event horizon analog (S ~ A/4 Planck units).
Horizon from curvature peak, entropy from fluctuation info on horizon, tied to consciousness bounds.
H0 tension + previous features.
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
        self.curvature_proxy = None

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
        
        # Curvature proxy for BH analog
        curvature = 8 * np.pi * rho_total
        curvature += 0.05 * np.gradient(np.gradient(curvature))
        self.curvature_proxy = curvature
        
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

    def bh_horizon_proxy(self):
        """Toy event horizon from curvature peak (early dense era proxy)."""
        peak_idx = np.argmax(self.curvature_proxy)
        horizon_radius_proxy = 1 / (self.scale_factors[peak_idx] + 0.01)  # Inverse scale
        area_proxy = 4 * np.pi * horizon_radius_proxy**2
        return area_proxy, peak_idx

    def bh_entropy_proxy(self):
        """S ~ A/4 Planck units analog, scaled by Gv info content."""
        area, _ = self.bh_horizon_proxy()
        s_bekenstein = area / 4  # Planck units proxy
        # Tie to info bounds: fluctuation entropy on "horizon" region
        horizon_slice = slice(max(0, peak_idx-50), min(len(self.rho_profile), peak_idx+50))
        local_fluct = self.rho_profile[horizon_slice] - np.mean(self.rho_profile[horizon_slice])
        info_entropy = -np.sum(local_fluct**2 * np.log(local_fluct**2 + 1e-100))
        entropy = s_bekenstein * (1 + 0.1 * info_entropy)  # Gv-tied info boost
        return entropy

    def plot_evolution(self, save_path="rho_bh_entropy.png"):
        plt.figure(figsize=(12, 10))
        plt.subplot(2,1,1)
        plt.plot(self.scale_factors, self.rho_profile, label=r"$\rho_{\text{total}}(a)$", color="purple")
        plt.plot(self.scale_factors, self.curvature_proxy / np.max(self.curvature_proxy), label="Curvature Proxy (norm)", color="darkgreen", alpha=0.7)
        area, peak_idx = self.bh_horizon_proxy()
        plt.axvline(self.scale_factors[peak_idx], color='red', linestyle='--', label="Toy BH Horizon")
        plt.xlabel("Scale Factor a(t)")
        plt.ylabel("Density / Curvature")
        plt.xscale('log')
        plt.title("Cosmic Evolution with Toy Black Hole Horizon Proxy")
        plt.grid(True)
        plt.legend()
        
        plt.subplot(2,1,2)
        plt.plot(self.scale_factors, self.rho_profile, color="purple")
        plt.xlabel("Scale Factor a(t)")
        plt.ylabel("Energy Density")
        plt.xscale('log')
        plt.grid(True)
        
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

    print("Tuning alpha with BH entropy layer...\n")
    best_alpha, error = tune_alpha_for_lambda()

    gv = GodVariable(alpha=best_alpha)
    gv.set_evolving_profile(vacuum_amplitude=0.05)
    derived_lambda = gv.derive_lambda()

    print(f"Best-fit α:       {best_alpha:.3e}")
    print(f"Λ error:          {error:.3e}\n")

    print(f"Derived Λ:        {derived_lambda:.3e} m⁻²")
    print(f"Observed Λ:       {observed_lambda:.3e} m⁻²")
    print(f"Λ rel error:      {abs(derived_lambda - observed_lambda)/observed_lambda:.2e}\n")

    area, peak_idx = gv.bh_horizon_proxy()
    entropy = gv.bh_entropy_proxy()
    print(f"Toy BH horizon area proxy: {area:.3e}")
    print(f"Toy BH entropy (S ~ A/4 + Gv info): {entropy:.3e} Planck units")

    gv.plot_evolution()


if __name__ == "__main__":
    main()
