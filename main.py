import subprocess
from typing import List

from pyaction import PyAction
from pyaction.workflow import annotations as AN
from pyaction.workflow.stream import WorkflowContext

workflow = PyAction()


def get_pushed_articles() -> List[str]:
    try:
        # Run the Git command and capture the output
        AN.notice("Getting the published/modified article.")
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD", "HEAD~1"],
            text=True,  # Ensure output is in string format
            capture_output=True,
            check=True,  # Raise an error if the command fails
        )
        # Split the output by lines to get the list of files
        changed_files = result.stdout.strip().split("\n")
        return changed_files
    except subprocess.CalledProcessError as e:
        AN.error(f"Unable to find the article: {e}")
        raise SystemExit(1)


@workflow.action
def action() -> None:
    article_path: str = get_pushed_articles()[0]

    with open(article_path, "r") as article:
        content: str = article.read()

    workflow.write(
        WorkflowContext(
            {
                "content": content,
            }
        )
    )
