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


def get_files_between_dates(start_date, end_date):
    commits = repo.get_commits(since=start_date, until=end_date)

    filenames = []

    # Iterate through all open pull requests in the repository
    for commit in commits:
        print(f"Checking Commit #{commit.raw_data['sha']} - {commit.author.name} ({commit.author.login})")

        # Get the list of files changed in the pull request
        pull_requests = commit.get_pulls()

        for pull_request in pull_requests:
            files = pull_request.get_files()

            # Iterate through each file and print the added lines
            for file in files:
                if file.filename.startswith("content/") and not (file.filename.endswith(".rb") or file.filename.endswith(".html.haml")):
                    print(f"File: {file.filename}")
                    filenames.append(file.filename)

    return filenames

def remove_duplicate_filenames(filenames): # array
      # Convert the list to a set to remove duplicates
    unique_lines = set(filenames)
    
    # Convert the set back to a list to maintain the order
    return list(unique_lines)


if __name__ == '__main__':
    filenames = get_files_between_dates(datetime(2024, 3, 1), datetime(2024, 3, 31))
    filenames = remove_duplicate_filenames(filenames)
    print(len(filenames))
    with open("updated.txt", "w") as file:
        file.writelines("\n".join(filenames))
