import json
from importlib import resources


def load_rating_scale(name: str) -> dict[str, float]:
    path = resources.files(__package__).joinpath(f"{name}.json")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
