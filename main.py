import os
from os.path import join, dirname
from pathlib import Path

from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlretrieve

import requests

from dotenv import load_dotenv

__here__ = Path(os.getcwd())
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
BLOG_NAME = os.getenv('TUMBLR_BLOG_NAME')
DRY_RUN = os.getenv('DRY_RUN', False) == "True"

POSTS_ENDPOINT = f"https://api.tumblr.com/v2/blog/{BLOG_NAME}.tumblr.com/posts/photo"

BLOG_ARCHIVE = __here__ / 'blogs' / BLOG_NAME / 'archive'
BLOG_PATH = __here__ / 'blogs' / BLOG_NAME


def empty_summary():
    summary = {
        'errors': [],
        'skipped': [],
        'completed': [],
    }
    return summary


def print_summary(summary):
    print('Errors:')
    for error in summary['errors']:
        print(f'    {error}')

    num_errors = len(summary['errors'])
    num_skipped = len(summary['skipped'])
    num_completed = len(summary['completed'])

    print('Summary:')
    print(f'    Skipped {num_skipped}')
    print(f'    Completed {num_completed}')
    print(f'    Finished with {num_errors} error(s)')


def make_folders():
    try:
        os.mkdir(BLOG_PATH)
    except FileExistsError:
        pass

        try:
            os.mkdir(BLOG_ARCHIVE)
        except FileExistsError:
            pass


def get_posts(**kwargs):
    params = {
        "api_key": CONSUMER_KEY,
        "npf": True,
        **kwargs
    }
    url = f"{POSTS_ENDPOINT}?{urlencode(params)}"
    response = requests.get(url)
    posts = response.json()["response"]["posts"]
    return posts


def main():
    make_folders()

    summary = empty_summary()
    images = []
    post_urls = []

    posts = get_posts(limit=10)

    for post in posts:

        for t in post["trail"]:

            for block in t["content"]:

                if block["type"] == "image":

                    biggest_width = max([media["width"] for media in block["media"]])
                    image_url = [media for media in block["media"] if media["width"] == biggest_width][0]["url"]

                    filename = image_url.split('/')[-1]
                    file_path = BLOG_ARCHIVE / filename
                    already_downloaded = Path(file_path).is_file()

                    if already_downloaded:
                        summary['skipped'].append(file_path)
                        post_urls.append(post["post_url"])
                        images.append(file_path)
                        print(f'File exists {file_path}')
                        continue

                    try:
                        print(f'Downloading {image_url} to {file_path}')

                        if not DRY_RUN:
                            urlretrieve(image_url, file_path)

                        summary['completed'].append(file_path)
                        images.append(file_path)
                        post_urls.append(post["post_url"])

                    except URLError as e:
                        print(f'    {e.reason}')
                        full_error = f'    {e.reason} {image_url}'
                        summary['errors'].append(full_error)

    print_summary(summary)

    # create html index page

    print('Generating html')

    post_data = zip(images, post_urls)

    posts = [
        f"""
        <div>
            <a href="{image}" rel="noopener noreferrer" target="_blank">
                <img src="{image}" />
            </a>
            <p>
                <a href="{post_url}" rel="noopener noreferrer" target="_blank">{post_url}</a>
            </p>
        </div>
        """
        for image, post_url in post_data
    ]

    posts_html = ''.join(posts)
    content = f'<main id="container">{posts_html}</main>'

    script = """
    <script>
        var macy = Macy({
            container: '#container',
            trueOrder: false,
            waitForImages: true,
            margin: 10,
            columns: 6,
            breakAt: {
                1200: 5,
                940: 3,
                520: 2,
                400: 1
            }
        });
    </script>
    """

    html = f"""
    <!DOCTYPE html>
    <html lang="en" dir="ltr">
      <head>
        <script src="../../macy.js"></script>
        <link rel="stylesheet" href="../../style.css">
        <meta charset="utf-8">
        <title>Tumblr archive</title>
      </head>
      <body>
        {content}
      </body>
      {script}
    </html>
    """

    with open(BLOG_PATH / 'index.html', 'w') as output:
        output.write(html)


if __name__ == "__main__":
    main()
