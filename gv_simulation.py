"""
gv_simulation.py
Clean rewrite: God Variable (Gv) toy simulation with alpha auto-tuning to match observed cosmological constant Λ.
Uses modern NumPy (np.trapezoid), wider bounds, plotting, and clear results.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar


class GodVariable:
    """
    Core God Variable implementation.
    Gv = ∫ ρ_total dV + α
    """

    def __init__(self, alpha=1e-120):
        self.alpha = alpha
        self.gv_value = alpha
        self.rho_profile = None
        self.x_values = None

    def set_energy_density_profile(self, rho_values, x_values=None):
        """Set 1D proxy for total energy density."""
        self.rho_profile = np.asarray(rho_values)
        if x_values is None:
            x_values = np.linspace(0, 1, len(rho_values))
        self.x_values = np.asarray(x_values)

    def compute_integral(self):
        """Numerical integration using modern NumPy."""
        if self.rho_profile is None:
            raise ValueError("Energy density profile not set.")
        return np.trapezoid(self.rho_profile, x=self.x_values)

    def update_gv(self):
        """Gv = integral + alpha"""
        integral = self.compute_integral()
        self.gv_value = integral + self.alpha
        return self.gv_value

    def derive_lambda(self, scale_factor=1e61):
        """
        Toy derivation of Λ from Gv.
        Rough proxy: Λ ~ Gv / (large cosmological scale)^4
        scale_factor approximates Planck → observable universe conversion.
        """
        self.update_gv()
        return self.gv_value / (scale_factor ** 4)

    def plot_profile(self, save_path="rho_profile.png"):
        """Plot and save the energy density profile."""
        if self.rho_profile is None:
            print("No profile to plot.")
            return
        plt.figure(figsize=(10, 6))
        plt.plot(self.x_values, self.rho_profile, label=r"$\rho_{\text{total}}(x)$", color="purple")
        plt.xlabel("Normalized Space")
        plt.ylabel("Energy Density")
        plt.title("Toy Energy Density Profile for Gv Simulation")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path)
        print(f"Plot saved: {save_path}")


def tune_alpha_for_lambda(target_lambda=1.1056e-52, scale_factor=1e61):
    """Find best alpha to match observed Λ with toy flat rho profile."""
    n_points = 1000
    x = np.linspace(0, 1, n_points)
    rho = np.full(n_points, 1e-121)  # Tiny flat density (dark energy proxy)

    def objective(alpha):
        gv = GodVariable(alpha=float(alpha))
        gv.set_energy_density_profile(rho, x)
        derived = gv.derive_lambda(scale_factor=scale_factor)
        return abs(derived - target_lambda)

    # Wide bounds — toy model needs large positive alpha due to scale_factor**4
    result = minimize_scalar(objective, bounds=(1e100, 1e200), method='bounded', tol=1e-15)
    return result.x, result.fun


def main():
    observed_lambda = 1.1056e-52  # m⁻² (real value)

    print("Tuning alpha to match observed Λ...\n")
    best_alpha, error = tune_alpha_for_lambda()

    print(f"Best-fit α:               {best_alpha:.3e}")
    print(f"Tuning residual error:    {error:.3e}\n")

    # Run full sim with tuned alpha
    gv = GodVariable(alpha=best_alpha)
    n_points = 1000
    x = np.linspace(0, 1, n_points)
    rho = np.full(n_points, 1e-121)
    gv.set_energy_density_profile(rho, x)

    derived_lambda = gv.derive_lambda()

    print(f"Computed Gv:              {gv.gv_value:.3e}")
    print(f"Derived Λ:                {derived_lambda:.3e} m⁻²")
    print(f"Observed Λ:               {observed_lambda:.3e} m⁻²")
    print(f"Relative error:           {abs(derived_lambda - observed_lambda)/observed_lambda:.2e}")

    # Save plot
    gv.plot_profile()


if __name__ == "__main__":
    main()
