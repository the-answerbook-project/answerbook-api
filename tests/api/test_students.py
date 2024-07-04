def test_can_get_enrolled_students_for_exam(client, student_factory):
    student_factory.create_batch(size=3, exam_id="simple")
    res = client("simple").get("/students")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_student_has_expected_fields(client, student_factory):
    student_ = student_factory(exam_id="simple")
    res = client("simple").get("/students")
    assert res.status_code == 200
    [student] = res.json()
    assert student["cid"] == student_.cid
    assert student["firstname"] == student_.firstname
    assert student["lastname"] == student_.lastname
    assert student["username"] == student_.username
    assert student["degree_code"] == student_.degree_code
