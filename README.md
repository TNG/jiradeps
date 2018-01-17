### About
Jiradeps is a Python tool to render the dependency graph of Jira stories (i.e., the "is blocked by" relations). It can 
also be used to track the progress during development.

### How to install

After the checkout, go to the jiradeps directory (Python >= 3.6 is required):

    pip install .

Then you can run jiradeps:

    jiradeps --help

If you installed it in a virtualenv (which is recommended), then you always have to activate the virtualenv first.

After installation you must create a config file. Jiradeps will offer to create a template config file for you if none 
is found (which then has to be adapted by you). The config file is read from the current working directory, unless 
specified otherwise.

### Usage
- Recommended flags for story checking during analysis: `-go` (group by epic, open file)
- Recommended flags for development: `-goas` (..., align by sprint, show status)

Explanation of the numbers in parentheses for story nodes, like `(2)` or `(2/3)`:
- The second or single number is the longest chain of blocking ancestors (including the story itself), so theoretically 
the sprint in which it can be started.
- The first number is the first sprint for which the story is marked (only shown if available).

For the example `(2/3)` this means that the story was scheduled for the second sprint, but it has a chain of two 
blocking dependencies before it.

### Copyright & License

Jiradeps was conceived, written and executed by [Niko Wilbert](https://github.com/nwilbert), 
[Achim Herwig](https://github.com/achimh3011) and [Ingo Bürk](https://github.com/airblader).

&copy; 2018 TNG Technology Consulting GmbH, Unterföhring, Germany

Licensed under the Apache License, Version 2.0 - see [LICENSE.md](LICENSE.md) in project root directory.
