# Pipeline data_collection

> _Note:_ This is a `README.md` boilerplate generated using `Kedro 0.18.12`.

## Overview

This pipeline makes sequential requests from the HN public API. It collects `Who is hiring (*)` post top-level comments only. At this time, only one or some months are collected, to reduce API pummeling.

This pipeline is relatively robust on usage, it assumes the `user` of interest is `whoishiring`, but this can be changed. Ditto, it assumes to look for posts with `who is hiring` (case–insensitive) in the title, this could be modified if desired (perhaps Freelancer posts are interesting?).

## Pipeline inputs

No data are input into this pipeline. Only configuration:

(as of submission, 18 Aug 2023)

```yaml
data_collection:
  user_name: "whoishiring"
  post_dates: ["August 2023"]
  api_ms_sleep_range: [200, 500]
```

The `post_dates` is a filter to apply that truncates the search space to a given month-year. Optional values are `<month> <year>` `<month>`, `<year>` (albeit, untested on the latter 2).

The `api_ms_sleep_range` is optional, it enforces a small, semi-random sleep to the program, to reduce API call-rate. If not supplied, there is none.

## Pipeline outputs

See the [catalog](../../../../conf/base/catalog.yml) for all entries. They are namespaced as `data_collection.*`.

The key output is `data_collection.post_comments`, found in `data/02_intermediate/post_comments.json` - it stores all comment post API returns as a Dictionary:

```json
{
  "36963693": {
    "by": "dokein",
    "id": 36963693,
    "kids": [36984740, 36965061, 37055762],
    "parent": 36956867,
    "text": "SmarterDx | 180 - 230K + equity + benefits | ...",
    "time": 1690926903,
    "type": "comment"
  }
}
```

This dataset will be processed for modelling.
