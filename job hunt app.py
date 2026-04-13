import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_engage_jobs_auto():
    line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = os.getenv('USER_ID')

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    
    # テスト用にキーワードを「求人」のみ、エリアを「沖縄」に固定
    search_url = "https://en-gage.net/user/search/list/?keyword=求人&area=47"
    driver.get(search_url)
    
    # ページが完全に読み込まれるまで最大10秒待つ
    time.sleep(5) 

    new_jobs = []
    try:
        # 求人のタイトルが含まれる要素（h3タグ）をすべて探す
        titles = driver.find_elements(By.TAG_NAME, "h3")
        links = driver.find_elements(By.TAG_NAME, "a")

        # とにかく最初の3件を無理やり取得する
        count = 0
        for title_el in titles:
            title_text = title_el.text.strip()
            if title_text and count < 3:
                # 親要素を辿ってリンクを探すか、適当なリンクを紐付ける
                new_jobs.append(f"【テスト通知】\nタイトル: {title_text}\nURL: {search_url}")
                count += 1
    except Exception as e:
        print(f"エラー発生: {e}")

    driver.quit()

    if new_jobs:
        message = "求人情報を取得しました！\n\n" + "\n\n".join(new_jobs)
        send_line_message(line_token, user_id, message)
        print(f"成功！{len(new_jobs)}件送信しました。")
    else:
        # デバッグ用：今の画面に何が映っているかテキストで出す
        print("求人が見つかりません。サイトの仕様が変わった可能性があります。")

def send_line_message(token, to_user, text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "to": to_user,
        "messages": [{"type": "text", "text": text}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"LINEエラー: {response.text}")

if __name__ == "__main__":
    scrape_engage_jobs_auto()
