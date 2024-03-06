"""
This is a boilerplate test file for pipeline 'data_collection'
generated using Kedro 0.18.12.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""

from datetime import datetime

import pytest
from hn_hiring.pipelines.data_collection.nodes import (
    calc_comments_collecting,
    filter_posts_by_dates,
    get_post_by_id,
    get_post_comments,
    get_submitted,
    get_user,
    get_user_submitted,
    get_whos_hiring,
    is_whos_hiring,
)


# from https://github.com/HackerNews/API#users
@pytest.fixture
def hn_user_expected():
    return {
        "about": "This is a test",
        "created": 1173923446,
        "delay": 0,
        "id": "jl",
        "karma": 2937,
        "submitted": [
            8265435,
            8168423,
            8090946,
            8090326,
            7699907,
            7637962,
            7596179,
            7596163,
            7594569,
            7562135,
            7562111,
            7494708,
            7494171,
            7488093,
            7444860,
            7327817,
            7280290,
            7278694,
            7097557,
            7097546,
            7097254,
            7052857,
            7039484,
            6987273,
            6649999,
            6649706,
            6629560,
            6609127,
            6327951,
            6225810,
            6111999,
            5580079,
            5112008,
            4907948,
            4901821,
            4700469,
            4678919,
            3779193,
            3711380,
            3701405,
            3627981,
            3473004,
            3473000,
            3457006,
            3422158,
            3136701,
            2943046,
            2794646,
            2482737,
            2425640,
            2411925,
            2408077,
            2407992,
            2407940,
            2278689,
            2220295,
            2144918,
            2144852,
            1875323,
            1875295,
            1857397,
            1839737,
            1809010,
            1788048,
            1780681,
            1721745,
            1676227,
            1654023,
            1651449,
            1641019,
            1631985,
            1618759,
            1522978,
            1499641,
            1441290,
            1440993,
            1436440,
            1430510,
            1430208,
            1385525,
            1384917,
            1370453,
            1346118,
            1309968,
            1305415,
            1305037,
            1276771,
            1270981,
            1233287,
            1211456,
            1210688,
            1210682,
            1194189,
            1193914,
            1191653,
            1190766,
            1190319,
            1189925,
            1188455,
            1188177,
            1185884,
            1165649,
            1164314,
            1160048,
            1159156,
            1158865,
            1150900,
            1115326,
            933897,
            924482,
            923918,
            922804,
            922280,
            922168,
            920332,
            919803,
            917871,
            912867,
            910426,
            902506,
            891171,
            807902,
            806254,
            796618,
            786286,
            764412,
            764325,
            642566,
            642564,
            587821,
            575744,
            547504,
            532055,
            521067,
            492164,
            491979,
            383935,
            383933,
            383930,
            383927,
            375462,
            263479,
            258389,
            250751,
            245140,
            243472,
            237445,
            229393,
            226797,
            225536,
            225483,
            225426,
            221084,
            213940,
            213342,
            211238,
            210099,
            210007,
            209913,
            209908,
            209904,
            209903,
            170904,
            165850,
            161566,
            158388,
            158305,
            158294,
            156235,
            151097,
            148566,
            146948,
            136968,
            134656,
            133455,
            129765,
            126740,
            122101,
            122100,
            120867,
            120492,
            115999,
            114492,
            114304,
            111730,
            110980,
            110451,
            108420,
            107165,
            105150,
            104735,
            103188,
            103187,
            99902,
            99282,
            99122,
            98972,
            98417,
            98416,
            98231,
            96007,
            96005,
            95623,
            95487,
            95475,
            95471,
            95467,
            95326,
            95322,
            94952,
            94681,
            94679,
            94678,
            94420,
            94419,
            94393,
            94149,
            94008,
            93490,
            93489,
            92944,
            92247,
            91713,
            90162,
            90091,
            89844,
            89678,
            89498,
            86953,
            86109,
            85244,
            85195,
            85194,
            85193,
            85192,
            84955,
            84629,
            83902,
            82918,
            76393,
            68677,
            61565,
            60542,
            47745,
            47744,
            41098,
            39153,
            38678,
            37741,
            33469,
            12897,
            6746,
            5252,
            4752,
            4586,
            4289,
        ],
    }


@pytest.fixture
def hn_post_expected():
    return {
        "by": "dhouston",
        "descendants": 71,
        "id": 8863,
        "kids": [
            8952,
            9224,
            8917,
            8884,
            8887,
            8943,
            8869,
            8958,
            9005,
            9671,
            8940,
            9067,
            8908,
            9055,
            8865,
            8881,
            8872,
            8873,
            8955,
            10403,
            8903,
            8928,
            9125,
            8998,
            8901,
            8902,
            8907,
            8894,
            8878,
            8870,
            8980,
            8934,
            8876,
        ],
        "score": 111,
        "time": 1175714200,
        "title": "My YC app: Dropbox - Throw away your USB drive",
        "type": "story",
        "url": "http://www.getdropbox.com/u/2/screencast.html",
    }


@pytest.fixture
def hn_comment_expected():
    return {
        "by": "norvig",
        "id": 2921983,
        "kids": [2922097, 2922429, 2924562, 2922709, 2922573, 2922140, 2922141],
        "parent": 2921506,
        "text": "Aw shucks, guys ... you make me blush with your \
            compliments.<p>Tell you what, Ill make a deal: I'll \
                keep writing if you keep reading. K?",
        "time": 1314211127,
        "type": "comment",
    }


@pytest.fixture
def hn_comment_parent():
    return {
        "by": "mayoff",
        "descendants": 31,
        "id": 2921506,
        "kids": [
            2921983,
            2921798,
            2922112,
            2921758,
            2921764,
            2922038,
            2923109,
            2922107,
            2921923,
            2922398,
            2921875,
        ],
        "score": 226,
        "time": 1314205301,
        "title": "Peter Norvig on a 45-year-old article about a \
            checkers-playing program",
        "type": "story",
        "url": "Cut for test",
    }


# from scraped wih posts
@pytest.fixture
def hn_wih_actual_posts():
    return {
        "36956867": {
            "by": "whoishiring",
            "descendants": 532,
            "id": 36956867,
            "kids": [36963693],
            "score": 479,
            "text": "Cut for test",
            "time": 1690902128,
            "title": "Ask HN: Who is hiring? (August 2023)",
            "type": "story",
        },
        "36573871": {
            "by": "whoishiring",
            "descendants": 451,
            "id": 36573871,
            "kids": [36577649],
            "score": 421,
            "text": "Cut for test",
            "time": 1688396452,
            "title": "Ask HN: Who is hiring? (July 2023)",
            "type": "story",
        },
        "7507765": {
            "by": "whoishiring",
            "descendants": 528,
            "id": 7507765,
            "kids": [7508982],
            "score": 337,
            "text": "Cut for test",
            "time": 1396357727,
            "title": "Ask HN: Who is hiring? (April 2014)",
            "type": "story",
        },
    }


def test_get_user(hn_user_expected):
    res = get_user(user="jl")

    assert res.get("id") == hn_user_expected.get("id")
    assert res.get("about") == hn_user_expected.get("about")
    assert all([x in res.get("submitted") for x in hn_user_expected.get("submitted")])

    # or on fail -- TODO hard to trigger fail status
    # with pytest.raises(Exception) as e_info:
    #     res = get_user(user="super_not_an_account")


def test_get_user_submitted(hn_user_expected):
    submitted = get_user_submitted(user="jl")

    assert all([x in submitted for x in hn_user_expected.get("submitted")])


def test_get_submitted(hn_user_expected):
    submitted = get_submitted(post=hn_user_expected)

    assert all([x in submitted for x in hn_user_expected.get("submitted")])


def test_get_post_by_id(hn_post_expected):
    """8863 is archived, so don't worry about new replies on it."""
    post = get_post_by_id(id=8863)
    assert post.get("id") == hn_post_expected.get("id")
    assert post.get("about") == hn_post_expected.get("about")
    assert set(post.get("kids")) == set(hn_post_expected.get("kids"))


@pytest.mark.parametrize(
    "hiring, not_hiring",
    [
        pytest.param(36956867, 36956866),
        pytest.param(36573871, 36956865),
        pytest.param(36152014, 36573870),
        pytest.param(36152014, 26661441),
    ],
)
def test_is_whos_hiring(hiring, not_hiring):
    hiring_post = get_post_by_id(hiring)
    not_hiring_post = get_post_by_id(not_hiring)

    assert is_whos_hiring(post=hiring_post)
    assert not is_whos_hiring(post=not_hiring_post)


# BC: this test runs correctly, both pytest and kedro test
# but the kedro harness cannot execute an async call.
# uncomment this when that is swapped to async
# @pytest.mark.xfail(reason="coroutine object has no attribute 'get'")
# @pytest.mark.asyncio
@pytest.mark.parametrize(
    "hiring, not_hiring, expected",
    [
        pytest.param([36956867], [36956866], ([36956867], [36956866], {"dummy": None})),
        pytest.param([36573871], [36956865], ([36573871], [36956865], {"dummy": None})),
        pytest.param([36152014], [36573870], ([36152014], [36573870], {"dummy": None})),
    ],
)
def test_get_whos_hiring(hiring, not_hiring, expected):
    is_hiring_ids, not_hiring_ids, _ = get_whos_hiring(hiring + not_hiring)
    assert is_hiring_ids == expected[0]
    assert not_hiring_ids == expected[1]


@pytest.mark.parametrize(
    "filter_dates, expected",
    [(("July 2023", "January 2021"), [datetime(2023, 7, 3, 16, 0, 52)])],
)
def test_filter_posts_by_dates(
    hn_wih_actual_posts,
    filter_dates,
    expected,
):
    # uses previous three actuals to check filtering 2 out

    filtered_posts = filter_posts_by_dates(hn_wih_actual_posts, filter_dates)

    assert len(filtered_posts) == 1
    assert list(filtered_posts.keys())[0] == "36573871"
    assert [v["time"] for _, v in filtered_posts.items()] == [
        int(dt.timestamp()) for dt in expected
    ]


def test_get_post_comments(hn_comment_parent):
    comments, _ = get_post_comments(
        posts={str(hn_comment_parent["id"]): hn_comment_parent}
    )

    expected_comment_ids = hn_comment_parent.get("kids")

    # not all comments have to be returned, but at least one
    assert len(comments) >= 1
    assert all([kid in expected_comment_ids for kid in comments.keys()])


def test_calc_comments_collecting(hn_wih_actual_posts):
    num_comments = calc_comments_collecting(hn_wih_actual_posts)
    assert num_comments == 3  # noqa : PLR2004


@pytest.mark.skip(reason="requires a dead profile")
def test_get_users_karma(): ...
