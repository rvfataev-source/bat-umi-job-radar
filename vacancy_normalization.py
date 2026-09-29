"""
Public portfolio version of the vacancy normalization layer
for the Batumi Job Radar.

The module converts vacancies from different public sources
into one common structure before filtering, deduplication,
classification, and Telegram delivery.

No private accounts, tokens, credentials, or user data
are included in this portfolio version.
"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class NormalizedVacancy:
    source: str
    title: str
    company: Optional[str]
    description: str
    location: Optional[str]
    category: Optional[str]
    remote: bool
    url: str


def clean_text(value: str) -> str:
    if not value:
        return ""

    value = value.strip()
    value = re.sub(r"\s+", " ", value)

    return value


def normalize_location(
    raw_location: str,
) -> Optional[str]:
    if not raw_location:
        return None

    location = clean_text(
        raw_location
    ).lower()

    batumi_keywords = {
        "batumi",
        "ბათუმი",
        "батуми",
    }

    for keyword in batumi_keywords:
        if keyword in location:
            return "Batumi"

    return clean_text(
        raw_location
    )


def detect_remote(
    title: str,
    description: str,
) -> bool:
    text = (
        f"{title} {description}"
    ).lower()

    remote_keywords = {
        "remote",
        "remotely",
        "work from home",
        "удаленно",
        "удалённо",
        "дистанционно",
        "დისტანციური",
    }

    return any(
        keyword in text
        for keyword in remote_keywords
    )


def detect_category(
    title: str,
    description: str,
) -> Optional[str]:
    text = (
        f"{title} {description}"
    ).lower()

    categories = {
        "SMM": [
            "smm",
            "social media",
            "социальные сети",
            "соцсети",
        ],
        "Marketing": [
            "marketing",
            "marketer",
            "маркетолог",
            "маркетинг",
        ],
        "Content": [
            "content creator",
            "content manager",
            "copywriter",
            "контент",
            "копирайтер",
        ],
        "Advertising": [
            "media buyer",
            "targetologist",
            "таргетолог",
            "facebook ads",
            "meta ads",
        ],
        "Design": [
            "graphic designer",
            "designer",
            "дизайнер",
        ],
    }

    for category, keywords in categories.items():
        if any(
            keyword in text
            for keyword in keywords
        ):
            return category

    return None


def normalize_vacancy(
    source: str,
    title: str,
    company: str,
    description: str,
    location: str,
    url: str,
) -> NormalizedVacancy:
    cleaned_title = clean_text(
        title
    )

    cleaned_description = clean_text(
        description
    )

    return NormalizedVacancy(
        source=clean_text(source),
        title=cleaned_title,
        company=(
            clean_text(company)
            if company
            else None
        ),
        description=cleaned_description,
        location=normalize_location(
            location
        ),
        category=detect_category(
            cleaned_title,
            cleaned_description,
        ),
        remote=detect_remote(
            cleaned_title,
            cleaned_description,
        ),
        url=clean_text(url),
    )


if __name__ == "__main__":
    example = normalize_vacancy(
        source="Example Source",
        title="SMM Manager",
        company="Example Company",
        description=(
            "Looking for an SMM specialist "
            "to manage social media content "
            "and advertising campaigns."
        ),
        location="Batumi, Georgia",
        url=(
            "https://example.com/"
            "vacancy/123"
        ),
    )

    print(example)
