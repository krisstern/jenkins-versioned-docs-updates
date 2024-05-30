from datetime import datetime

from github import Github
from dotenv import dotenv_values

config = dotenv_values(".env")

# Replace 'your_access_token' with your GitHub personal access token
g = Github(config["GITHUB_TOKEN"])

# Replace 'repo_owner' and 'repo_name' with the owner and name of the repository
repo_owner = 'jenkins-infra'
repo_name = 'jenkins.io'
repo = g.get_repo(f"{repo_owner}/{repo_name}")


def get_pull_requests_between_dates(start_date, end_date):
    commits = repo.get_commits(since=start_date, until=end_date)

    requested_pull_requests = []

    # Iterate through all open pull requests in the repository
    for commit in commits:
        print(f"Checking Commit #{commit.raw_data['sha']} - {commit.author.name} ({commit.author.login})")

        # Get the list of files changed in the pull request
        pull_requests = commit.get_pulls()
        requested_pull_requests.extend(pull_requests)

        for pull_request in pull_requests:
            # Get the list of files changed in the pull request
            files = pull_request.get_files()

            # Iterate through each file and print the added lines
            for file in files:
                print(f"File: {file.filename}")

                # Fetch the content of the patch for the file
                patch_content = file.patch

                # Split the patch content into lines
                patch_lines = patch_content.split('\n')

                # Print patch lines
                for patch_line in patch_lines:
                    print(patch_line)

                print("\n" + "=" * 50 + "\n")  # Separating each file's output

            print("\n" + "=" * 50 + "\n")  # Separating each pull request's output

    return requested_pull_requests


if __name__ == '__main__':
    requested_pull_requests = get_pull_requests_between_dates(datetime(2024, 3, 1), datetime(2024, 3, 31))
    print(len(requested_pull_requests))
