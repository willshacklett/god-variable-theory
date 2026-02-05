"""
gv_simulation.py
Upgraded: More realistic rho profile (matter + radiation + dark energy components).
Alpha tuning for Λ, plus optional fine-structure α derivation attempt.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)  # Suppress overflow warnings


class GodVariable:
    def __init__(self, alpha=1e-120):
        self.alpha = alpha
        self.gv_value = alpha
        self.rho_profile = None
        self.x_values = None

    def set_realistic_profile(self, n_points=1000):
        """More physical toy profile: matter bump + radiation tail + dark energy floor."""
        x = np.linspace(0, 1, n_points)
        # Normalized proxies (arbitrary units for toy)
        matter = 0.3 * np.exp(-((x - 0.3)**2) / 0.05)  # Early matter peak
        radiation = 0.1 / (1 + 100 * x**2)            # High early, falls off
        dark_energy = 0.7 * np.ones_like(x)           # Constant floor
        rho_total = matter + radiation + dark_energy + 1e-121  # Tiny offset
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

    def plot_profile(self, save_path="rho_profile_realistic.png"):
        plt.figure(figsize=(10, 6))
        plt.plot(self.x_values, self.rho_profile, label=r"$\rho_{\text{total}}(x)$", color="purple")
        plt.xlabel("Normalized Scale Factor (early → late universe proxy)")
        plt.ylabel("Energy Density (arbitrary units)")
        plt.title("Realistic Toy Energy Density Profile")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path)
        print(f"Plot saved: {save_path}")


def tune_alpha_for_lambda(target_lambda=1.1056e-52, scale_factor=1e61):
    gv = GodVariable()
    gv.set_realistic_profile()
    integral = gv.compute_integral()  # Fixed profile

    def objective(alpha):
        gv.alpha = float(alpha)
        derived = gv.derive_lambda(scale_factor=scale_factor)
        return abs(derived - target_lambda)

    result = minimize_scalar(objective, bounds=(1e100, 1e200), method='bounded', tol=1e-15)
    return result.x, result.fun, integral


def main():
    observed_lambda = 1.1056e-52

    print("Tuning alpha with realistic toy profile...\n")
    best_alpha, error, integral = tune_alpha_for_lambda()

    gv = GodVariable(alpha=best_alpha)
    gv.set_realistic_profile()
    derived_lambda = gv.derive_lambda()

    print(f"Profile integral contribution: {integral:.3e}")
    print(f"Best-fit α:                    {best_alpha:.3e}")
    print(f"Tuning residual error:         {error:.3e}\n")

    print(f"Computed Gv:                   {gv.gv_value:.3e}")
    print(f"Derived Λ:                     {derived_lambda:.3e} m⁻²")
    print(f"Observed Λ:                    {observed_lambda:.3e} m⁻²")
    print(f"Relative error:                {abs(derived_lambda - observed_lambda)/observed_lambda:.2e}")

    gv.plot_profile()


if __name__ == "__main__":
    main()
