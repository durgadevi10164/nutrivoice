"""
validation.py
-------------
Validates profile form data before it reaches the database layer.
Returns a list of human-readable error strings — an empty list means
the data is valid. Keeping this separate from app.py means the same
rules can be reused if a Phase 2 API/voice input ever feeds data in
without going through the Streamlit form.
"""

from database.models import USER_TYPE_PREGNANT, USER_TYPE_CHILD


def validate_profile_form(data: dict) -> list:
    errors = []

    # --- Basic information ---
    if not data.get("full_name") or not str(data.get("full_name")).strip():
        errors.append("Full Name cannot be empty.")

    age = data.get("age")
    if age is None or age <= 0 or age > 120:
        errors.append("Age must be a valid number between 1 and 120.")

    if not data.get("gender"):
        errors.append("Please select a gender.")

    email = data.get("email")
    if email and "@" not in email:
        errors.append("Please enter a valid email address, or leave it blank.")

    phone = data.get("phone")
    if phone and not str(phone).strip().isdigit():
        errors.append("Phone number should contain digits only, or leave it blank.")

    # --- Physical information ---
    height = data.get("height")
    if height is None or height <= 0 or height > 300:
        errors.append("Height must be a positive number (in cm).")

    weight = data.get("weight")
    if weight is None or weight <= 0 or weight > 400:
        errors.append("Weight must be a positive number (in kg).")

    # --- User category ---
    user_type = data.get("user_type")
    if user_type not in (USER_TYPE_PREGNANT, USER_TYPE_CHILD):
        errors.append("Please select a user category.")

    if user_type == USER_TYPE_PREGNANT:
        month = data.get("pregnancy_month")
        if month is None or month < 1 or month > 9:
            errors.append("Pregnancy month must be between 1 and 9.")

    if user_type == USER_TYPE_CHILD:
        child_age = data.get("child_age")
        if child_age is None or child_age < 0 or child_age > 18:
            errors.append("Child age must be between 0 and 18.")
        if not data.get("child_gender"):
            errors.append("Please select the child's gender.")

    if not data.get("food_preference"):
        errors.append("Please select a food preference.")

    if not data.get("preferred_language"):
        errors.append("Please select a preferred language.")

    return errors
