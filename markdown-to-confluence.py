import argparse
import logging
import os
import requests
import sys

from confluence import Confluence
from convert import convtoconf, parse
"""Deploys Markdown posts to Confluenceo

This script is meant to be executed as either part of a CI/CD job or on an
adhoc basis.
"""

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

SUPPORTED_FORMATS = ['.md']



def parse_args():
    parser = argparse.ArgumentParser(
        description='Converts and deploys a markdown post to Confluence')
    parser.add_argument(
        '--api_url',
        dest='api_url',
        default=os.getenv('CONFLUENCE_API_URL'),
        help=
        'The URL to the Confluence API (e.g. https://wiki.example.com/rest/api/)'
    )
    parser.add_argument(
        '--username',
        dest='username',
        default=os.getenv('CONFLUENCE_USERNAME'),
        help=
        'The username for authentication to Confluence (default: env(\'CONFLUENCE_USERNAME\'))'
    )
    parser.add_argument(
        '--password',
        dest='password',
        default=os.getenv('CONFLUENCE_PASSWORD'),
        help=
        'The password for authentication to Confluence (default: env(\'CONFLUENCE_PASSWORD\'))'
    )
    parser.add_argument(
        '--space',
        dest='space',
        default=os.getenv('CONFLUENCE_SPACE'),
        help=
        'The Confluence space where the post should reside (default: env(\'CONFLUENCE_SPACE\'))'
    )
    parser.add_argument(
        '--title',
        dest='title',
        default=os.getenv('CONFLUENCE_TITLE'),
        help=
        'The title of the Confluence page (default: env(\'CONFLUENCE_TITLE\'))'
    )
    parser.add_argument(
        '--ancestor_id',
        dest='ancestor_id',
        default=os.getenv('CONFLUENCE_ANCESTOR_ID'),
        help=
        'The Confluence ID of the parent page to place posts under (default: env(\'CONFLUENCE_ANCESTOR_ID\'))'
    )
    parser.add_argument(
        'posts',
        type=str,
        nargs='*',
        help=
        'Individual files to deploy to Confluence'
    )

    args = parser.parse_args()

    if not args.api_url:
        log.error('Please provide a valid API URL')
        sys.exit(1)

    return parser.parse_args()


def deploy_file(post_path, args, confluence):
    """Creates or updates a file in Confluence

    Arguments:
        post_path {str} -- The absolute path of the post to deploy to Confluence
        args {argparse.Arguments} -- The parsed command-line arguments
        confluence {confluence.Confluence} -- The Confluence API client
    """

    _, ext = os.path.splitext(post_path)
    if ext not in SUPPORTED_FORMATS:
        log.info('Skipping {} since it\'s not a supported format.'.format(
            post_path))
        return

    try:
        markdown = parse(post_path)
    except Exception as e:
        log.error(
            'Unable to process {}. Normally not a problem, but here\'s the error we received: {}'
            .format(post_path, e))
        return

    # Normalize the content into whatever format Confluence expects
    html, attachments = convtoconf(markdown)

    static_path = os.path.join('.', 'static')
    for i, attachment in enumerate(attachments):
        attachments[i] = os.path.join(static_path, attachment.lstrip('/'))

    title = args.title
    ancestor_id = args.ancestor_id
    space = args.space

    page = confluence.exists(title=title,
                             ancestor_id=ancestor_id,
                             space=space)
    if page:
        confluence.update(page['id'],
                          content=html,
                          title=title,
                          space=space,
                          ancestor_id=ancestor_id,
                          page=page,
                          attachments=attachments)
    else:
        confluence.create(content=html,
                          title=title,
                          space=space,
                          ancestor_id=ancestor_id,
                          attachments=attachments)


def main():
    args = parse_args()

    confluence = Confluence(api_url=args.api_url,
                            username=args.username,
                            password=args.password)

    changed_posts = [os.path.abspath(post) for post in args.posts]
    for post_path in changed_posts:
        if not os.path.exists(post_path) or not os.path.isfile(post_path):
            log.error('File doesn\'t exist: {}'.format(post_path))
            sys.exit(1)

    for post in changed_posts:
        log.info('Attempting to deploy {}'.format(post))
        deploy_file(post, args, confluence)


if __name__ == '__main__':
    main()
