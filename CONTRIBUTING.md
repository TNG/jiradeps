# Contributing

Contributions are very welcome. The following will provide some helpful guidelines.

## Conditions

* Whatever content you contribute, you will provide it under the project license(s) (see [LICENSE.md](LICENSE.md))
* You accompany your submission with a signature of the Developer's Certificate of Origin (see [DCO.md](DCO.md)).
* You will submit your contribution together with your full name and e-mail address (see below).

## How to contribute

If you want to submit a contribution, please follow the following workflow:

* Fork the project
* Make sure you did ``pre-commit --install`` already. Doing it twice won't hurt.
* Create a feature branch
* Add your contribution
* Create a Pull Request

### Commits

Commit messages should be clear and fully elaborate the context and the reason of a change. Please stick to the
[customary format](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).

If your commit refers to an issue, please post-fix it with the issue number, e.g.

```
Issue: #123
```

Please sign-off each commit as described in [DCO.md](DCO.md), e.g. by committing using

````
git commit -s ...
````

### Pull Requests

If your Pull Request resolves an issue, please add a respective line to the end, like

```
Resolves #123
```

### Code Style & Formatting

Please adjust your code formatter to the general style of the project as defined in the .pre-commit.yaml file. That boils down to
 * use Python 3.9 constructs where possible
 * use black formatting
 * sort your imports
 * use proper typing

The good thing is that `pre-commit` will do everything for should you forget.
