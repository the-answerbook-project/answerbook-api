import requests


def main():
    res = requests.get("http://localhost:5004/students")
    students = res.json()
    print(students)


if __name__ == "__main__":
    main()
