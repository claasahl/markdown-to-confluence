# markdown-to-confluence

Converts and deploys a Markdown file to Confluence.

This project was created to sync [Journal](https://duo-labs.github.io/journal/) posts to Confluence as part of the CI process. 

# Installation

To install the project, you need to first install the dependencies:

```
pip install -r requirements.txt
```

Alternatively, you can use the provided Dockerfile:

```
docker build -t markdown-to-confluence .
```

# Usage

```
usage: markdown-to-confluence.py [-h] [--git GIT] [--api_url API_URL]
                                 [--username USERNAME] [--password PASSWORD]
                                 [--space SPACE] [--ancestor_id ANCESTOR_ID]
                                 [--header HEADER] [--dry-run]
                                 [posts [posts ...]]

Converts and deploys a markdown post to Confluence

positional arguments:
  posts                 Individual files to deploy to Confluence

optional arguments:
  -h, --help            show this help message and exit
  --api_url API_URL     The URL to the Confluence API (e.g.
                        https://wiki.example.com/rest/api/)
  --username USERNAME   The username for authentication to Confluence
                        (default: env('CONFLUENCE_USERNAME'))
  --password PASSWORD   The password for authentication to Confluence
                        (default: env('CONFLUENCE_PASSWORD'))
  --space SPACE         The Confluence space where the post should reside
                        (default: env('CONFLUENCE_SPACE'))
  --title TITLE         The title of the Confluence page
                        (default: env('CONFLUENCE_TITLE'))                
  --ancestor_id ANCESTOR_ID
                        The Confluence ID of the parent page to place posts
                        under (default: env('CONFLUENCE_ANCESTOR_ID'))

```

### Deploying Posts On-Demand

You may wish to deploy a post on-demand, rather than building this process into your CI/CD pipeline. To do this, just put the filenames of the posts you wish to deploy to Confluence as arguments:

```
markdown-to-confluence.py /path/to/your/post.md
```