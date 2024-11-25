from pyaction import PyAction

workflow = PyAction()


@workflow.action
def action(article_path: str):
    workflow.write(
        {
            "article": article_path,
        }
    )
