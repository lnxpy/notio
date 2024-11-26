from string import Template

import requests

query = Template('query $name {$method(content: $content, language: "$language")}')


def abstract_article(content: str, endpoint: str, api_token: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    query = Template("query $name {$method(content: $content)}")

    new_query = query.safe_substitute(
        name="AbstractArticle", method="abstractArticle", content=content
    )

    response = requests.post(endpoint, headers=headers, json={"query": new_query})

    data = response.json()
    return data["data"]["abstractArticle"]


def simplify_article(content: str, endpoint: str, api_token: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    query = Template("query $name {$method(content: $content)}")

    new_query = query.safe_substitute(
        name="SimplifyArticle", method="simplifyArticle", content=content
    )

    response = requests.post(endpoint, headers=headers, json={"query": new_query})

    data = response.json()
    return data["data"]["simplifyArticle"]


def translate_article(
    content: str, language: str, endpoint: str, api_token: str
) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    query = Template('query $name {$method(content: $content, language: "$language")}')

    new_query = query.safe_substitute(
        name="TranslateArticle",
        method="translateArticle",
        content=content,
        language=language,
    )

    response = requests.post(endpoint, headers=headers, json={"query": new_query})

    data = response.json()
    return data["data"]["translateArticle"]


def generate_questions(
    content: str, limit: int, include_answers: bool, endpoint: str, api_token: str
) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    query = Template(
        'query $name {$method(content: $content, limit: "$limit", include_answers: $include_answers)}'
    )

    new_query = query.safe_substitute(
        name="GenerateQuestions",
        method="generateQuestions",
        content=content,
        limit=limit,
        include_answers="true" if include_answers else "false",
    )

    response = requests.post(endpoint, headers=headers, json={"query": new_query})

    data = response.json()
    return data["data"]["generateQuestions"]
