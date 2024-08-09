from datetime import datetime, timezone

from freezegun import freeze_time

mark_posting_ts = datetime(2024, 5, 1, 14, 22, tzinfo=timezone.utc)
valid_section = {"question": 1, "part": 1, "section": 1}


def test_can_get_marks(client_, assessment_factory):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[
            dict(username="hpotter", with_marks=2),
            dict(username="hgranger", with_marks=1),
        ],
    )

    res = client_.get(f"/{assessment.code}/marks")
    assert res.status_code == 200
    assert len(res.json()) == 3


def test_can_filter_marks_by_student_username(client_, assessment_factory):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[
            dict(username="hpotter", with_marks=2),
            dict(username="hgranger", with_marks=1),
        ],
    )

    res = client_.get(
        f"/{assessment.code}/marks", params={"student_username": "hpotter"}
    )
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_response_mark_has_expected_fields(client_, assessment_factory):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[dict(username="hpotter", with_marks=1)],
    )

    res = client_.get(f"/{assessment.code}/marks")
    assert res.status_code == 200
    assert len(res.json()) == 1
    [mark] = res.json()
    assert "question" in mark
    assert "part" in mark
    assert "section" in mark
    assert "marker" in mark
    assert "username" in mark
    assert "mark" in mark
    assert "feedback" in mark
    assert "history" in mark


def test_gets_empty_list_response_if_no_marks_exist_for_assessment(client_):
    res = client_.get("/y2023_12345_exam/marks")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_mark_include_mark_history(client_, assessment_factory):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[
            dict(username="hpotter", with_marks=[dict(question=1, with_history=5)])
        ],
    )
    res = client_.get(f"/{assessment.code}/marks")
    assert res.status_code == 200
    [mark] = res.json()
    assert len(mark["history"]) == 5


def test_mark_history_has_expected_fields(client_, assessment_factory):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[
            dict(username="hpotter", with_marks=[dict(question=1, with_history=1)])
        ],
    )
    res = client_.get(f"/{assessment.code}/marks")
    assert res.status_code == 200
    [mark] = res.json()
    [history_entry] = mark["history"]
    assert "mark" in history_entry
    assert "feedback" in history_entry
    assert "marker" in history_entry


def test_cannot_post_to_marks_with_no_mark_and_no_feedback(client_, assessment_factory):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[dict(username="hpotter")],
    )
    res = client_.post(
        f"/{assessment.code}/marks",
        json={**valid_section, "username": "hpotter", "feedback": None, "mark": None},
    )

    assert res.status_code == 400
    assert (
        res.json()["detail"]
        == "At least one between 'mark' and 'feedback' is required."
    )


def test_posting_mark_without_feedback_updates_root_mark(client_, assessment_factory):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[
            dict(username="hpotter", with_marks=[dict(**valid_section, with_history=1)])
        ],
    )
    [student] = assessment.candidates
    [mark] = student.marks

    with freeze_time(mark_posting_ts):
        res = client_.post(
            f"/{assessment.code}/marks",
            json={**valid_section, "username": "hpotter", "mark": 2.5},
        )

    assert res.status_code == 200
    res_mark = res.json()
    assert res_mark["mark"] == 2.5
    assert res_mark["marker"] == "adumble"  # Currently implicit
    assert res_mark["feedback"] == mark.feedback
    assert res_mark["timestamp"] == "2024-05-01T14:22:00+00:00"


def test_posting_feedback_without_mark_updates_root_feedback(
    client_, assessment_factory
):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[dict(username="hpotter", with_marks=[dict(**valid_section)])],
    )
    [student] = assessment.candidates
    [mark] = student.marks

    with freeze_time(mark_posting_ts):
        res = client_.post(
            f"/{assessment.code}/marks",
            json={**valid_section, "username": "hpotter", "feedback": "Some comment"},
        )

    assert res.status_code == 200
    res_mark = res.json()
    assert res_mark["mark"] == mark.mark
    assert res_mark["marker"] == "adumble"  # Currently implicit
    assert res_mark["feedback"] == "Some comment"
    assert res_mark["timestamp"] == "2024-05-01T14:22:00+00:00"


def test_posting_mark_and_feedback_for_section(client_, assessment_factory):
    assessment = assessment_factory(
        code="y2023_12345_exam", with_students=[dict(username="hpotter")]
    )
    res = client_.post(
        f"/{assessment.code}/marks",
        json={
            **valid_section,
            "username": "hpotter",
            "mark": 2.5,
            "feedback": "Some comment",
        },
    )

    assert res.status_code == 200
    mark = res.json()
    assert mark["mark"] == 2.5
    assert mark["marker"] == "adumble"  # Currently implicit
    assert mark["feedback"] == "Some comment"


def test_posting_mark_without_feedback_adds_to_mark_history(
    client_, assessment_factory
):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[
            dict(username="hpotter", with_marks=[dict(**valid_section, with_history=1)])
        ],
    )
    with freeze_time(mark_posting_ts):
        res = client_.post(
            f"/{assessment.code}/marks",
            json={**valid_section, "username": "hpotter", "mark": 2.5},
        )

    assert res.status_code == 200
    history = res.json()["history"]
    assert len(history) == 2
    [_, latest_mark] = history
    assert latest_mark["marker"] == "adumble"  # Currently implicit
    assert latest_mark["timestamp"] == "2024-05-01T14:22:00+00:00"
    assert latest_mark["feedback"] == None
    assert latest_mark["mark"] == 2.5


def test_posting_feedback_without_mark_adds_to_mark_history(
    client_, assessment_factory
):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[
            dict(username="hpotter", with_marks=[dict(**valid_section, with_history=1)])
        ],
    )
    with freeze_time(mark_posting_ts):
        res = client_.post(
            f"/{assessment.code}/marks",
            json={**valid_section, "username": "hpotter", "feedback": "Some comment"},
        )

    assert res.status_code == 200
    history = res.json()["history"]
    assert len(history) == 2
    [_, latest_mark] = history
    assert latest_mark["marker"] == "adumble"  # Currently implicit
    assert latest_mark["timestamp"] == "2024-05-01T14:22:00+00:00"
    assert latest_mark["feedback"] == "Some comment"
    assert latest_mark["mark"] == None


# ANSWERS =================================


def test_can_get_answers(client_, assessment_factory):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[dict(username="hpotter", with_answers=5)],
    )
    res = client_.get(f"/{assessment.code}/answers")
    assert res.status_code == 200
    assert len(res.json()) == 5


def test_can_filter_answers_by_student(client_, assessment_factory):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[
            dict(username="hpotter", with_answers=2),
            dict(username="hgranger", with_answers=5),
        ],
    )
    res = client_.get(
        f"/{assessment.code}/answers", params={"student_username": "hpotter"}
    )
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_gets_empty_list_response_if_no_answers_exist_for_assessment(
    client_, assessment_factory
):
    assessment = assessment_factory(code="y2023_12345_exam")
    res = client_.get(f"/{assessment.code}/answers")
    assert res.status_code == 200
    assert len(res.json()) == 0


def test_response_answer_has_expected_fields(client_, assessment_factory):
    assessment = assessment_factory(
        code="y2023_12345_exam",
        with_students=[dict(username="hpotter", with_answers=1)],
    )

    res = client_.get(f"/{assessment.code}/answers")
    assert res.status_code == 200
    [answer] = res.json()
    assert "username" in answer
    assert "question" in answer
    assert "part" in answer
    assert "section" in answer
    assert "task" in answer
    assert "answer" in answer
