# Front-end visualizer in streamlit


import pandas as pd
from pathlib import Path
import streamlit as st

from kedro.config import OmegaConfigLoader

from kedro.framework.context import KedroContext, KedroContextError
from kedro.framework.hooks import _create_hook_manager

# Load Kedro configuration
config_loader = OmegaConfigLoader(conf_source="conf/base")
conf_catalog = config_loader.get("catalog*", "catalog*/**")

# Create KedroContext
class MyAppContext(KedroContext):
    project_name = "hn_hiring"

# Load KedroContext
try:
    context = MyAppContext(
        package_name=__name__,
        project_path="./",
        hook_manager=_create_hook_manager(),
        config_loader=config_loader,
        env='base',
    )
except KedroContextError as exc:
    st.error(f"Unable to create KedroContext: {exc}")

# Load the dataset
catalog = context.catalog
print(catalog.list())
hiring_df = catalog.load("data_processing.processed_text_posts")
print(f"{hiring_df.shape = }")
print("-----END-----")