![banner](media/notio.svg)

## NotioAI
Notio is a CI automated LLM toolkit that gets triggered when a [Hashnode](https://hashnode.com) article gets published/modified. With the help of this pipeline, you can..

- Share the translated version of a newly published Hashnode article.
- Generate questions about the article and push it to GitHub.
- Create an abstraction from the article.
- Simplify the article and share it in a Markdown file on GitHub.

> [!TIP]
> Read [this article](https://blog.imsadra.me/notio-hashnode-post-publication-llm-toolkit) about the development process and full potential of this CI action.

### Setup
Follow these steps to enable Notio for your Hashnode blog.

#### Enable the backup feature
On your Hashnode dashboard, enable the backup feature. This way, Hashnode will push any change you make on your articles.

#### Deploy a personal Hypermode instance
Clone [this Hypermode sample instance](http://github.com/lnxpy/notio-model) and [deploy](https://docs.hypermode.com/deploy) a personal instance for yourself. Then in the dashboard, grab the endpoint URL and take the API Token from the settings.

#### Create secrets
When Hashnode backup is enabled, you can see there is a repository created on your GitHub account called `hashnode`. Navigate to that repository, go to "**Settings**" > "**Secrets and variables**" > "**Actions**" and create the following secrets.

- `HYPERMODE_ENDPOINT_URL`: The endpoint URL taken from the Hypermode dashboard.
- `HYPERMODE_API_TOKEN`: The API token taken from the Hypermode dashboard settings.

### Usage
In the Hashnode backup repository, create the `.github/notio-ci.yml` file and paste the following workflow settings there.

```yml
name: Notio LLM CI

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    name: Running the action
    steps:
      - name: checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
```

Now, use one of the following steps to configure your workflow and satisfy your needs.

#### `translate-article`: Article translation
> Grabs the article and translates it into another language.
```yml
- name: Running Notio
  uses: lnxpy/notio@main
  with:
    method: translate-article
    path: dutch/
    translate_to: Dutch
    hypermode_endpoint: ${{ secrets.HYPERMODE_ENDPOINT }}
    hypermode_api_token: ${{ secrets.HYPERMODE_API_TOKEN }}
```

#### `generate-questions`: Question generation
> Grabs the article and generates questions about the article.
```yml
- name: Running Notio
  uses: lnxpy/notio@main
  with:
    method: generate-questions
    path: questions/
    question_limit: 10
    include_answers: false
    hypermode_endpoint: ${{ secrets.HYPERMODE_ENDPOINT }}
    hypermode_api_token: ${{ secrets.HYPERMODE_API_TOKEN }}
```

#### `abstract-article`: Article abstraction
> Grabs the article and generates an abstraction.

```yml
- name: Running Notio
  uses: lnxpy/notio@main
  with:
    method: abstract-article
    path: abstractions/
    hypermode_endpoint: ${{ secrets.HYPERMODE_ENDPOINT }}
    hypermode_api_token: ${{ secrets.HYPERMODE_API_TOKEN }}
```

#### `simplify-article`: Article simplification
> Grabs the article and simplifies it.

```yml
- name: Running Notio
  uses: lnxpy/notio@main
  with:
    method: simplify-article
    path: simplified_articles/
    hypermode_endpoint: ${{ secrets.HYPERMODE_ENDPOINT }}
    hypermode_api_token: ${{ secrets.HYPERMODE_API_TOKEN }}
```

#### Commit changes
At the end of your workflow, don't forget to add this action usage. It simply commits the generated article into the repository.
```yml
- name: Commiting
  uses: EndBug/add-and-commit@v9
  with:
    default_author: github_actions
    message: 'article updated'
```

### Tech Stacks
- [PyAction](https://pyaction.imsadra.me)
- [Hypermode](https://hypermode.com/)
- Modus CLI

### Running Locally
If you want to run this action locally, follow these steps.

* Clone the repo and `cd` into it.
* Run `uv sync --no-install-project --extra cli`.
* Create the `.env` file filled with the required input parameters.
* Run `uv run pyaction run`.

> [!TIP]
> Check out [this guide](https://pyaction.imsadra.me/docs/concepts/local-running) if you need more details.
