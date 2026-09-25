"""
Mining & Geological Domain Calculators.
Implements standardized CMPDI / Indian Ministry of Coal formulas:
- In-Situ Geological Reserves Estimation
- Stripping Ratio Computation
- Coal Quality Grade Banding (GCV to Indian Standard Grades G1 - G17)
"""

from typing import Dict, Any, Tuple

class MiningCalculator:
    """Standardized mining computations."""

    @staticmethod
    def calculate_geological_reserves(
        area_sq_m: float,
        thickness_m: float,
        specific_gravity: float = 1.40
    ) -> Dict[str, Any]:
        """
        Calculates in-situ geological coal reserves in Million Tonnes (MT).
        Formula: Reserves (Tonnes) = Area (m^2) * Average Thickness (m) * Specific Gravity (t/m^3)
        """
        if area_sq_m <= 0 or thickness_m <= 0 or specific_gravity <= 0:
            raise ValueError("Area, thickness, and specific gravity must be strictly positive.")

        tonnes = area_sq_m * thickness_m * specific_gravity
        million_tonnes = tonnes / 1_000_000.0

        return {
            "area_sq_m": area_sq_m,
            "thickness_m": thickness_m,
            "specific_gravity": specific_gravity,
            "reserves_tonnes": round(tonnes, 2),
            "reserves_million_tonnes": round(million_tonnes, 4),
            "formula": "Area (m^2) * Thickness (m) * Specific Gravity (t/m^3)"
        }

    @staticmethod
    def calculate_stripping_ratio(
        overburden_volume_m3: float,
        coal_tonnes: float
    ) -> Dict[str, Any]:
        """
        Calculates the volumetric stripping ratio (m^3 of overburden per tonne of coal).
        """
        if coal_tonnes <= 0:
            raise ValueError("Coal reserve tonnage must be greater than zero.")

        ratio = overburden_volume_m3 / coal_tonnes
        return {
            "overburden_volume_m3": overburden_volume_m3,
            "coal_tonnes": coal_tonnes,
            "stripping_ratio_m3_per_tonne": round(ratio, 2)
        }

    @staticmethod
    def get_coal_grade_from_gcv(gcv_kcal_kg: float) -> Tuple[str, str]:
        """
        Classifies non-coking coal into Indian Ministry of Coal Grade bands (G1 to G17)
        based on Gross Calorific Value (GCV in kcal/kg).
        """
        bands = [
            (7000, float("inf"), "G1", "> 7000"),
            (6700, 7000, "G2", "6701 - 7000"),
            (6400, 6700, "G3", "6401 - 6700"),
            (6100, 6400, "G4", "6101 - 6400"),
            (5800, 6100, "G5", "5801 - 6100"),
            (5500, 5800, "G6", "5501 - 5800"),
            (5200, 5500, "G7", "5201 - 5500"),
            (4900, 5200, "G8", "4901 - 5200"),
            (4600, 4900, "G9", "4601 - 4900"),
            (4300, 4600, "G10", "4301 - 4600"),
            (4000, 4300, "G11", "4001 - 4300"),
            (3700, 4000, "G12", "3701 - 4000"),
            (3400, 3700, "G13", "3401 - 3700"),
            (3100, 3400, "G14", "3101 - 3400"),
            (2800, 3100, "G15", "2801 - 3100"),
            (2500, 2800, "G16", "2501 - 2800"),
            (2200, 2500, "G17", "2201 - 2500"),
        ]

        for lower, upper, grade, band_desc in bands:
            if lower < gcv_kcal_kg <= upper:
                return grade, f"{band_desc} kcal/kg"

        return "Ungraded", "< 2200 kcal/kg"
