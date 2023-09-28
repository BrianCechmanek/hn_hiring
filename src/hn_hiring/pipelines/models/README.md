# Pipeline models

> _Note:_ This is a `README.md` boilerplate generated using `Kedro 0.18.12`.

## Overview

All model training is called in this pipeline. If many, they can be split by it's modular setup.

For now, it outputs one plot: the `Companies' karma` plot.

## Pipeline inputs

- `data_processing.companies_karma`: to make a barh plot with the company name, user name, and user's karma as proxy for the company.

## Pipeline outputs

- `models.companies_karma_rank_plot`: a barh plot with the company name, user name, and user's karma as proxy for the company.
