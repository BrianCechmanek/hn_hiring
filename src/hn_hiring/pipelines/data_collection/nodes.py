"""
This is a boilerplate pipeline 'data_collection'
generated using Kedro 0.18.12
"""

import logging
from datetime import datetime
from random import randint
from time import sleep
from typing import Any, Dict, List, Optional, Tuple

import requests

logger = logging.getLogger(__name__)


def get_user(user: str = "whoishiring") -> Dict[str, Any]:
    """For any user, usually whoishiring, get a list of their submission.
    The"""
    try:
        response = requests.get(
            f"https://hacker-news.firebaseio.com/v0/user/{user}.json?print=pretty"
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise e


def get_user_submitted(user: str = "whoishiring") -> List[int]:
    """For any user, get the List[id] of their submitted."""
    try:
        response = requests.get(
            f"https://hacker-news.firebaseio.com/v0/user/{user}.json?print=pretty"
        )
        response.raise_for_status()
        return response.json().get("submitted")
    except requests.exceptions.RequestException as e:
        raise e


def get_users_karma(posts: Dict[str, Any]) -> Dict[int, Tuple[str, int]]:
    """for each post, return the company name and the karma count (for that post).
    Duplicate company posts are not yet handled.

    args:
        posts: {str(id): {comment_response}}
    Returns:
        company_karma: {id: (company_name, karma_count)}"""
    ...

    users_karma = {}
    logger.debug(f"Collecting karma for {len(posts) = }")
    for id, post in posts.items():
        user = post.get("by")
        user_profile = get_user(user=user)
        if user_profile:
            users_karma[id] = user_profile["karma"]
        else:
            logger.debug(f"skipping {user = }, {id = } due to {type(user_profile)}")

    return users_karma


def get_submitted(post: Dict[str, Any]) -> List[int]:
    return post["submitted"]


def get_post_by_id(id: int) -> Dict[str, Any]:
    try:
        response = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=pretty"
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise e


def is_whos_hiring(post: Dict[str, Any]) -> bool:
    """The whoishiring setup is pretty consistent - back as far as 2017.
    Don't need to be too robust on matching at this time."""

    s = "who is hiring"

    def contains_s(title, s):
        return s.lower() in title.lower()

    try:
        return (post.get("type") == "story") and (contains_s(post.get("title"), s))
    except AttributeError:
        logger.debug(f"Post {post.get('id')} has no title: {post.get('title')}")
        return False


# BC: TODO - get this running async
# when uncommented, will raise RuntimeError: asyncio.run() cannot be
# called from a running event loop
# apparently a well known issue:
# https://stackoverflow.com/questions/56154176/
# runtimeerror-asyncio-run-cannot-be-called-from-a-
# running-event-loop-in-spyd
# async def get_whos_hiring(
#     ids: List[int],
# ) -> Tuple[List[int], List[int], Dict[str, Any]]:
#     is_hiring_ids = []
#     not_hiring_ids = []
#     is_hiring_posts = {}

#     for id in ids:
#         post = await get_post_by_id(id=id)
#         if is_whos_hiring(post):
#             is_hiring_ids.append(id)
#             is_hiring_posts[id] = post
#         else:
#             not_hiring_ids.append(id)

#     return (is_hiring_ids, not_hiring_ids, is_hiring_posts)


def get_whos_hiring(
    ids: List[int],
) -> Tuple[List[int], List[int], Dict[str, Any]]:
    is_hiring_ids = []
    not_hiring_ids = []
    is_hiring_posts = {}

    for id in ids:
        try:
            post = get_post_by_id(id=id)
            if is_whos_hiring(post):
                is_hiring_ids.append(id)
                is_hiring_posts[id] = post
            else:
                not_hiring_ids.append(id)
        except RuntimeError:
            # allow any exception and move on
            continue

    return (is_hiring_ids, not_hiring_ids, is_hiring_posts)


def ids_to_str(ids: List[int]) -> str:
    """Kedro textDataSet requires string inputs. map int->str"""
    return ", ".join(map(str, ids))


def filter_posts_by_dates(
    posts: Dict[str, Any], filter_dates: List[str]
) -> Dict[str, Any]:
    # the desired post dates (of Aug 2023, jul 2023, Aptil 2014)
    def date_to_dt(date: str) -> List[datetime]:
        # convert string to datetime object
        return datetime.strptime(date, "%B %Y")

    # the existing unix timestamps
    def ts_to_dt(ts):
        return datetime.fromtimestamp(ts)

    filter_datetimes = list(map(date_to_dt, filter_dates))

    post_timestamps = [v["time"] for _, v in posts.items()]
    post_datetimes = list(map(ts_to_dt, post_timestamps))

    filtered_datetimes = [
        post_dt
        for post_dt in post_datetimes
        if any(
            post_dt.year == filter_dt.year and post_dt.month == filter_dt.month
            for filter_dt in filter_datetimes
        )
    ]

    filtered_timestamps = [int(dt.timestamp()) for dt in filtered_datetimes]

    filtered_posts = {
        k: v for k, v in posts.items() if v["time"] in filtered_timestamps
    }

    return filtered_posts


def get_post_comments(
    posts: Dict[str, Any], sleep_ms_range: Optional[List[int]] = None
) -> Dict[str, Any]:
    post_comments = {}
    error_post_ids = []
    total_sleep = 0.0
    for id, post in posts.items():
        # kid is an id already
        for kid in post.get("kids"):
            try:
                post_comments[kid] = get_post_by_id(kid)
            except Exception as e:
                error_post_ids.append(kid)
                logger.info(f"skipping {kid = } because", e)
                continue
            finally:
                if sleep_ms_range:
                    random_ms = randint(*sleep_ms_range) / 1000.0
                    sleep(random_ms)
                    total_sleep += random_ms

    logger.info(f"Slept a total of {total_sleep = }s to delay API calls.")

    return (post_comments, error_post_ids)


def calc_comments_collecting(posts) -> int:
    num_comments = 0
    for _, post in posts.items():
        # descendants counts nested, which aren't all grabbed
        num_comments += len(post.get("kids"))

    logger.info(
        f"Calling sequential GETs for {num_comments} comments,"
        "this will take some time..."
    )

    return num_comments
