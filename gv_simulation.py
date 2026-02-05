"""
gv_simulation.py
Per Grok: Recursive Gv layers for hierarchy/meta-variables.
Nested integrals cascade scales, toy derivation of particle masses (hierarchy problem proxy).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


class GodVariable:
    def __init__(self, alpha=1e-120, layers=3):
        self.alpha = alpha
        self.layers = layers
        self.gv_values = [alpha] * layers  # Recursive Gv stack
        self.rho_profiles = []
        self.x_values = None

    def set_recursive_profile(self, n_points=1000, vacuum_amplitude=0.05):
        x = np.linspace(0, 1, n_points)
        self.x_values = x
        rho_base = np.zeros_like(x)
        
        for layer in range(self.layers):
            # Each layer adds finer fluctuations (meta-cascade)
            scale = 10 ** (layer + 1)
            freq = scale * 200 * np.pi * x
            log_cutoff = np.log10(freq + 10) / np.log10(1e3 + layer * 1e3)
            vacuum_raw = vacuum_amplitude / scale * np.sin(freq) * np.exp(-5 * x)
            vacuum_fluct = vacuum_raw * (1 - log_cutoff.clip(0, 0.95))
            
            # Add cosmological components on base layer only
            if layer == 0:
                matter = 0.3 * np.exp(-((x - 0.3)**2) / 0.05)
                radiation = 0.1 / (1 + 100 * x**2)
                dark_energy = 0.7 * np.ones_like(x)
                rho_base = matter + radiation + dark_energy + vacuum_fluct + 1e-121
            else:
                rho_base += vacuum_fluct  # Higher layers add quantum fines
            
            self.rho_profiles.append(rho_base.copy())

    def compute_nested_integral(self, layer=0):
        """Recursive nested integral across layers."""
        if layer >= self.layers:
            return 0.0
        inner = self.compute_nested_integral(layer + 1)
        outer = np.trapezoid(self.rho_profiles[layer], x=self.x_values)
        return outer + 0.1 * inner  # Cascade weighting

    def update_gv(self):
        nested = self.compute_nested_integral()
        for i in range(self.layers):
            self.gv_values[i] = nested / (10 ** i) + self.alpha
        return self.gv_values[0]  # Top-level Gv

    def derive_lambda(self, scale_factor=1e61):
        self.update_gv()
        return self.gv_values[0] / (scale_factor ** 4)

    def derive_particle_mass_ratio(self):
        """
        Toy hierarchy problem: Higgs/electron mass ratio ~10^17 proxy.
        From nested scale cascade (fine layer Gv small, coarse large).
        """
        self.update_gv()
        fine_gv = self.gv_values[-1] + 1e-100  # Quantum layer
        coarse_gv = self.gv_values[0] + 1e-100  # Cosmic layer
        ratio = coarse_gv / fine_gv
        return ratio

    def plot_profiles(self, save_path="rho_recursive_layers.png"):
        plt.figure(figsize=(12, 8))
        colors = ['purple', 'darkgreen', 'orange']
        for i, rho in enumerate(self.rho_profiles):
            plt.plot(self.x_values, rho, label=f"Layer {i+1} ρ(x)", color=colors[i % len(colors)])
        plt.xlabel("Normalized Scale Factor")
        plt.ylabel("Energy Density")
        plt.title("Recursive Gv Layers — Nested Fluctuations Cascade")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path)
        print(f"Plot saved: {save_path}")


def tune_alpha_for_lambda(target_lambda=1.1056e-52, scale_factor=1e61):
    gv = GodVariable(layers=3)
    gv.set_recursive_profile(vacuum_amplitude=0.05)
    nested = gv.compute_nested_integral()

    def objective(alpha):
        gv.alpha = float(alpha)
        derived = gv.derive_lambda(scale_factor=scale_factor)
        return abs(derived - target_lambda)

    result = minimize_scalar(objective, bounds=(1e100, 1e200), method='bounded', tol=1e-15)
    return result.x, result.fun


def main():
    observed_lambda = 1.1056e-52

    print("Tuning alpha with recursive Gv layers...\n")
    best_alpha, error = tune_alpha_for_lambda()

    gv = GodVariable(alpha=best_alpha, layers=3)
    gv.set_recursive_profile(vacuum_amplitude=0.05)
    derived_lambda = gv.derive_lambda()

    print(f"Best-fit α:       {best_alpha:.3e}")
    print(f"Λ error:          {error:.3e}\n")

    print(f"Top-level Gv:     {gv.gv_values[0]:.3e}")
    print(f"Derived Λ:        {derived_lambda:.3e} m⁻²")
    print(f"Observed Λ:       {observed_lambda:.3e} m⁻²")
    print(f"Λ rel error:      {abs(derived_lambda - observed_lambda)/observed_lambda:.2e}\n")

    mass_ratio = gv.derive_particle_mass_ratio()
    print(f"Toy Higgs/electron mass ratio (hierarchy proxy): {mass_ratio:.3e}")

    gv.plot_profiles()


if __name__ == "__main__":
    main()
