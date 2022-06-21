import json
import os
import re
import sys
import time
import requests
from typing import Any, Dict, List, Union


MAX_PAGE_NUMBER: int = 3
SEARCH_ENDPOINT: str = "https://bg.annapurnapost.com/api/search"
SEARCH_QUERIES: List[str] = ["पाकिस्तान", "पेट्रोलियम"]
LOGS_DIRECTORY = os.path.join(os.getcwd(), "logs")  # directory to store all log files
POSTS_DIRECTORY = os.path.join(
    os.getcwd(), "posts"
)  # directory to store all scraped posts


def remove_html(html: str) -> str:
    """Remove html tags from a string"""
    html_re = re.compile("<[^>]*>")
    return html_re.sub("", html)


def make_directory(path: str) -> None:
    """Create a directory if it doesn't exist"""
    if not os.path.exists(path):
        os.mkdir(path)


def create_log(file_name: str, data: Any) -> None:
    # creating directory to store all log files if it already doesn't exist
    make_directory(LOGS_DIRECTORY)
    with open(os.path.join(LOGS_DIRECTORY, file_name), "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_log_file(file_path: str) -> Union[Dict[str, str], None]:
    # if there is no log file created yet, return None
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def read_posts(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, "r") as file:
        return json.load(file)


def save_posts(file_path: str, posts: List[Dict[str, str]]) -> None:
    # create a directory to store all posts if it doesn't exist
    make_directory(POSTS_DIRECTORY)
    all_posts = [*posts]
    if os.path.exists(file_path):
        # if there is already a file, read it and append the existing posts and new posts
        # so if we run the script from page 2, we will get all the existing posts of page 1
        existing_posts = read_posts(file_path)
        all_posts = [*existing_posts, *posts]
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(all_posts, file, ensure_ascii=False, indent=4)


def fetch_posts(searh_query: str, page_number: int) -> List[Dict[str, str]]:
    response = requests.get(f"{SEARCH_ENDPOINT}?title={searh_query}&page={page_number}")
    response_json = response.json()
    posts = response_json["data"]["items"]
    html_removed_posts = [
        {**post, "content": remove_html(post["content"])} for post in posts
    ]
    return html_removed_posts


def fetch_multiple_page_posts(search_queries: List[str]) -> None:
    for search_query in search_queries:
        exit_log = read_log_file(
            os.path.join(LOGS_DIRECTORY, f"{search_query}_log.json")
        )
        # if there is a log file for this search query, get the last exited page number for the search query
        current_page: int = 1 if exit_log is None else int(exit_log["exited_page"])
        if current_page > 1:
            print(
                f"Fetching from page {current_page} since the program was last exited on this page"
            )
        while current_page <= MAX_PAGE_NUMBER:
            try:
                print(f"Fetching {search_query} posts from page {current_page}")
                posts = fetch_posts(search_query, current_page)
                save_posts(
                    os.path.join(POSTS_DIRECTORY, f"{search_query}_posts.json"), posts
                )
                current_page += 1
                time.sleep(3)  # remove this line if you want to fetch posts faster
            except KeyboardInterrupt:
                print(f"Stop fetching posts from page {current_page}")
                log_file_path = os.path.join(LOGS_DIRECTORY, f"{search_query}_log.json")
                create_log(log_file_path, {"exited_page": current_page})
                sys.exit(1)


def main() -> None:
    fetch_multiple_page_posts(SEARCH_QUERIES)


if __name__ == "__main__":
    main()
