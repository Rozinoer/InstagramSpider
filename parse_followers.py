import glob
import json
import subprocess

rm = """rm -r json/*"""

fbv = glob.glob("json/followed*.json")
fv = glob.glob("json/follows*.json")


def parse():
    followers = {}
    for f in fv:
        with open(f, 'r') as file:
            data = json.load(file)
            for user in data['data']['user']['edge_followed_by']['edges']:
                followers[user['node']['id']] = {
                    'id': user['node']['id'],
                    'username': user['node']['username'],
                    'full_name': user['node']['full_name'],
                    'followed_by_viewer': user['node']['followed_by_viewer'],  # подписан я
                    'follows_viewer': user['node']['follows_viewer']  # подписаны на меня
                }

    followers = list(followers.values())

    followers_on = {}
    for f in fbv:
        with open(f, 'r') as file:
            data = json.load(file)
            for user in data['data']['user']['edge_follow']['edges']:
                followers_on[user['node']['id']] = {
                    'id': user['node']['id'],
                    'username': user['node']['username'],
                    'full_name': user['node']['full_name'],
                    'followed_by_viewer': user['node']['followed_by_viewer'],  # подписан я
                    'follows_viewer': user['node']['follows_viewer']  # подписаны на меня
                }

    followers_on = list(followers_on.values())

    with open('followers.json', 'w') as f:
        json.dump(followers, f)
    i = 0
    for follower in followers_on:
        if follower not in followers:
            print(follower["username"])
            i += 1
    print(i)

    subprocess.run(rm, shell=True, capture_output=True)


parse()
