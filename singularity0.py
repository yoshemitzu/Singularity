import requests
from atproto import Client

from credentials import USERNAME,APP_PASSWORD
client = Client()
client.login(USERNAME, APP_PASSWORD)

# Base API URLs
BGS_HOST = "https://bsky.social"
AUTH_URL = f"{BGS_HOST}/xrpc/com.atproto.server.createSession"
FEED_URL = f"{BGS_HOST}/xrpc/app.bsky.feed.getFeed"

# Authenticate and get access token
def get_auth_token():
    response = requests.post(AUTH_URL, json={"identifier": USERNAME, "password": APP_PASSWORD})
    response.raise_for_status()
    return response.json()["accessJwt"]

# Fetch posts from Newskies
def fetch_newskies_feed(auth_token):
##    params = {"feed": "at://newskies.bsky.social/app.bsky.feed.generator/newskies"}
    params = {"feed": "at://did:plc:wzsilnxf24ehtmmc3gssy5bu/app.bsky.feed.generator/newskies"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(FEED_URL, params=params, headers=headers)
    response.raise_for_status()
    return response.json()["feed"]

# Keywords to filter by
KEYWORDS = ["music", "tech", "news"]

# Filter posts by keywords
def filter_posts(posts):
    return [p for p in posts if any(k.lower() not in p['post']['record']['text'].lower() for k in KEYWORDS)]

# Main function
def main():
    auth_token = get_auth_token()
    posts = fetch_newskies_feed(auth_token)
    filtered_posts = filter_posts(posts)

    for post in filtered_posts:
        text = post["post"]["record"]["text"]
        handle = post["post"]["author"]["handle"]
        print(f"{handle}: {text}")

    return filtered_posts

if __name__ == "__main__":
    main()
