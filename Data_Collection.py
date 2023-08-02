import requests
from concurrent.futures import ThreadPoolExecutor

# List of access tokens with "public_repo" scope
access_tokens = ["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", "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",
                 "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", "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",
                 "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"]

# Query parameters
params = {"q": "type:user", "per_page": 100}

# Endpoint for searching users
endpoint = "https://api.github.com/search/users"


# Function to retrieve user information
def get_user_info(user, access_token):
    headers = {"Authorization": f"token {access_token}"}
    user_endpoint = f"https://api.github.com/users/{user['login']}"
    user_response = requests.get(user_endpoint, headers=headers)
    if user_response.status_code == 200:
        # Retrieve the user's repositories
        repo_endpoint = f"https://api.github.com/users/{user['login']}/repos"
        repo_response = requests.get(repo_endpoint, headers=headers)
        if repo_response.status_code == 200:
            repos = repo_response.json()
            languages = set()
            for repo in repos:
                if repo["language"]:
                    languages.add(repo["language"])
            return {
                "username": user["login"],
                "email": user_response.json().get("email", "N/A"),
                "followers": user_response.json().get("followers", "N/A"),
                "type": user_response.json().get("type", "N/A"),
                "number of repos": user_response.json().get("public_repos", "N/A"),
                "achievements": user_response.json().get("public_gists", "N/A"),
                "languages": ", ".join(sorted(languages))
            }
        else:
            print(f"Error retrieving repositories for {user_endpoint}. Status code: {repo_response.status_code}")
            print(f"Response content: {repo_response.content}")
    else:
        print(f"Error retrieving user details for {user_endpoint}. Status code: {user_response.status_code}")
        print(f"Response content: {user_response.content}")
    return None


# Retrieve the search results
user_data = []
for i in range(5):
    access_token = access_tokens[i % len(access_tokens)]
    headers = {"Authorization": f"token {access_token}"}
    with ThreadPoolExecutor(max_workers=5) as threadexecutor:
        for page in range(1, 11):
            params["page"] = page
            response = requests.get(endpoint, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                users = data["items"]
                emptylist = []
                for user in users:
                    emptylist.append(threadexecutor.submit(get_user_info, user, access_token))
                for future in emptylist:
                    result = future.result()
                    if result is not None:
                        user_data.append(result)
            else:
                print(f"Error retrieving search results. Status code: {response.status_code}")
                print(f"Response content: {response.content}")

