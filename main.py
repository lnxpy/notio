import os
from pathlib import Path
from typing import Tuple

from pyaction import PyAction
from pyaction.workflow import annotations as AN
from pyaction.workflow.stream import Dict

from discovery import get_pushed_articles
from modus import ask_modus

workflow = PyAction()

ALLOWED_METHODS: Dict[str, Tuple[str, str]] = {
    "summarize-article": ("SummarizeArticle", "summarizeArticle"),
    "conclude-article": ("ConcludeArticle", "concludeArticle"),
}


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
    path: str,
    translate_to: str,
    hypermode_endpoint: str,
    hypermode_api_token: str,
) -> None:
    if method not in ALLOWED_METHODS.keys():
        AN.error(
            f"`{method}` method is not available. Use one of {list(ALLOWED_METHODS.keys())}."
        )
        raise SystemExit(1)

    article: str = get_pushed_articles(github_event_before, github_event_after)[0]

    with open(article, "r") as file:
        content = file.read()

    result = ask_modus(
        content,
        translate_to,
        ALLOWED_METHODS[method],
        hypermode_endpoint,
        hypermode_api_token,
    )

    write_path = Path(get_or_create_path(path)).joinpath(article)

    with open(write_path, "w") as file:
        file.write(result)
