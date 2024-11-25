from string import Template

import requests

query = Template('query $name {$method(content: "$content", language: "$language")}')


def ask_modus(
    content: str, language: str, method: str, endpoint: str, api_token: str
) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}",
    }
    new_query = query.safe_substitute(
        name=method[0],
        method=method[1],
        content=repr(content),
        language=language,
    )

    response = requests.post(endpoint, headers=headers, json={"query": new_query})

    print(response.text)
    print(response.text)
    print(response.text)

    data = response.json()
    return data["data"][method[1]]
