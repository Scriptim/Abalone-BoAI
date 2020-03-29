<!--
Copyright 2020 Scriptim (https://github.com/Scriptim)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-->

# Contribution Guidelines

If you want to contribute to this repository, please first discuss your desired changes in an issue (especially before opening a pull request).

**Please follow the [code of conduct](./CODE_OF_CONDUCT.md) in all interactions with this repository.**

## How can I Contribute?

### Report a Bug

- Bugs are reported as [GitHub Issues](https://github.com/Scriptim/Abalone-BoAI/issues).
- Please make sure that there is no issue for the bug already, to avoid duplicates.
- Provide a concise title and an precise and clear description of the bug.
- Describe the exact steps to reproduce the bug and include any relevant information such as version numbers.

### Suggest Enhancements

- Enhancements suggestion are tracked as [GitHub Issues](https://github.com/Scriptim/Abalone-BoAI/issues).
- If there is already an issue regarding the desired or a similar enhancement, please discuss the details there to avoid duplicates.
- Provide a concise title and an precise and clear description of the enhancement.

### Open a Pull Requests

- Added or modified code is properly formatted ([PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)), documented (docstrings according to the [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)) and tested.
- The issue resolved by a PR is clearly referenced, preferably by using a [keyword](https://help.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword).
- All code, comments, documentation, PR descriptions etc. are written exclusively in English.
- All dependencies are listed in [`Pipfile`](./Pipfile) and [`Pipfile.lock`](./Pipfile.lock).
- Commit messages use the imperative mood, have a meaningful, capitalized subject line with maximum 50 characters and do not end with a period. 

## Testing

This project uses the [`unittest`](https://docs.python.org/3/library/unittest.html) module for testing. The command for testing is specified in [`.coveragerc`](./.coveragerc). You can run it from the project root using:

    $ coverage run
    
Use `$ coverage report` for a report on testing coverage.

## Documentation

API documentation is available at <https://scriptim.github.io/Abalone-BoAI>.
