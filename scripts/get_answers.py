import requests


def main():
    res = requests.get("http://localhost:5004/students")
    students = res.json()
    for student in students:
        res = requests.get(
            f"http://localhost:5004/answers/{student['username']}/question/1/part/1/section/1"
        )
        tasks = res.json()

        if not tasks:
            # Student didn't answer this question
            requests.post(
                f"http://localhost:5004/{student['username']}/marks",
                json={
                    "question": 1,
                    "part": 1,
                    "section": 1,
                    "mark": 0,
                    "feedback": "Not attempted. Your paper shall be burned in the next class.",
                },
            )
            continue

        if tasks[0]["answer"] == "answer":
            requests.post(
                f"http://localhost:5004/{student['username']}/marks",
                json={
                    "question": 1,
                    "part": 1,
                    "section": 1,
                    "mark": 20,
                    "feedback": "Correct! You are a genius.",
                },
            )
            continue


if __name__ == "__main__":
    main()
