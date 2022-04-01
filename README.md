[![CircleCI](https://circleci.com/gh/TNG/jiradeps.svg?style=svg)](https://circleci.com/gh/TNG/jiradeps)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FTNG%2Fjiradeps.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FTNG%2Fjiradeps?ref=badge_shield)

# Jiradeps

Graphically assess the dependencies of your Jira stories

### About
Jiradeps is a Python tool to render the dependency graph of Jira stories (i.e., the "is blocked by" relations). It can
also be used to track the progress during development.

Internally, jiradeps works in three stages to render a dependency graph:
1. First the selected Epics are loaded from [Jira](https://www.atlassian.com/software/jira), based on the provided parameters. Then the stories contained in these Epics are loaded.
2. The story dependencies are translated into a graph representation (using the networkx library). Graph properties like the longest dependency chain are calculated from this graph.
3. A graphical representation of the dependency graph is rendered into a file (e.g., an SVG or PNG) via the [graphviz](https://www.graphviz.org/) library.

### How to install

First, you have to ensure that [graphviz](https://www.graphviz.org/) is installed (e.g., via a manual installation, or via a package manager / brew on macOS / Chocolatey on Windows).

Then download or clone this project. Afterwards go to the resulting jiradeps directory (Python >= 3.9 is required):

If you want to install in a virtualenv (which is recommended), then you always have to [create and activate the virtualenv](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/) first. A convenient alternative to this approach is [pipx](https://pypa.github.io/pipx/) - especially if you don't want to develop on `jiradeps`:

    pip install git+https://github.com/TNG/jiradeps.git

Then you can run jiradeps:

    jiradeps --help

### Configuration

After installation you must create a config file. Jiradeps will offer to create a template config file for you if none
is found (which then has to be adapted by you). The config file is read from the current working directory, unless
specified otherwise. Besides authentication, options specifiying the dependency relation used in Jira (default: _Blocker_)
and the custom field id denoting the _Sprint_ field sometimes need to be set differently.

### Usage
- Recommended flags for backlog analysis: `-go` (group by epic, open file)
- Recommended flags during development of the stories: `-goas` (..., align by sprint, show status)

#### Explanation of the numbers in parentheses for story nodes
You will notice that story nodes contain cryptic numbers like `(2)` or `(2/3)` next to the story title:
- The second or single number is the longest chain of blocking ancestors (including the story itself), so theoretically
the sprint in which it can be started.
- The first number is the first sprint for which the story is marked (only shown if available).

For the example `(2/3)` this means that the story was scheduled for the second sprint, but it has a chain of two
blocking dependencies before it.

### Development

If you plan to tinker with jiradeps, you should set yourself up for development:

1. create virtualenv (see above)
2. install `pip-tools` and `pre-commit`
3. clone repository
4. install commit hooks: `pre-commit install`
5. define package current versions: `pip-compile setup.py`
6. install development packages: `pip install -r requirements-dev.txt`
7. install `jiradeps` for development `pip install -e .`

If you plan to contribute to the project, please check [CONTRIBUTING.md](CONTRIBUTING.md)

### Copyright & License

Jiradeps was conceived, written and executed by [Niko Wilbert](https://github.com/nwilbert),
[Achim Herwig](https://github.com/achimh3011) and [Ingo Bürk](https://github.com/airblader).

&copy; 2018,2022 TNG Technology Consulting GmbH, Unterföhring, Germany

Licensed under the Apache License, Version 2.0 - see [LICENSE.md](LICENSE.md) in project root directory.


[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FTNG%2Fjiradeps.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FTNG%2Fjiradeps?ref=badge_large)
