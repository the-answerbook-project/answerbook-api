import re

import pytest

from api.yaml_parser import convert_images_to_base64
from tests.conftest import ASSESSMENTS_DIR


@pytest.mark.parametrize(
    "md_text, expected_pattern",
    [
        (
            "![alt-text](starwars.jpg){: attributes}",
            r"!\[alt-text\]\(data:image/jpg;base64,.*G4OC2kTtJz78BzGjaKcb8BpzWjcG\+.*\)\{: attributes\}",
        ),
        (
            "![alt-text](starwars.jpg) {: attributes}",
            r"!\[alt-text\]\(data:image/jpg;base64,.*G4OC2kTtJz78BzGjaKcb8BpzWjcG\+.*\) \{: attributes\}",
        ),
        (
            "![alt-text](starwars.jpg)",
            r"!\[alt-text\]\(data:image/jpg;base64,.*G4OC2kTtJz78BzGjaKcb8BpzWjcG\+.*\)",
        ),
        (
            "Some *bold* md text",
            r"Some \*bold\* md text",
        ),
    ],
)
def test_conversion_of_images_to_base64(md_text: str, expected_pattern: str):
    base_path = ASSESSMENTS_DIR / "image_in_question_spec" / "images"
    encoded = convert_images_to_base64(md_text, base_path)
    assert re.compile(expected_pattern).match(encoded)
