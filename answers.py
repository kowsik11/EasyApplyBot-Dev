import random
import yaml

# Load custom mappings from additionalquestions.yaml if present
try:
    with open("additionalquestions.yaml", "r", encoding="utf-8") as f:
        YAML_DEFAULTS = yaml.safe_load(f) or {}
except Exception:
    YAML_DEFAULTS = {}

# Explicit answers for known questions
_DEFAULTS = {
    "visa": "No",
    "sponsorship": "No",
    "salary": "0",
    "compensation": "0",
    "notice period": "0",
    "notice": "0",
    "pronoun": "They/Them",
    "javascript": "0",
    "react.js": "0",
    "wordpress": "0",
    "dashboard": "0",
    "background": "Yes",
    # Education dropdowns
    "clg":        "Amrita Vishwa Vidyapeetham",
    "college":    "Amrita Vishwa Vidyapeetham",
    "school":     "Amrita Vishwa Vidyapeetham",
    "degree":     "Bachelor's Degree",
    "discipline": "Computer Science and Engineering",
}

# Fallback texts for free-text questions
_DEFAULT_FALLBACK_TEXT = [
    # "N/A",
    # "Not Applicable",
    # "No Comments",
    "1",
    "2",
]

# Preferred dropdown answers for common selects
_DROPDOWN_DEFAULTS = {
    "experience":    "Yes",             # e.g. Do you have 2+ years…?
    "latency":       "Efficiency",      # e.g. Why is low latency good?
    "proficiency":   "Professional",    # e.g. level of proficiency…
    "country code":  "India (+91)",     # cellphone country picker
    "commute":       "Yes",             # willing to commute?
}

def lookup(label: str):
    """
    Return an explicit answer if key in YAML_DEFAULTS or _DEFAULTS matches the label.
    """
    l = label.lower()
    for key, ans in YAML_DEFAULTS.items():
        if key.lower() in l:
            return ans
    for key, ans in _DEFAULTS.items():
        if key in l:
            return ans
    return None

def get_answer(label: str, field_type: str) -> str:
    """
    Determine an answer by:
      1) explicit lookup
      2) number/tel → "0"
      3) text/textarea → random fallback
      4) default fallback
    """
    explicit = lookup(label or "")
    if explicit is not None:
        return explicit

    t = (field_type or "").lower()
    if t in ("number", "tel"):
        return "0"
    if t in ("text", "textarea"):
        return random.choice(_DEFAULT_FALLBACK_TEXT)

    return random.choice(_DEFAULT_FALLBACK_TEXT)
