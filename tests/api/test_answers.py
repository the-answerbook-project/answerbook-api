###
# NOTE: QPS: Question Part Section
###
from api.factories.student import StudentFactory


def test_can_get_a_part_for_student(client, student_factory: StudentFactory):
    student_ = student_factory(exam_id="simple")
    res = client("random").get("/answers/hpotter/question/1/part/1/section/1")
    assert res.status_code == 200
