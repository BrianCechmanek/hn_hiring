"""
This is a boilerplate pipeline 'models'
generated using Kedro 0.18.12
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import plot_companies_karma


def create_pipeline(**kwargs) -> Pipeline:
    ppl_instance = pipeline(
        [
            node(
                func=plot_companies_karma,
                inputs="data_processing.companies_karma",
                outputs="companies_karma_rank_plot",
                name="plot_companies_karma",
            ),
        ]
    )
    return pipeline(
        pipe=ppl_instance,
        inputs="data_processing.companies_karma",
        namespace="models",
    )
