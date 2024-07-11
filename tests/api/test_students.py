def test_can_get_enrolled_students_for_exam(client, assessment_factory):
    assessment_factory(exam_code="simple", with_students=3)
    res = client("simple").get("/students")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_student_has_expected_fields(client, assessment_factory):
    assessment = assessment_factory(exam_code="simple", with_students=1)
    [student_] = assessment.candidates
    res = client("simple").get("/students")
    assert res.status_code == 200
    [student] = res.json()
    assert student["cid"] == student_.cid
    assert student["firstname"] == student_.firstname
    assert student["lastname"] == student_.lastname
    assert student["username"] == student_.username
    assert student["degree_code"] == student_.degree_code
