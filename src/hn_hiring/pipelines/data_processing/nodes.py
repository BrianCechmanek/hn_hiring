"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.12
"""

import logging
import re
from typing import Any, Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)


def process_text(
    posts: Dict[str, Any],
    funcs: Optional[List[str]],
    text_params: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Process post text by a variable list of functions.

    Args:
        posts: Dict: hn posts, in full API json
        funcs: str: list of functions to apply, ordered
        text_params: str: dict of params that can be fed into funcs, keyed by func name
    Returns:
        post-processed posts, where the text fields have been modified.
    """

    drop_keys = []
    for key, post in posts.items():
        post_text = post.get("text", "")
        for func in funcs:
            # Assuming the functions are available in the global scope
            func_params = text_params.get(func, {})
            post_text = globals()[func](post_text, func_params)
            if post_text is None:
                drop_keys.append(key)

    # Filter out posts with None in the text field
    list(map(posts.pop, drop_keys))

    return posts


def filter_jobs(text: str, filters: List[str]) -> Union[str, None]:
    """filter a post's text for a list of jobs.

    Not case sensitive. no fuzzy matching.
    """

    if any([job.lower() in text.lower().split() for job in filters]):
        return text
    else:
        return None


def _get_company_from_comment(text: str) -> str:
    """Attempt to get a company name from a comment post.

    naiive way: first word in the post, usually correct.
    TODO: implement NER
    """

    if text:
        splits = r"\||,|\("
        split_s = re.split(splits, text)
        return split_s[0].lstrip().rstrip()
    else:
        return "No Company Found"


def get_companies_post_karma(
    posts: Dict[str, Any], users_karma: Dict[str, int]
) -> Dict[int, Tuple[str, str, int]]:
    """Get company names from post text, assign to post id/user,
    and append poster's karma

    returns:
        companies_karma: {id: (company, user, karma)}"""
    companies_karma = {}

    for id, post in posts.items():
        karma = users_karma.get(id)
        user = post.get("by")
        company = _get_company_from_comment(post.get("text"))

        companies_karma[id] = (company, user, karma)

    return companies_karma
