from typing import Callable

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI


class MarkFeedback(BaseModel):
    mark: int = Field(description="A mark out of 10")
    feedback: str = Field(description="Feedback based on student's answer")


model = ChatOpenAI(model="gpt-4")
structured_model = model.with_structured_output(MarkFeedback)

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a marker for an exam question. Give feedback on the student's answer.
                    Also give a mark out of {max_mark} based on how good the answer is.
                    Minor spelling and grammar mistakes should not affect the mark and feedback.
                    Limit feedback to 15 completion tokens or less.
                    Ignore all previous interactions or chat history and focus solely on the information provided below.""",
        ),
        ("user", "The question asks: {question}. My answer is: {answer}"),
    ]
)


def make_value_explanation_automarker(
    question: str, model_ans: float
) -> Callable[[dict], tuple[int, str] | None]:
    def value_explanation_automarker(tasks) -> tuple[int, str] | None:
        if not tasks:
            return None

        mark = 0
        feedback = ""

        student_ans = float(tasks[0]["answer"])
        epsilon = 1

        if abs(model_ans - student_ans) < epsilon:
            mark += 2
            feedback += "You calculated the value correctly. "
        else:
            feedback += "Your calculated value is incorrect. "

        if len(tasks) < 2:
            feedback += "You failed to enter an explanation. "
        else:
            prompt = prompt_template.invoke(
                {
                    "max_mark": 8,
                    "question": question,
                    "answer": f"My value is: ${tasks[0]["answer"]}. My explanation is: ${tasks[1]["answer"]}",
                }
            )

            res: MarkFeedback = structured_model.invoke(prompt)  # type: ignore
            mark += res.mark
            feedback += res.feedback
        return (mark, feedback)

    return value_explanation_automarker


def make_prompt_automarker(
    question: str, max_mark: int
) -> Callable[[dict], tuple[int, str] | None]:
    def prompt_automarker(tasks) -> tuple[int, str] | None:
        if not tasks:
            return None
        prompt = prompt_template.invoke(
            {"max_mark": max_mark, "question": question, "answer": tasks[0]["answer"]}
        )

        res = structured_model.invoke(prompt)
        return (res.mark, res.feedback)  # type: ignore

    return prompt_automarker


# take chat history out


# task 1 calculate
# task 2 use task 1 result and use ai
