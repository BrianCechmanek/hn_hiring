"""
This is a boilerplate pipeline 'data_collection'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import (
    calc_comments_collecting,
    filter_posts_by_dates,
    get_post_comments,
    get_submitted,
    get_user,
    get_users_karma,
    get_whos_hiring,
    ids_to_str,
)


def create_pipeline(**kwargs) -> Pipeline:
    ppl_instance = pipeline(
        [
            node(
                func=get_user,
                inputs="params:user_name",
                outputs="user_profile",
                name="get_user_submitted",
            ),
            node(
                func=get_submitted,
                inputs="user_profile",
                outputs="user_submitted_ids",
                name="get_submitted_ids",
            ),
            node(
                func=get_whos_hiring,
                inputs="user_submitted_ids",
                outputs=["is_hiring_ids", "not_hiring_ids", "is_hiring_posts"],
                name="get_whos_hiring",
            ),
            node(
                func=ids_to_str,
                inputs="is_hiring_ids",
                outputs="is_hiring_ids_str",
                name="save_hiring_post_ids",
            ),
            node(
                func=ids_to_str,
                inputs="not_hiring_ids",
                outputs="not_hiring_ids_str",
                name="save_not_hiring_post_ids",
            ),
            node(
                func=filter_posts_by_dates,
                inputs=["is_hiring_posts", "params:post_dates"],
                outputs="filtered_posts",
                name="filter_posts_by_dates",
            ),
            node(
                func=calc_comments_collecting,
                inputs="filtered_posts",
                outputs="num_comments",
                name="calc_comments_collecting",
            ),
            node(
                func=get_post_comments,
                inputs=["filtered_posts", "params:api_ms_sleep_range"],
                outputs=["post_comments", "error_post_ids"],
                name="get_hiring_post_comments",
            ),
            node(
                func=get_users_karma,
                inputs="post_comments",
                outputs="users_karma",
                name="get_users_karma",
            ),
        ]
    )
    return pipeline(
        pipe=ppl_instance,
        inputs=None,
        namespace="data_collection",
    )
