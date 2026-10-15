# NutriVoice – AI-Based Voice Nutrition Assistant

**Current stage: Basic Profile Management System (Professional UI)**

## 1. Project Objective

NutriVoice is a college project aiming to build an accessible, voice-enabled
nutrition assistant for rural pregnant women and children. This stage builds
the **foundation**: a professional-looking Streamlit web app where a user
can create, view, and edit a nutrition profile, stored in a local SQLite
database. The AI nutrition engine and voice features are **not**
implemented yet — they are planned for later phases (see Section 13).

## 2. Features

- Professional healthcare-technology UI: dark navy background, white
  text/headings, NutriVoice green (`#2E9F6B`) accents, Inter font
- User profile creation with dynamic fields (Pregnant Woman vs Child/Parent)
- Profile validation with friendly, non-crashing error messages
- Automatic BMI calculation (clearly labeled as informational only)
- SQLite storage (`nutrivoice.db`, created automatically)
- Profile dashboard ("My Profile") with clearly readable field names and values
- Edit Profile (loads existing data, saves changes back to the database)
- Personalized home dashboard once a profile exists, with a "Coming Soon"
  preview of the AI Nutrition Assistant and future voice features
- About page describing the project and its roadmap
- Header + sidebar navigation, both highlighting the active page in green
- Sidebar "Profile Status" indicator (green = completed, amber = not created)

## 3. Technology

- **Python 3**
- **Streamlit** — web UI
- **SQLite** (via Python's built-in `sqlite3`) — data storage
- **CSS** — professional healthcare-style theme (`assets/style.css`)
- **pandas** — included for future data handling (Phase 3+)

No React, Node.js, MongoDB, Firebase, Docker, or Kubernetes are used.

## 3a. UI / Design System

| Role | Color |
|---|---|
| Page & card background | Dark Navy `#0F2A47` (page) / `#17395C` (cards, sidebar) |
| Primary text (headings, labels, body) | White `#FFFFFF` |
| Secondary text | Light blue-gray `#C7D6E5` |
| Accent (buttons, highlights, active nav, section labels) | NutriVoice Green `#2E9F6B` |
| Input field background | White `#FFFFFF` (kept light for readability against the dark page) |
| Input text | Dark Navy `#12355B` |
| Borders / dividers | `#2F5878` |

Font: **Inter** (loaded from Google Fonts, with a system sans-serif fallback).

**Why labels were showing up invisible before:** Streamlit auto-selects a
light or dark theme based on the visitor's OS/browser setting unless a
theme is explicitly configured, and it also lets each visitor manually
override the theme via its own in-app Settings menu, which is remembered
per-browser and takes precedence over `config.toml`. This version fixes
that at two levels:
1. `.streamlit/config.toml` pins the app to this exact dark navy theme.
2. `assets/style.css` hardens every label/input/dropdown/sidebar selector
   (`stWidgetLabel`, `stTextInput`, `stNumberInput`, `data-baseweb="select"`,
   `stRadio`, sidebar buttons, etc.) with explicit colors, so the UI stays
   readable regardless of the visitor's own theme setting. If a page ever
   looks wrong, check the app's own Settings menu (⋮ top-right) and set
   its theme explicitly rather than "Use system setting".

## 4. Architecture

The project separates concerns into four layers so that later phases
(voice input, AI recommendations, local-language support) can be added
without rewriting existing code:

- **UI (`views/`)** — Streamlit pages only; no direct database access
- **Database (`database/`)** — all SQLite queries live here
- **Utils (`utils/`)** — validation and BMI calculation logic, reusable by future phases
- **Styling (`assets/`)** — CSS kept separate from Python code

> **Note on folder naming:** the original spec suggested a folder named
> `pages/`. This project uses `views/` instead, because Streamlit
> automatically turns any folder literally named `pages/` into its own
> built-in multipage navigation sidebar, which would create a second,
> conflicting navigation menu alongside the custom sidebar this app
> already builds. `views/` keeps the same separation of concerns without
> that conflict. Everything else follows the requested structure.

## 5. Folder Structure

```
NutriVoice/
│
├── app.py                  # Main entry point — run this with Streamlit
│
├── database/
│   ├── __init__.py
│   ├── database.py         # All SQLite connection/CRUD functions
│   └── models.py           # Table name + shared field/option constants
│
├── views/
│   ├── __init__.py
│   ├── home.py              # Home page (hero, features, dashboard)
│   ├── profile.py           # Create/Edit form, success page, profile view
│   └── about.py             # About page
│
├── utils/
│   ├── __init__.py
│   ├── validation.py       # Form validation
│   └── bmi.py               # BMI calculation
│
├── assets/
│   └── style.css            # Custom healthcare-style CSS (navy + green theme)
│
├── .streamlit/
│   └── config.toml          # Pins the app to a light theme (fixes white-on-white labels)
│
├── requirements.txt
├── README.md
└── .gitignore
```

`nutrivoice.db` is created automatically the first time you run the app —
it is not included in the project files.

## 6. Installation

### Step 1 — Create a virtual environment (Windows)

```bash
python -m venv venv
```

### Step 2 — Activate it (Windows)

```bash
venv\Scripts\activate
```

*(On macOS/Linux, use `source venv/bin/activate` instead.)*

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

## 7. How to Run

```bash
streamlit run app.py
```

Streamlit will open the app in your browser (usually at
`http://localhost:8501`). The SQLite database file `nutrivoice.db` is
created automatically in the project folder on first run.

## 8. Database Explanation

A single table, **`users`**, stores every profile. Fields not relevant to
a given user type are stored as `NULL` — for example, a "Pregnant Woman"
profile has a `pregnancy_month` value and a `NULL` `child_age`, while a
"Child / Parent" profile has `child_age`/`child_gender` values and a
`NULL` `pregnancy_month`.

This is a **single-profile prototype**: there is no login system yet, so
"My Profile" always refers to the most recently created or edited row in
the database. Multi-user accounts can be added in a later phase.

## 9. How to Create a Profile

1. From the Home page, click **Create Your Profile** (or **Create Profile**
   in the header/sidebar).
2. Fill in Basic Information, Physical Information, and select a User
   Category (**Pregnant Woman** or **Child / Parent**) — the form fields
   below update automatically based on your selection.
3. Click **Create Profile**. If any field is invalid, a friendly error
   message appears and nothing is saved until it's fixed.
4. On success, you'll see a **Profile Created Successfully** screen.

## 10. How to Edit a Profile

1. Open **My Profile** from the header or sidebar.
2. Click **Edit Profile**. The form loads your existing saved data.
3. Make changes and click **Save Changes** — this updates the same
   database row (it does not create a new profile).

## 11. How to Test the Project

Manually verify the checklist below (all are satisfied by this version):

1. `streamlit run app.py` starts without errors.
2. A profile can be created through the form.
3. Required fields are validated with friendly error messages.
4. "Pregnancy Month" only appears when "Pregnant Woman" is selected.
5. "Child Age"/"Child Gender" only appear when "Child / Parent" is selected.
6. BMI is calculated correctly from height and weight.
7. The profile is saved to `nutrivoice.db`.
8. The saved profile displays correctly on "My Profile".
9. The profile can be edited.
10. Edited data is correctly updated in the database.
11. The Home page shows a personalized dashboard once a profile exists.
12. Leaving optional fields (phone, email, allergies) blank does not crash the app.
13. `nutrivoice.db` is created automatically if it doesn't exist.
14. Header and sidebar navigation both correctly switch pages.
15. Custom CSS from `assets/style.css` loads and styles the app.

## 12. Current Limitations

- Single profile only (no multi-user login/authentication yet)
- No AI nutrition recommendations
- No voice input, speech-to-text, or text-to-speech
- No Tamil or other local-language interface (only stored as a preference field)
- Not intended for real medical use — informational/demo purposes only

## 13. Future Development Plan

| Phase | Feature |
|---|---|
| Phase 2 | Voice input: microphone → speech-to-text → user question |
| Phase 3 | Nutrition knowledge base: profile + question → relevant information |
| Phase 4 | AI recommendation: profile + nutrition data + question → personalized guidance |
| Phase 5 | Voice output: AI response → text-to-speech → spoken answer |
| Phase 6 | Local language support, including Tamil |

The current architecture (separated UI, database, and utils layers) is
designed so these phases can be added incrementally without rewriting
the existing profile-management foundation.
