"""
This is a boilerplate pipeline 'models'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import plot_companies_karma, plot_processed_text_posts


def create_pipeline(**kwargs) -> Pipeline:
    ppl_instance = pipeline(
        [
            node(
                func=plot_companies_karma,
                inputs="data_processing.companies_karma",
                outputs="companies_karma_rank_plot",
                name="plot_companies_karma",
            ),
            node(
                func=plot_processed_text_posts,
                inputs="data_processing.processed_text_posts",
                outputs="processed_text_posts_plot",
                name="plot_processed_text_posts",
            ),
        ]
    )
    return pipeline(
        pipe=ppl_instance,
        inputs=[
            "data_processing.companies_karma",
            "data_processing.processed_text_posts",
        ],
        namespace="models",
    )
