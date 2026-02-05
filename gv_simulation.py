"""
gv_simulation.py
Upgraded with quantum vacuum fluctuations in rho_total for realism.
Improved toy fine-structure α derivation incorporating fluctuation amplitude.
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
        self.x_values = None

    def set_realistic_profile(self, n_points=1000, vacuum_amplitude=0.05):
        """Realistic profile + quantum vacuum fluctuations."""
        x = np.linspace(0, 1, n_points)
        matter = 0.3 * np.exp(-((x - 0.3)**2) / 0.05)
        radiation = 0.1 / (1 + 100 * x**2)
        dark_energy = 0.7 * np.ones_like(x)
        # Quantum vacuum fluctuations: small high-frequency oscillation
        vacuum_fluct = vacuum_amplitude * np.sin(200 * np.pi * x) * np.exp(-10 * x)  # Early dominance, damps
        rho_total = matter + radiation + dark_energy + vacuum_fluct + 1e-121
        self.rho_profile = rho_total
        self.x_values = x

    def compute_integral(self):
        return np.trapezoid(self.rho_profile, x=self.x_values)

    def update_gv(self):
        integral = self.compute_integral()
        self.gv_value = integral + self.alpha
        return self.gv_value

    def derive_lambda(self, scale_factor=1e61):
        self.update_gv()
        return self.gv_value / (scale_factor ** 4)

    def derive_fine_structure(self, quantum_offset=120.0):
        """Improved toy α: incorporate vacuum fluctuation amplitude into coupling."""
        self.update_gv()
        # Fluct amplitude proxy from profile (early high-freq part)
        fluct_amp = np.max(np.abs(self.rho_profile[:200] - np.mean(self.rho_profile[:200])))
        log_gv = np.log10(abs(self.gv_value) + 1e-100)
        derived_inv_alpha = log_gv + quantum_offset + 10 / (fluct_amp + 0.01)  # Fluct dampens coupling
        return 1 / derived_inv_alpha, derived_inv_alpha

    def plot_profile(self, save_path="rho_profile_quantum.png"):
        plt.figure(figsize=(10, 6))
        plt.plot(self.x_values, self.rho_profile, label=r"$\rho_{\text{total}}(x)$ w/ Vacuum Fluctuations", color="purple")
        plt.xlabel("Normalized Scale Factor (early → late universe proxy)")
        plt.ylabel("Energy Density (arbitrary units)")
        plt.title("Realistic Toy Profile with Quantum Vacuum Fluctuations")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path)
        print(f"Plot saved: {save_path}")


def tune_alpha_for_lambda(target_lambda=1.1056e-52, scale_factor=1e61):
    gv = GodVariable()
    gv.set_realistic_profile(vacuum_amplitude=0.05)
    integral = gv.compute_integral()

    def objective(alpha):
        gv.alpha = float(alpha)
        derived = gv.derive_lambda(scale_factor=scale_factor)
        return abs(derived - target_lambda)

    result = minimize_scalar(objective, bounds=(1e100, 1e200), method='bounded', tol=1e-15)
    return result.x, result.fun, integral


def main():
    observed_lambda = 1.1056e-52
    observed_inv_alpha = 137.036

    print("Tuning alpha with quantum vacuum fluctuations...\n")
    best_alpha, error, integral = tune_alpha_for_lambda()

    gv = GodVariable(alpha=best_alpha)
    gv.set_realistic_profile(vacuum_amplitude=0.05)
    derived_lambda = gv.derive_lambda()

    print(f"Profile integral contribution: {integral:.3e}")
    print(f"Best-fit α (for Λ):            {best_alpha:.3e}")
    print(f"Λ tuning residual error:       {error:.3e}\n")

    print(f"Computed Gv:                   {gv.gv_value:.3e}")
    print(f"Derived Λ:                     {derived_lambda:.3e} m⁻²")
    print(f"Observed Λ:                    {observed_lambda:.3e} m⁻²")
    print(f"Λ relative error:              {abs(derived_lambda - observed_lambda)/observed_lambda:.2e}\n")

    # Improved α with fluctuations
    derived_alpha, derived_inv_alpha = gv.derive_fine_structure(quantum_offset=120.0)
    print("Improved toy fine-structure derivation (vacuum fluctuations included):")
    print(f"Derived α:                     {derived_alpha:.6f}")
    print(f"Derived 1/α:                   {derived_inv_alpha:.3f}")
    print(f"Observed 1/α:                  {observed_inv_alpha:.3f}")
    print(f"1/α match error:               {abs(derived_inv_alpha - observed_inv_alpha):.3f}")

    gv.plot_profile()


if __name__ == "__main__":
    main()
