"""
gv_simulation.py
First minimal simulation of the God Variable (Gv) to derive/test the cosmological constant Λ.
"""

import numpy as np


class GodVariable:
    """
    Basic God Variable class.
    Core: Gv = ∫ ρ_total(x,t) dV + α
    """

    def __init__(self, alpha=1.23e-120):
        """
        alpha: the necessary/initiating constant (tuning parameter)
        Current value is a rough Planck-scale placeholder — we will tune it.
        """
        self.alpha = alpha
        self.gv_value = alpha
        self.rho_profile = None

    def set_energy_density_profile(self, rho_values, x_values=None):
        """
        Set a 1D proxy for total energy density profile.
        In reality this would be 4D over spacetime — this is a toy model.
        """
        self.rho_profile = np.asarray(rho_values)
        if x_values is None:
            # fake uniform spacing
            x_values = np.linspace(0, 1, len(rho_values))
        self.x_values = np.asarray(x_values)

    def compute_integral(self):
        """Numerically integrate the energy density profile"""
        if self.rho_profile is None:
            raise ValueError("No energy density profile set.")
        integral = np.trapz(self.rho_profile, x=self.x_values)
        return integral

    def update_gv(self):
        """Gv = integral + α"""
        integral = self.compute_integral()
        self.gv_value = integral + self.alpha
        return self.gv_value

    def derive_cosmological_constant(self, planck_length=1.616e-35):
        """
        Very rough derivation of Λ from Gv.
        Λ ~ 1 / (some large length scale)^2
        Here we pretend Gv sets an effective inverse length^4 scale.
        This is NOT rigorous — just a toy sanity check.
        """
        # Extremely rough conversion: pretend Gv relates to 1/L^4
        # (in natural units where ħ = c = 1)
        L_planck = planck_length
        scale_factor = 1e61  # huge number from Planck → cosmological scales
        derived_lambda = self.gv_value / (scale_factor * L_planck)**4
        return derived_lambda


def main():
    # Toy example: almost flat, very low average energy density
    # (critical density today ~ 8.6e-27 kg/m³, but in natural units tiny)
    n_points = 1000
    x = np.linspace(0, 1, n_points)
    # Very small, almost constant rho (dark energy dominated toy universe)
    rho = np.full(n_points, 1e-120)  # placeholder tiny value

    gv = GodVariable(alpha=1.1e-120)  # start close to expected Λ scale
    gv.set_energy_density_profile(rho, x)
    gv.update_gv()

    derived_lambda = gv.derive_cosmological_constant()

    observed_lambda = 1.1056e-52  # m⁻² (real value)

    print(f"Computed Gv:              {gv.gv_value:.3e}")
    print(f"Derived Λ:                {derived_lambda:.3e} m⁻²")
    print(f"Observed Λ:               {observed_lambda:.3e} m⁻²")
    print(f"Relative difference:      {abs(derived_lambda - observed_lambda)/observed_lambda:.2e}")


if __name__ == "__main__":
    main()
