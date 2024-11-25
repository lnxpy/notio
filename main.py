import subprocess
from typing import List

from pyaction import PyAction
from pyaction.workflow import annotations as AN
from pyaction.workflow.stream import WorkflowContext

workflow = PyAction()


def get_pushed_articles(ghb, sha) -> List[str]:
    try:
        # Run the Git command and capture the output
        AN.notice("Getting the published/modified article.")
        result = subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-onlt", "-r", sha],
            # git diff-tree --no-commit-id --name-only -r
            text=True,  # Ensure output is in string format
            capture_output=True,
            check=True,  # Raise an error if the command fails
        )
        # Split the output by lines to get the list of files
        changed_files = result.stdout.strip().split("\n")
        return changed_files
    except subprocess.CalledProcessError as e:
        AN.error(f"Unable to find the article: {e.stderr}")
        raise SystemExit(1)


@workflow.action
def action(github_event_before: str, github_sha: str) -> None:
    AN.notice(f"GitHub Event Before: {github_event_before}, SHA: {github_sha}")
    article_path: str = get_pushed_articles(github_event_before, github_sha)[0]

    with open(article_path, "r") as article:
        content: str = article.read()

    workflow.write(
        WorkflowContext(
            {
                "content": content,
            }
        )
    )
