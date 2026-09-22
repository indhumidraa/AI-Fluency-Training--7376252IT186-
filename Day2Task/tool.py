def course_info(course):
    courses = {
        "CS101": {
            "name": "Computer Science Fundamentals",
            "fee": 12000
        },
        "AI202": {
            "name": "Artificial Intelligence",
            "fee": 18000
        },
        "ML303": {
            "name": "Machine Learning",
            "fee": 15000
        }
    }

    course = course.strip().upper()

    if course in courses:
        info = courses[course]
        return (
            f"{course}: {info['name']}, "
            f"Fee = Rs. {info['fee']}"
        )

    return f"Course {course} not found."