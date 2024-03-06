"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import get_companies_post_karma, process_text


def create_pipeline(**kwargs) -> Pipeline:
    ppl_instance = pipeline(
        [
            node(
                func=process_text,
                inputs=[
                    "data_collection.post_comments",
                    "params:funcs",
                    "params:text_params",
                ],
                outputs="processed_text_posts",  # "processed_comments_text",
                name="process_post_text",
            ),
            node(
                func=get_companies_post_karma,
                inputs=["data_collection.post_comments", "data_collection.users_karma"],
                outputs="companies_karma",
                name="get_companies_post_karma",
            ),
        ]
    )
    return pipeline(
        pipe=ppl_instance,
        inputs=["data_collection.post_comments", "data_collection.users_karma"],
        namespace="data_processing",
    )
