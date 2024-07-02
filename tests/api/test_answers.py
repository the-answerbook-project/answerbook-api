###
# NOTE: QPS: Question Part Section
###
from api.factories.student import StudentFactory


def test_can_get_a_part_for_student(client, answer_factory):
    answer_factory(
        exam_id="y2023_12345_exam", question=1, part=1, section=1, username="hpotter"
    )
    res = client("y2023_12345_exam").get("/answers/hpotter/question/1/part/1/section/1")
    assert res.status_code == 200
    assert len(res.json()) == 1
