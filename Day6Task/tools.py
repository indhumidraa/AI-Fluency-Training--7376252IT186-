# tools.py
# Tools and their shared JSON schemas for the College Study Planner.

SCHEMAS = {
    "get_subject_info": {
        "name": "get_subject_info",
        "description": "Look up information about a college subject.",
        "parameters": {
            "type": "object",
            "properties": {
                "subject": {
                    "type": "string",
                    "description": "The name of the college subject."
                }
            },
            "required": ["subject"],
            "additionalProperties": False
        },
        "strict": True
    },

    "calculate_study_hours": {
        "name": "calculate_study_hours",
        "description": "Calculate recommended daily study hours for a subject.",
        "parameters": {
            "type": "object",
            "properties": {
                "difficulty": {
                    "type": "string",
                    "enum": ["easy", "medium", "hard"],
                    "description": "Difficulty level of the subject."
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days available for studying."
                }
            },
            "required": ["difficulty", "days"],
            "additionalProperties": False
        },
        "strict": True
    }
}


SUBJECTS = {
    "data structures": {
        "credits": 4,
        "difficulty": "hard"
    },
    "database management systems": {
        "credits": 3,
        "difficulty": "medium"
    },
    "computer networks": {
        "credits": 3,
        "difficulty": "medium"
    },
    "python programming": {
        "credits": 4,
        "difficulty": "easy"
    }
}


def get_subject_info(subject):
    """Return information about a college subject."""
    key = subject.strip().lower()

    if key not in SUBJECTS:
        return f"Subject '{subject}' was not found in the study planner database."

    info = SUBJECTS[key]

    return (
        f"{subject}: {info['credits']} credits, "
        f"difficulty = {info['difficulty']}."
    )


def calculate_study_hours(difficulty, days):
    """Calculate recommended study hours per day."""
    hours_by_difficulty = {
        "easy": 6,
        "medium": 10,
        "hard": 15
    }

    total_hours = hours_by_difficulty[difficulty]

    daily_hours = total_hours / days

    return (
        f"For a {difficulty} subject, the recommended total is "
        f"{total_hours} hours. Over {days} days, study about "
        f"{daily_hours:.1f} hours per day."
    )


TOOL_FUNCTIONS = {
    "get_subject_info": get_subject_info,
    "calculate_study_hours": calculate_study_hours
}