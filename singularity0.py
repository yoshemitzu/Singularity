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
def fetch_feed(auth_token,feed_info):
    location,name = feed_info[0],feed_info[1]
    params = {"feed": f"at://{location}/app.bsky.feed.generator/{name}"}
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = requests.get(FEED_URL, params=params, headers=headers)
    response.raise_for_status()
    return response.json()["feed"]

# Filter posts by keywords
def filter_posts(posts,KEYWORDS):
    return [p for p in posts if any(k.lower() not in p['post']['record']['text'].lower() for k in KEYWORDS)]

# feeds of interest
feed_dict = {"newskies":["did:plc:wzsilnxf24ehtmmc3gssy5bu","newskies"]}
feed_info = feed_dict["newskies"]

# Keywords to filter by
KEYWORDS = ["music", "tech", "news"]

# Main function
def main():
    auth_token = get_auth_token()
    posts = fetch_feed(auth_token,feed_info)
    filtered_posts = filter_posts(posts,KEYWORDS)

    for post in filtered_posts:
        text = post["post"]["record"]["text"]
        handle = post["post"]["author"]["handle"]
        print(f"{handle}: {text}")

    return filtered_posts

if __name__ == "__main__":
    main()
