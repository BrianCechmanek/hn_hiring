# hn_hiring

## Executive Summary

A Data Engineering-heavy collection and processing pipeline gather's HN Who Is Hiring posts, with minimal analysis.

Posts are gathered, by one or more months, and semi-filtered for provided keywords, such as `data scientist`, `machine learning engineer`. No fuzzy matching is done.

# Setup & Running

This repo runs on [kedro](www.kedro.org). Requirements are standard python (`~=3.10`) and an appropriate environment.

0. Clone the repo: `$ git clone https://github.com/BrianCechmanek/hn_hiring.git`
1. In terminal of choice change to project dir: `$ cd hn_hiring`
2. (optional, recommended) create a python 3.10.5 venv [via pyenv](https://github.com/pyenv/pyenv): `$ pyenv virtualenv 3.10.5 hn`
3. (optional, recommended) activate venv: `$ pyenv activate hn`
4. install kedro & requirements: `$ python -m pip install -r src/requirements.txt`
5. run pipelines: `$ kedro run`
6. (optional, highly recommended) visualise the ppl: `$ kedro viz` (opens browser window. refresh after a moment if you get an error page)

Outputs will be in `data/*`

# Pipelines

The code is strictly split into discrite pipelines. Each can be run separately, though an initial sequential run is required (to collect and process the data).

The Kedro data convention is similar to that of cookie-cutter data science's, where raw, primary, ... , reports, are explicitly separated from each other. I follow this.

The full pipeline is concatenated such that `kedro run` runs all three sequentially.

## data_collection

Data are collected via the public HN API.

- To run: `kedro run --pipeline=data_collection`
- I suggest only running this pipeline once or twice. it takes a minute, but mostly I don't think it's nice to pummel the HN API (though, really, only a couple hundred calls are performed)
- See pipeline specifics in it's [README](./src/hn/pipelines/data_collection/README.md)

## data_processing

- To run: `kedro run --pipeline=data_processing`
- See pipeline specifics in it's [README](./src/hn/pipelines/data_processing/README.md)

## models

- See pipeline specifics in it's [README](./src/hn/pipelines/models/README.md)
- To run: `kedro run --pipeline=models`

At this time, I'm not training, running, or evaluating any models. I May add something in the future.

## Notebooks

I do not use notebooks at this time.

# HN Who is Hiring Post Assumptions

- I don't think the "freelancer" or "wants to be hired" posts have any relevance

# Additional Info

- [pre-commit](https://pre-commit.com/) is used for formatting and linting. Feel free to install it, if you're going to do anything to the code. I just like using it
- If you wish to run tests, you can use the (deprecated) `kedro test`, which handles package importing. Else you will have to install the package: `python -m pip install -e .` followed by `pytest .` (or whichever selection you desire)
- I wanted to do some async stuff with the API collection, but kedro doesn't handle it natively, and writing an AsyncRunner was WAY out of scope
- Children of posts are ignored: in general Who's Hiring posts shouldn't get replies; their value would be unclear; I wan't to avoid a recursion task at the moment
- Sometimes a poster will reply to themselves with additonal job info. Looking at you Lloyd's. Thus, I'm not worried at this time about losing descendants.

---

(the below is the stock Kedro README. I've kept it for reference)

## Overview

This is your new Kedro project, which was generated using `kedro 0.18.12`.

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

## Rules and guidelines

In order to get the best out of the template:

- Don't remove any lines from the `.gitignore` file we provide
- Make sure your results can be reproduced by following a data engineering convention
- Don't commit data to your repository
- Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies

Declare any dependencies in `src/requirements.txt` for `pip` installation and `src/environment.yml` for `conda` installation.

To install them, run:

```
pip install -r src/requirements.txt
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the file `src/tests/test_run.py` for instructions on how to write your tests. You can run your tests as follows:

```
kedro test
```

To configure the coverage threshold, go to the `.coveragerc` file.

## Project dependencies

To generate or update the dependency requirements for your project:

```
kedro build-reqs
```

This will `pip-compile` the contents of `src/requirements.txt` into a new file `src/requirements.lock`. You can see the output of the resolution by opening `src/requirements.lock`.

After this, if you'd like to update your project requirements, please update `src/requirements.txt` and re-run `kedro build-reqs`.

[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `context`, `catalog`, and `startup_error`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r src/requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter

To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab

To use JupyterLab, you need to install it:

```
pip install jupyterlab
```

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython

And if you want to run an IPython session:

```
kedro ipython
```

### How to convert notebook cells to nodes in a Kedro project

You can move notebook code over into a Kedro project structure using a mixture of [cell tagging](https://jupyter-notebook.readthedocs.io/en/stable/changelog.html#release-5-0-0) and Kedro CLI commands.

By adding the `node` tag to a cell and running the command below, the cell's source code will be copied over to a Python file within `src/<package_name>/nodes/`:

```
kedro jupyter convert <filepath_to_my_notebook>
```

> _Note:_ The name of the Python file matches the name of the original notebook.

Alternatively, you may want to transform all your notebooks in one go. Run the following command to convert all notebook files found in the project root directory and under any of its sub-folders:

```
kedro jupyter convert --all
```

### How to ignore notebook output cells in `git`

To automatically strip out all output cell contents before committing to `git`, you can run `kedro activate-nbstripout`. This will add a hook in `.git/config` which will run `nbstripout` before anything is committed to `git`.

> _Note:_ Your output cells will be retained locally.

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://docs.kedro.org/en/stable/tutorial/package_a_project.html)
