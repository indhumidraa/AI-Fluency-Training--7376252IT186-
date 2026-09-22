def read_courses():
    courses = []

    with open("expenses.txt", "r") as file:
        for line in file:
            name, price = line.strip().split(",")

            courses.append({
                "name": name.strip(),
                "price": int(price.strip())
            })

    return courses


def workflow(question):
    budget = 30000
    courses = read_courses()

    results = []

    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):

            total = courses[i]["price"] + courses[j]["price"]

            if total <= budget:
                results.append(
                    f"{courses[i]['name']} + "
                    f"{courses[j]['name']} = Rs. {total}"
                )

    if not results:
        return "No two courses fit within Rs. 30,000."

    return "\n".join(results)


QUESTION = (
    "I can pay Rs. 30,000. "
    "Which two courses can I take together?"
)

print("Q:", QUESTION)
print("\nWorkflow:")
print(workflow(QUESTION))