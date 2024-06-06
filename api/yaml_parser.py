import base64
import re
from pathlib import Path

import yaml


def convert_images_to_base64(markdown_text: str, base_path: Path):
    def repl(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        attributes = match.group(3) or ""
        full_path = base_path / img_path
        if full_path.is_file():
            with open(full_path, "rb") as img_file:
                ext = full_path.suffix[1:]  # remove leading dot
                base64_str = base64.b64encode(img_file.read()).decode("utf-8")
                return (
                    f"![{alt_text}](data:image/{ext};base64,{base64_str}){attributes}"
                )
        return match.group(0)

    # Improved regex pattern to capture alt text, image path, and optional attributes
    pattern = re.compile(r"!\[(.*?)]\((.*?)\)(\{.*?})?")
    return re.sub(pattern, repl, markdown_text)


def encode_images_in_instructions(data, base_path: Path):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if key == "instructions" and isinstance(value, str):
                new_data[key] = convert_images_to_base64(value, base_path)
            else:
                new_data[key] = encode_images_in_instructions(value, base_path)
        return new_data
    elif isinstance(data, list):
        return [encode_images_in_instructions(item, base_path) for item in data]
    else:
        return data


def construct_mapping(loader, node):
    return {
        str(loader.construct_scalar(k)).replace(" ", "_"): loader.construct_object(v)
        for k, v in node.value
    }


yaml.SafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
)


def parse_yaml(file_path: Path) -> dict:
    with open(file_path, "r") as yaml_conf:
        return yaml.safe_load(yaml_conf)
