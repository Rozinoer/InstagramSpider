import subprocess
import time
import urllib.parse
import json
from pprint import pprint

url_base = 'https://www.instagram.com/graphql/query/?'

followed_by_viewer = """curl '{url}' \
  -H 'authority: www.instagram.com' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.77 YaBrowser/20.11.0.918 Yowser/2.5 Safari/537.36' \
  -H 'accept: */*' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://www.instagram.com/suerstorff/' \
  -H 'accept-language: ru,en;q=0.9' \
  -H 'cookie: ig_did=C7260445-E17A-4695-87B6-7C9492AD0954; mid=YBCdMAAEAAGHOCWKRnePx15f94tD; ig_nrcb=1; csrftoken=JobQeb5jVlr1gtz0qGTSwlevAz9ClR7q; ds_user_id=1720899220; sessionid=1720899220%3AYMuNQrgVhFRbS3%3A14; shbid=357; shbts=1611701588.71077; rur=ATN;urlgen="{{\"37.204.158.31\": 42610}}:1l4pYT:gYwPxMFUzPQ6n5myfsxMFH65AMc"' \
  --compressed > json/followed_by_viewer_{index}.json"""

follows_viewer = """curl '{url}' \
  -H 'authority: www.instagram.com' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.77 YaBrowser/20.11.0.918 Yowser/2.5 Safari/537.36' \
  -H 'accept: */*' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'referer: https://www.instagram.com/suerstorff/' \
  -H 'accept-language: ru,en;q=0.9' \
  -H 'cookie: ig_did=C7260445-E17A-4695-87B6-7C9492AD0954; mid=YBCdMAAEAAGHOCWKRnePx15f94tD; ig_nrcb=1; csrftoken=JobQeb5jVlr1gtz0qGTSwlevAz9ClR7q; ds_user_id=1720899220; sessionid=1720899220%3AYMuNQrgVhFRbS3%3A14; shbid=357; shbts=1611701588.71077; rur=ATN;urlgen="{{\"37.204.158.31\": 42610}}:1l4pYT:gYwPxMFUzPQ6n5myfsxMFH65AMc"' \
  --compressed > json/follows_viewer_{index}.json"""

index = 1
after = None
in_current_batch = 0
user_id = 1552392772
while True:
    after_value = f',"after": "{after}"' if after else ''
    variables = f'{{"id": "{user_id}", "include_reel": true, "fetch_mutual": false, "first": 50{after_value}}}'
    get_params = {
        'query_hash': '5aefa9893005572d237da5068082d8d5',
        'variables': variables
    }
    ws_url = url_base + urllib.parse.urlencode(get_params)
    result = subprocess.run(follows_viewer.format(url=ws_url, index=index), shell=True, capture_output=True)
    if result.returncode != 0:
        exit("Ошибка!")

    with open(f'json/follows_viewer_{index}.json', 'r') as f:
        data = json.load(f)

    after = data['data']['user']['edge_followed_by']['page_info']['end_cursor']
    all_followers = data['data']['user']['edge_followed_by']['count']
    in_current_batch += len(data['data']['user']['edge_followed_by']['edges'])
    print(f'Обработано {in_current_batch} из {all_followers}')
    if not data['data']['user']['edge_followed_by']['page_info']['has_next_page']:
        break
    time.sleep(5 if index % 10 != 0 else 20)
    index = index + 1


index = 1
after = None
in_current_batch = 0
while True:
    after_value = f',"after": "{after}"' if after else ''
    variables = f'{{"id": "{user_id}", "include_reel": true, "fetch_mutual": false, "first": 50{after_value}}}'
    get_params = {
        'query_hash': '3dec7e2c57367ef3da3d987d89f9dbc8',
        'variables': variables
    }
    ws_url = url_base + urllib.parse.urlencode(get_params)
    result = subprocess.run(followed_by_viewer.format(url=ws_url, index=index), shell=True, capture_output=True)
    if result.returncode != 0:
        exit("Ошибка!")

    with open(f'json/followed_by_viewer_{index}.json', 'r') as f:
        data = json.load(f)

    after = data['data']['user']['edge_follow']['page_info']['end_cursor']
    all_followers = data['data']['user']['edge_follow']['count']
    in_current_batch += len(data['data']['user']['edge_follow']['edges'])
    print(f'Обработано {in_current_batch} из {all_followers}')
    if not data['data']['user']['edge_follow']['page_info']['has_next_page']:
        break
    time.sleep(5 if index % 10 != 0 else 20)
    index = index + 1

print('Готово')
