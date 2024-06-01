from pydantic import BaseModel, model_validator
from pydantic.networks import UrlConstraints
from pydantic_core import Url
from typing_extensions import Annotated

from src.exceptions.api import ModelValidationException

RepoUrl = Annotated[
    Url, UrlConstraints(max_length=2083, allowed_schemes=["ssh", "https"])
]


class RepoValidated(BaseModel):
    url: RepoUrl
    ref: str | None = None

    def __str__(self):
        return f"Repo <{self.url}>"

    @model_validator(mode="after")
    def validate(self):
        if not any([self.ref]):
            raise ModelValidationException(
                "None of the ref types [branch, hash, ref] are presented"
            )
        return self

    def dump(self) -> dict:
        return {"url": self.url, "hash": self.ref}