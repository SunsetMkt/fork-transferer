import json

import httpx
from github import Github

TOKEN = "TOKEN"  # Personal access token
DESTINATION = "SunsetMkt-Forks"  # Name of the destination organization


def transfer(owner, repo, new_owner, token):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = json.dumps({"new_owner": new_owner})

    response = httpx.post(
        f"https://api.github.com/repos/{owner}/{repo}/transfer",
        headers=headers,
        data=data,
    )

    # response.raise_for_status()

    return response


# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = Auth.Token(TOKEN)

# First create a Github instance:

# Public Web Github
g = Github(auth=auth)

myname = g.get_user().login

for repo in g.get_user(login=myname).get_repos():

    if repo.fork and not repo.private:
        print(f"Transferring {repo.name}...")
        print(repo, repo.fork)

        # input("Press Enter to confirm...")

        # Transfer the repo
        resp = transfer(myname, repo.name, DESTINATION, TOKEN)

        print(resp.status_code)
        if resp.status_code == 202:
            print(f"Transferred {repo.name}.")
        else:
            print(f"Failed to transfer {repo.name}.")
            print(resp.text)
            # input("Press Enter to continue...")


# To close connections after use
g.close()
