"""
gv_simulation.py
Improved simulation of the God Variable (Gv) — now with alpha tuning to match observed Λ.
Toy model for empirical testing.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

class GodVariable:
    """
    God Variable class with energy integral and Λ derivation.
    """

    def __init__(self, alpha=1e-120):
        self.alpha = alpha
        self.gv_value = alpha
        self.rho_profile = None
        self.x_values = None

    def set_energy_density_profile(self, rho_values, x_values=None):
        """Set 1D proxy energy density profile."""
        self.rho_profile = np.asarray(rho_values)
        if x_values is None:
            x_values = np.linspace(0, 1, len(rho_values))  # normalized "space"
        self.x_values = np.asarray(x_values)

    def compute_integral(self):
        """Trapezoidal integration of rho over x."""
        if self.rho_profile is None:
            raise ValueError("Set energy density profile first.")
        return np.trapz(self.rho_profile, x=self.x_values)

    def update_gv(self):
        """Gv = integral + alpha"""
        integral = self.compute_integral()
        self.gv_value = integral + self.alpha
        return self.gv_value

    def derive_lambda(self, scale_factor=1e61):
        """
        Rough toy derivation: Λ ~ Gv / (large scale)^4
        scale_factor approximates Planck → cosmological conversion.
        """
        self.update_gv()
        return self.gv_value / scale_factor**4

    def plot_profile(self, save_path=None):
        """Plot the energy density profile."""
        if self.rho_profile is None:
            print("No profile to plot.")
            return
        plt.figure(figsize=(8, 5))
        plt.plot(self.x_values, self.rho_profile, label='ρ_total(x)')
        plt.xlabel('Normalized Space')
        plt.ylabel('Energy Density')
        plt.title('Toy Energy Density Profile')
        plt.grid(True)
        plt.legend()
        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved to {save_path}")
        else:
            plt.show()


def tune_alpha_for_lambda(target_lambda=1.1056e-52, scale_factor=1e61):
    """
    Optimize alpha to match observed Λ.
    Fixed toy rho profile (flat low density).
    """
    # Toy flat profile — dark energy dominated universe proxy
    n_points = 1000
    x = np.linspace(0, 1, n_points)
    rho = np.full(n_points, 1e-121)  # very small base density

    def objective(alpha):
        gv = GodVariable(alpha=float(alpha))
        gv.set_energy_density_profile(rho, x)
        derived = gv.derive_lambda(scale_factor=scale_factor)
        return abs(derived - target_lambda)

    result = minimize_scalar(objective, bounds=(1e-130, 1e-110), method='bounded')
    return result.x, result.fun  # best alpha, residual error


def main():
    observed_lambda = 1.1056e-52  # m⁻²

    # Tuned alpha
    best_alpha, error = tune_alpha_for_lambda()
    print(f"Best-fit alpha: {best_alpha:.3e}")
    print(f"Residual error in Λ: {error:.3e}")

    # Full sim with tuned alpha
    gv = GodVariable(alpha=best_alpha)
    n_points = 1000
    x = np.linspace(0, 1, n_points)
    rho = np.full(n_points, 1e-121)  # placeholder
    gv.set_energy_density_profile(rho, x)

    derived_lambda = gv.derive_lambda()

    print(f"\nComputed Gv:      {gv.gv_value:.3e}")
    print(f"Derived Λ:        {derived_lambda:.3e} m⁻²")
    print(f"Observed Λ:       {observed_lambda:.3e} m⁻²")
    print(f"Match quality:    {abs(derived_lambda - observed_lambda)/observed_lambda:.2e} relative error")

    # Plot (uncomment to run locally)
    # gv.plot_profile(save_path="rho_profile.png")


if __name__ == "__main__":
    main()
