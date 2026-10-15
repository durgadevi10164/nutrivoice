"""
bmi.py
------
Simple BMI calculation helper. Kept separate from the UI so the same
function can later be reused by the AI nutrition engine (Phase 3/4)
without duplicating logic.
"""


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Return BMI rounded to 1 decimal place. Assumes both inputs are positive numbers."""
    height_m = height_cm / 100
    if height_m <= 0:
        return 0.0
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)


def bmi_category(bmi: float) -> str:
    """Return a plain-language BMI band. Informational only — not a medical diagnosis."""
    if bmi <= 0:
        return "Not available"
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal range"
    if bmi < 30:
        return "Overweight"
    return "Obese"
