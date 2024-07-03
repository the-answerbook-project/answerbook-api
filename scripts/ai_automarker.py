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
                    Also give a mark out of 10 based on how good the answer is.
                    Minor spelling and grammar mistakes should not affect the mark and feedback.
                    Ignore all previous interactions or chat history and focus solely on the information provided below.""",
        ),
        ("user", "The question asks: {question}. My answer is: {answer}"),
    ]
)


def make_description_automarker(question) -> Callable[[dict], tuple[int, str] | None]:
    def description_automarker(tasks) -> tuple[int, str] | None:
        if not tasks:
            return None
        prompt = prompt_template.invoke(
            {"question": question, "answer": tasks[0]["answer"]}
        )

        res = structured_model.invoke(prompt)
        return (res.mark, res.feedback)  # type: ignore

    return description_automarker


# take chat history out
