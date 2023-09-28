"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.12
"""

import logging
import re
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)


def process_text(params: Dict):
    ...


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
