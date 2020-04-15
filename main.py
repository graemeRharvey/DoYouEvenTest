import os
import sys
from github import Github
import argparse
from envdefault import EnvDefault
import checks
import logging
from config_parser import Config

def parse_arguments():
    """
    Parse them args
    """
    parser = argparse.ArgumentParser()
    # user_login_group = parser.add_mutually_exclusive_group(required=False)
    # user_login_group.add_argument('-u', '--username', help="GitHub username")
    # user_login_group.add_argument('-t', '--token', action=EnvDefault, envvar='GIT_API_TOKEN', 
    #     help="GitHub token: set using -t or setting env var 'GIT_API_TOKEN'")
    #parser.add_argument('-p', '--password', required=False, help="GitHub password")
    parser.add_argument('-t', '--token', action=EnvDefault, envvar='GIT_API_TOKEN', 
        help="GitHub token: set using -t or setting env var 'GIT_API_TOKEN'")
    parser.add_argument('-e', '--enterprise', action='store_true', help="Enable Github Enterprise")
    org_repo_group = parser.add_mutually_exclusive_group(required=True)
    org_repo_group.add_argument('-o', '--organization', help="Organization to scan all repos from")
    org_repo_group.add_argument('-r', '--repository', help="Single repo to scan PRs in")
    parser.add_argument('-b', '--branch', default='master', help="Base branch to use")
    parser.add_argument('-g', '--githost', action=EnvDefault, envvar='GIT_HOST', 
        help="GitHub enterprise host: set using -g or setting env var 'GIT_HOST'")
    parsed_args = parser.parse_args()
    # if parsed_args.username and not parsed_args.password:
    #     parser.error("If using a github username, you must also provide a password")
    #     sys.exit()
    if parsed_args.enterprise and not parsed_args.githost:
        parser.error("-e requires use of -g to set host, or env var 'GIT_HOST' to be set.")
        sys.exit()
    if parsed_args.repository and "/" not in parsed_args.repository:
        parser.error("repo name should also contain organization name like: organization/repo_name")
        sys.exit()
    return parsed_args


def main():
    args = parse_arguments()
    config = Config()
    if args.enterprise:
        # Enterprise
        base_url = f"https://{args.githost}/api/v3"
        g = Github(base_url=base_url, login_or_token=args.token) # UPDATE
    else:
        # Github
        g = Github(args.token)

    # Get organization (For github enterprise)
    #org = g.get_organization(args.organization)
    #repos = org.get_repos()

    repo = None
    if args.repository:
        repo = g.get_repo(args.repository)
    else:
        org = g.get_organization(args.organization)
        repos = org.get_repos()

    # Reduce list of repos? Any criteria?

    is_valid = 0
    did_test = 0
    # Grab PRs based on criteria (how far back to go?)
    pulls = repo.get_pulls(state='closed', sort='created', direction='desc', base=args.branch)
    relevant_pulls = pulls[:config.constants["LOOKBACK"]]

    for pr in relevant_pulls:
        files_list = pr.get_files()

        # Read files list
        print(pr.title)
        if checks.pr_valid(files_list, config.ignore_list):
            print(str(pr.number) + " is valid.")
            is_valid+=1
            if checks.look_for_tests(files_list, config.test_pattern_list):
                did_test+=1
        else:
            print(str(pr.number) + " is NOT valid.")
    print("Of " + str(is_valid) + " PRs, " + str(did_test) + " were tested!")
    percent = did_test / is_valid * 100
    print("That's " + str(percent) + " percent tested!")

if __name__ == '__main__':
    main()