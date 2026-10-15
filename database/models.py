"""
models.py
---------
This prototype uses plain sqlite3 (see database.py) rather than a full ORM,
but we keep field names, table name, and dropdown option lists centralized
here so the UI, validation, and database layers never disagree about what
a "user_type" or "gender" value is allowed to be. When Phase 2+ (voice,
AI recommendations) is added, new tables/constants can be appended here
without touching this file's existing contents.
"""

TABLE_NAME = "users"

USER_TYPE_PREGNANT = "Pregnant Woman"
USER_TYPE_CHILD = "Child / Parent"
USER_TYPES = [USER_TYPE_PREGNANT, USER_TYPE_CHILD]

GENDERS = ["Female", "Male", "Other"]
CHILD_GENDERS = ["Female", "Male", "Other"]

FOOD_PREFERENCES = ["Vegetarian", "Non-Vegetarian"]

DIETARY_PREFERENCES = [
    "No specific preference",
    "Diabetic-friendly",
    "Low-spice",
    "High-protein",
    "Other",
]

LANGUAGES = ["Tamil", "English", "Hindi", "Telugu", "Kannada", "Malayalam", "Other"]

# Column list, in the order the users table stores them (used by the
# profile display page so it always shows every stored field).
USER_FIELDS = [
    "id", "full_name", "age", "gender", "phone", "email",
    "height", "weight", "bmi", "user_type", "pregnancy_month",
    "child_age", "child_gender", "food_preference", "dietary_preference",
    "preferred_language", "food_allergies", "created_at", "updated_at",
]
