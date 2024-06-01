from dataclasses import dataclass


@dataclass
class ToolConfig:
    """"""

    args: list[str]
    bin: str
    rule_path: str

    timeout: int
    max_unpacked_size: int
