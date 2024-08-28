"""
This script fetches the latest events for a given GitHub username and prints them.

How to use:
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 github_events.py <username>
"""

import sys
import json
# import requests
from urllib import request, error
from rich import print as rich_print


def get_user_acitivity_data(url: str) -> dict:
    """get user data via http

    Args:
        url (str): url path to user data

    Returns:
        dict: response body
    """
    try:
        with request.urlopen(url, timeout=10) as response:
            data = response.read()
            return data
    except error.HTTPError as e:
        print(f"HTTP Error code: {e.code}")
    except error.URLError as e:
        print(f"HTTP Error message: {e.reason}")


def get_latest_events(username):
    """Fetch and display the latest GitHub events for a given username."""
    url = f"https://api.github.com/users/{username}/events"
    # response = requests.get(url, timeout=10)
    response = get_user_acitivity_data(url=url)
    if response:
        event = json.loads(response.decode('utf-8'))
        latest_events = event
        rich_print(f"Latest events for [bold green]{username}[/bold green]:")
        for event in latest_events:
            # Covering only the most common events
            if event['type'] == 'IssueCommentEvent':
                rich_print(f"- :smiley: commented on issue {event['payload']['issue']['number']}")
            elif event['type'] == 'PushEvent':
                rich_print(f"- :smiley: pushed to {event['repo']['name']}")
            elif event['type'] == 'IssuesEvent':
                rich_print(f"- :smiley: created issue {event['payload']['issue']['number']}")
            elif event['type'] == 'WatchEvent':
                rich_print(f"- :smiley: starred {event['repo']['name']}")
            elif event['type'] == 'PullRequestEvent':
                rich_print(f"- :smiley: created pull request {event['payload']['pull_request']['number']}")
            elif event['type'] == 'PullRequestReviewEvent':
                rich_print(f"- :smiley: reviewed pull request {event['payload']['pull_request']['number']}")
            elif event['type'] == 'PullRequestReviewCommentEvent':
                rich_print(f"- :smiley: commented on pull request {event['payload']['pull_request']['number']}")
            elif event['type'] == 'CreateEvent':
                rich_print(f"- :smiley: created {event['payload']['ref_type']} {event['payload']['ref']}")
            else:
                rich_print(f"- :smiley: {event['type']}")
    else:
        rich_print(f"Error fetching events for {username}: {response.status_code}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_latest_events(sys.argv[1])
    else:
        print("Please provide a GitHub username as a command line argument.")
