from pathlib import Path

import yaml


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
