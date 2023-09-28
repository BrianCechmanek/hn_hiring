# Pipeline data_processing

> _Note:_ This is a `README.md` boilerplate generated using `Kedro 0.18.12`.

## Overview

The data processing pipeline is to set up the raw data in a manner that readies it for arbitrary modelling purposes. New processing can be added as more models are added.

At this time, the text processing is a pass-through function.

## Pipeline inputs

`data_collection.post_comments`, `data_collection.users_karma` are used to construct a simple karma-by-company ranking.

## Pipeline outputs

- `data_processing.companies_karma`: gives a proxy estimate of company "clout". it will be used in modelling (a simple rank plot, at first)
