# Do You Even Test?
A python program to gather evidence on how often tests are committed with major changes.

## Usage

### Setup

1. Install required packages: `pip install -r requirements.txt`
2. Modify `config.yml` to your liking.
* `LOOKBACK` represents how many PRs backwards you'd like to analyze.
* `WORKSHEET` allows you to define a name (or path) of the output file.
* `TEST_PATTERNS` is the list of identifiers used to determine if a file is a test.
_Note that currently, this is using a simple 'contains' approach, so glob/regexs are not yet supported._
* `IGNORE_LIST` is the set of files that would contain irrelevant files (no need to test).
If a PR doesn't contain any files not found in the ignore list, the PR is assumed trivial and not analyzed.

### Run

To run against a GitHub instance:

`python main.py -t my_git_api_token -o my_organization`


To run against a GitHub Enterprise instance:

`GIT_API_TOKEN=my_git_api_token python main.py -o my_organization -e -g "git.myorg.com"`


The tool can be run against a single repo (using `-r organization_name/repo_name`) 
or all repos in an organization (using `-o organization_name`).

To run against a Github Enterprise instance, include the `-e` flag.
_Note: for enterprise, you must also include the host address either using `-h myinstance.git.com` or by setting 
the environment variable `GIT_HOST=myinstance.git.com`._

By default, the tool analyzes PRs targeted at `master`. 
This can be changed by setting `-b target_branch`.

