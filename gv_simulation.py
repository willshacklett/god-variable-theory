"""
gv_simulation.py
Per Grok: Cosmic time evolution — expanding universe sim (Big Bang → DE dominance).
Gv evolves over scale factor, derive toy Hubble constant H0 proxy from expansion rate.
Recursive layers + previous features preserved.
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
        self.gv_values = [alpha] * layers
        self.rho_profiles = []
        self.scale_factors = None  # a(t) proxy

    def set_evolving_profile(self, n_points=1000, vacuum_amplitude=0.05):
        """Evolving universe: scale factor a(t) from early (a~0) to late (a=1)."""
        a = np.linspace(0.001, 1, n_points)  # Avoid a=0 singularity
        self.scale_factors = a
        rho_base = np.zeros_like(a)
        
        for layer in range(self.layers):
            scale = 10 ** (layer + 1)
            freq = scale * 200 * np.pi * a
            log_cutoff = np.log10(freq + 10) / np.log10(1e3 + layer * 1e3)
            vacuum_raw = vacuum_amplitude / scale * np.sin(freq) / a**2  # Dilutes with expansion
            vacuum_fluct = vacuum_raw * (1 - log_cutoff.clip(0, 0.95))
            
            if layer == 0:
                # Time-evolving components (density ~ 1/a^3 matter, 1/a^4 radiation, constant DE)
                matter = 0.3 / a**3
                radiation = 0.1 / a**4
                dark_energy = 0.7 * np.ones_like(a)
                rho_base = matter + radiation + dark_energy + vacuum_fluct + 1e-121
            else:
                rho_base += vacuum_fluct
                
            self.rho_profiles.append(rho_base.copy())

    def compute_nested_integral(self, layer=0):
        if layer >= self.layers:
            return 0.0
        inner = self.compute_nested_integral(layer + 1)
        outer = np.trapezoid(self.rho_profiles[layer], x=self.scale_factors)
        return outer + 0.1 * inner

    def update_gv(self):
        nested = self.compute_nested_integral()
        for i in range(self.layers):
            self.gv_values[i] = nested / (10 ** i) + self.alpha
        return self.gv_values[0]

    def derive_lambda(self, scale_factor=1e61):
        self.update_gv()
        return self.gv_values[0] / (scale_factor ** 4)

    def derive_hubble_proxy(self):
        """Toy H0 from Gv growth rate over scale factor (expansion proxy)."""
        self.update_gv()
        # Numerical da/dt proxy from late universe Gv change
        late_gv = self.gv_values[0]
        early_gv = self.gv_values[0] * 0.1  # Rough
        da = self.scale_factors[-1] - self.scale_factors[0]
        dGv_da = (late_gv - early_gv) / da if da != 0 else 0
        derived_H0 = dGv_da * 70  # Toy scaling to ~70 km/s/Mpc range
        return derived_H0

    def plot_evolution(self, save_path="rho_cosmic_evolution.png"):
        plt.figure(figsize=(12, 8))
        colors = ['purple', 'darkgreen', 'orange']
        for i, rho in enumerate(self.rho_profiles):
            plt.plot(self.scale_factors, rho, label=f"Layer {i+1} ρ(a)", color=colors[i % len(colors)])
        plt.xlabel("Scale Factor a(t) (early → late universe)")
        plt.ylabel("Energy Density")
        plt.title("Cosmic Evolution: Recursive Gv Layers in Expanding Universe")
        plt.xscale('log')  # Better view early times
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path)
        print(f"Plot saved: {save_path}")


def tune_alpha_for_lambda(target_lambda=1.1056e-52, scale_factor=1e61):
    gv = GodVariable(layers=3)
    gv.set_evolving_profile(vacuum_amplitude=0.05)
    nested = gv.compute_nested_integral()

    def objective(alpha):
        gv.alpha = float(alpha)
        derived = gv.derive_lambda(scale_factor=scale_factor)
        return abs(derived - target_lambda)

    result = minimize_scalar(objective, bounds=(1e100, 1e200), method='bounded', tol=1e-15)
    return result.x, result.fun


def main():
    observed_lambda = 1.1056e-52
    observed_H0 = 70  # km/s/Mpc proxy

    print("Tuning alpha in expanding universe sim...\n")
    best_alpha, error = tune_alpha_for_lambda()

    gv = GodVariable(alpha=best_alpha, layers=3)
    gv.set_evolving_profile(vacuum_amplitude=0.05)
    derived_lambda = gv.derive_lambda()

    print(f"Best-fit α:       {best_alpha:.3e}")
    print(f"Λ error:          {error:.3e}\n")

    print(f"Top-level Gv (late): {gv.gv_values[0]:.3e}")
    print(f"Derived Λ:        {derived_lambda:.3e} m⁻²")
    print(f"Observed Λ:       {observed_lambda:.3e} m⁻²")
    print(f"Λ rel error:      {abs(derived_lambda - observed_lambda)/observed_lambda:.2e}\n")

    derived_H0 = gv.derive_hubble_proxy()
    print(f"Toy derived H0:   {derived_H0:.3f} km/s/Mpc (proxy vs ~70 observed)")

    gv.plot_evolution()


if __name__ == "__main__":
    main()
