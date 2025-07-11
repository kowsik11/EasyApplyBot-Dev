# import random
# import yaml

# # Load custom mappings from additionalquestions.yaml if present
# try:
#     with open("additionalquestions.yaml", "r", encoding="utf-8") as f:
#         YAML_DEFAULTS = yaml.safe_load(f) or {}
# except Exception:
#     YAML_DEFAULTS = {}

# # Explicit answers for known questions
# _DEFAULTS = {
#     "visa":           "No",
#     "sponsorship":    "No",
#     "pronoun":        "They/Them",
#     "college":        "Amrita Vishwa Vidyapeetham",
#     "school":         "Amrita Vishwa Vidyapeetham",
#     "degree":         "Bachelor's Degree",
#     "discipline":     "Computer Science and Engineering",
# }

# # Fallback texts for free-text questions
# _DEFAULT_FALLBACK_TEXT = [
#     "N/A",
#     "Not Applicable",
#     "No Comments",
# ]

# # Preferred dropdown answers for common selects
# _DROPDOWN_DEFAULTS = {
#     "experience":    "Yes",             # e.g. Do you have 2+ years…?
#     "latency":       "Efficiency",      # e.g. Why is low latency good?
#     "proficiency":   "Professional",    # e.g. level of proficiency…
#     "country code":  "India (+91)",     # cellphone country picker
#     "commute":       "Yes",             # willing to commute?
#     "notice period": "Immediatley",              # notice period
#     "availability":  "Immediately",     # availability to start
#     "suitable":     "Yes",             # are you suitable?
#     "immedialtely":     "Yes",             # can you start immediately?
#     "authorized":    "Yes",             # are you authorized to work?
#     "currently":     "Yes",             # are you currently employed?
#     "willing":      "Yes",             # are you willing to relocate?
#     "latency":         "Efficiency",      # why is low latency good?
#     "interested":     "Yes",             # are you interested in this position?
#     "inteview":       "Yes",             # are you available for an interview?
#     "training":        "Yes",             # are you willing to undergo training?
#     "ready":           "Yes",             # are you ready to start?
#     "remote":         "Yes",             # are you willing to work remotely?
#     "onsite":         "Yes",             # are you willing to work onsite?
#     "hybrid":         "Yes",             # are you willing to work hybrid?
#     "full-time":      "Yes",             # are you looking for full-time work? 
#     "part-time":      "Yes",             # are you looking for part-time work?
#     "contract":       "Yes",             # are you looking for contract work?   
#     "freelance":      "Yes",             # are you looking for freelance work?
#     "internship":     "Yes",             # are you looking for an internship?
#     "relocation":     "Yes",             # are you willing to relocate?
#     "sponsorship":    "No",              # are you looking for sponsorship?
#     "visa":           "No",              # are you looking for a visa?
#     "salary":         "700000",               # expected salary
#     "compensation":   "700000",               # expected compensation
#     "notice":         "0",                # notice period
#     "pronoun":        "He/Him",       # preferred pronouns
#     "javascript":     "2",                # javascript experience
#     "react.js":       "2",                # react.js experience   
#     "course":          "yes",  # course taken
#     "clicking":       "Yes",             # are you clicking on the apply button?
#     "apply":          "Yes",             # are you applying for the job?
#     "apply now":      "Yes",             # are you applying now?
# }

# def lookup(label: str):
#     """
#     Return an explicit answer if a key in YAML_DEFAULTS or _DEFAULTS matches the label.
#     """
#     q = label.lower()
#     for k, ans in YAML_DEFAULTS.items():
#         if k.lower() in q:
#             return ans
#     for k, ans in _DEFAULTS.items():
#         if k in q:
#             return ans
#     return None

# def get_answer(label: str, field_type: str) -> str:
#     """
#     Determine an answer by:
#       1) Years of experience → “1”/“2”/“3”
#       2) Notice period → “Immediately”/“Within 7 days”
#       3) Salary questions
#       4) Explicit lookup (YAML/_DEFAULTS)
#       5) Numeric fields → “0”
#       6) Text fields → random fallback
#     """
#     q = (label or "").lower()

#     # 1) Years of experience
#     if "experience" in q and any(w in q for w in ["year", "years"]):
#         return random.choice(["1", "2", "3"])

#     # 2) Notice period
#     if "notice period" in q or ("notice" in q and "period" not in q):
#         return random.choice(["Immediately", "Within 7 days"])

#     # 3) Salary
#     if "expected salary" in q or "expected compensation" in q:
#         return _DROPDOWN_DEFAULTS.get("expected salary", "700000")
#     if "current salary" in q:
#         return _DROPDOWN_DEFAULTS.get("current salary", "600000")

#     # 4) Explicit mappings
#     expl = lookup(label)
#     if expl is not None:
#         return expl

#     # 5) Numeric fields
#     if field_type.lower() in ("number", "tel"):
#         return "0"

#     # 6) Text / textarea
#     return random.choice(_DEFAULT_FALLBACK_TEXT)


import random
import yaml

# Load custom mappings from additionalquestions.yaml if present
try:
    with open("additionalQuestions.yaml", "r", encoding="utf-8") as f:
        YAML_DEFAULTS = yaml.safe_load(f) or {}
except Exception:
    YAML_DEFAULTS = {}

# Explicit answers for known questions
_DEFAULTS = {
    "visa":           "No",
    "sponsorship":    "No",
    "pronoun":        "They/Them",
    "clg":            "Amrita Vishwa Vidyapeetham",
    "college":        "Amrita Vishwa Vidyapeetham",
    "school":         "Amrita Vishwa Vidyapeetham",
    "degree":         "Bachelor's Degree",
    "discipline":     "Computer Science and Engineering",
}

# Fallback texts for free-text questions
_DEFAULT_FALLBACK_TEXT = [
    "1",
    "2",
]

# Preferred dropdown answers for common selects
_DROPDOWN_DEFAULTS = {
    "experience":       "Yes",
    "latency":          "Efficiency",
    "proficiency":      "Professional",
    "country code":     "India (+91)",
    "commute":          "Yes",
    "notice period":    "Immediately",
    "expected salary":  "700000",
    "current salary":   "600000",
    "course":           "No",
    "suitable":         "Yes",
    "authorized":       "Yes",
    "relocate":         "Yes",
    "privacy":          "Yes",
    "interested":       "Yes",
    "interview":        "Yes",  
    "cliking":         "Yes",
    "apply":            "Yes",
    "apply now":        "Yes",
    "ready":            "Yes",
    "remote":           "Yes",
    "onsite":           "Yes",
}

def lookup(label: str):
    """
    Return an explicit answer if a key in YAML_DEFAULTS or _DEFAULTS matches the label.
    """
    q = label.lower()
    for k, ans in YAML_DEFAULTS.items():
        if k.lower() in q:
            return ans
    for k, ans in _DEFAULTS.items():
        if k in q:
            return ans
    return None

def get_answer(label: str, field_type: str) -> str:
    q = (label or "").lower()

    # 1) Expected or current salary / compensation / CTC
    if any(x in q for x in ["expected ctc", "expected salary", "expected compensation"]):
        return "800000"
    if any(x in q for x in ["current ctc", "current salary", "current compensation"]):
        return "600000"

    # 2) Notice period
    if "notice period" in q or ("notice" in q and "period" not in q):
        return "0"

    # 3) Years of experience or work experience
    if "experience" in q and any(w in q for w in ["year", "years", "work"]):
        return random.choice(["1", "2", "3"])

    # 4) YAML or hardcoded overrides
    expl = lookup(label)
    if expl is not None:
        return expl

    # 5) For number fields, return a safe default
    if field_type.lower() in ("number", "tel"):
        return "1"

    # 6) Fallback for text fields
    return random.choice(_DEFAULT_FALLBACK_TEXT)

