import json
import os
from pathlib import Path

from pyaction import PyAction
from pyaction.workflow import annotations as AN
from typing_extensions import List

from discovery import get_pushed_articles
from modus import (
    abstract_article,
    generate_questions,
    simplify_article,
    translate_article,
)

workflow = PyAction()

ALLOWED_METHODS: List[str] = [
    "abstract-article",
    "simplify-article",
    "translate-article",
    "generate-questions",
]


def get_or_create_path(path: str) -> str:
    """gets or creates the path then returns it

    Args:
        path (str): path

    Returns:
        str: path
    """

    if not os.path.exists(path):
        AN.warning(f"Couldn't find `{path}` path in the repo. Creating it!")
        os.makedirs(path)

    return path


@workflow.action
def action(
    github_event_before: str,
    github_event_after: str,
    method: str,
    translate_to: str,
    question_limit: int,
    include_answers: bool,
    path: str,
    hypermode_endpoint: str,
    hypermode_api_token: str,
) -> None:
    article: str = get_pushed_articles(github_event_before, github_event_after)[0]

    AN.notice(f"got the article: {article}")
    AN.notice(str(get_pushed_articles(github_event_before, github_event_after)))
    
    with open(article, "r") as file:
        content = json.dumps(file.read().strip())

    if method == "translate-article":
        result = translate_article(
            content, translate_to, hypermode_endpoint, hypermode_api_token
        )
    elif method == "generate-questions":
        result = generate_questions(
            content,
            question_limit,
            include_answers,
            hypermode_endpoint,
            hypermode_api_token,
        )
    elif method == "simplify-article":
        result = simplify_article(content, hypermode_endpoint, hypermode_api_token)
    elif method == "abstract-article":
        result = abstract_article(content, hypermode_endpoint, hypermode_api_token)
    else:
        AN.error(
            f"`{method}` method is not available. Use one of {list(ALLOWED_METHODS)}."
        )
        raise SystemExit(1)

    write_path = Path(get_or_create_path(path)).joinpath(article)

    with open(write_path, "w") as file:
        file.write(result)
