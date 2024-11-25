import subprocess
from typing import List

from pyaction.workflow import annotations as AN


def get_pushed_articles(github_event_before, github_event_after) -> List[str]:
    try:
        # Run the Git command and capture the output
        AN.notice("Getting the published/modified article.")
        subprocess.run(
            [
                "git",
                "config",
                "--global",
                "--add",
                "safe.directory",
                "/github/workspace",
            ]
        )
        result = subprocess.run(
            [
                "git",
                "diff-tree",
                "--no-commit-id",
                "--name-only",
                github_event_before,
                github_event_after,
            ],
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
