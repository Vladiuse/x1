from dataclasses import dataclass


@dataclass(frozen=True)
class PageContent:
    title: str | None
    description: str | None
    url: str | None
    image: str | None
    type: str | None
