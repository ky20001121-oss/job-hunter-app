import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrape_jobs():
    line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = os.getenv('USER_ID')

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    
    # 検索条件：沖縄県(area=47) × エンジニア/技術職(category=2001)
    # 状況に合わせてキーワードを変更してください
    search_url = "https://en-gage.net/user/search/list/?keyword=%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2&area=47"
    
    print(f"検索を開始します: {search_url}")
    driver.get(search_url)
    time.sleep(5)  # 読み込み待ち

    new_jobs = []
    # 求人カードの要素を取得（エンゲージの現在の構造に対応）
    job_elements = driver.find_elements(By.CSS_SELECTOR, "div.p-search_list_item")

    for job in job_elements[:3]:  # 上位3件をチェック
        try:
            title = job.find_element(By.CSS_SELECTOR, "h3").text
            link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            new_jobs.append(f"📌 {title}\n🔗 {link}")
        except:
            continue

    driver.quit()

    if new_jobs:
        message = "【本番通知】沖縄のエンジニア求人を見つけました！\n\n" + "\n\n".join(new_jobs)
        send_line(line_token, user_id, message)
        print(f"成功: {len(new_jobs)}件送信しました。")
    else:
        # 0件だとActionsが寂しいのでログだけ出す
        print("現在、条件に合う新しい求人は見つかりませんでした。")

def send_line(token, to, text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"to": to, "messages": [{"type": "text", "text": text}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    scrape_jobs()
