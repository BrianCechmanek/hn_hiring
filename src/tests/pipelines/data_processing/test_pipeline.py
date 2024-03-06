"""
This is a boilerplate test file for pipeline 'data_processing'
generated using Kedro 0.18.12.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""

import pytest
from hn_hiring.pipelines.data_processing.nodes import (
    _get_company_from_comment,
    get_companies_post_karma,
)


# actual data. consider swapping
@pytest.fixture
def hn_comment_expected():
    return {
        "36963693": {
            "by": "dokein",
            "id": 36963693,
            "kids": [36984740, 36965061, 37055762],
            "parent": 36956867,
            "text": "SmarterDx | 180 - 230K + equity + benefits | ",
            "time": 1690926903,
            "type": "comment",
        }
    }


@pytest.mark.skip(reason="process_text not yet implemented")
def test_process_text(): ...


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "SerpApi | https://serpapi.com | Senior Ruby Engineer | C",
            "SerpApi",
        ),
        (
            "Defense MicroElectronics Activity (DMEA) | $110 - $140k (GS-13)",
            "Defense MicroElectronics Activity",
        ),
        ("HamiltonPractice, REMOTE, INTERNS, ~1000$ pm, 3 months", "HamiltonPractice"),
    ],
)
def test__get_company_from_comment(text, expected):
    company = _get_company_from_comment(text)
    assert company == expected


@pytest.mark.parametrize(
    "users_karma",
    [({"36963693": 759})],
)
def test_get_companies_post_karma(hn_comment_expected, users_karma):
    companies_karma = get_companies_post_karma(hn_comment_expected, users_karma)
    assert list(companies_karma.keys())[0] == "36963693"
    assert companies_karma["36963693"][0] == "SmarterDx"
    assert companies_karma["36963693"][1] == "dokein"
    assert companies_karma["36963693"][2] >= 750  # noqa : PLR2004
