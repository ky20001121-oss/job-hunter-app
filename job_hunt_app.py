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
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # 沖縄のITエンジニア求人に絞ったURL
    search_url = "https://求人ボックス.com/沖縄県のITエンジニアの求人"
    
    print(f"検索開始: {search_url}")
    new_jobs = []

    try:
        driver.get(search_url)
        time.sleep(8) # 読み込みを待つ

        # ターゲット：求人ボックスのタイトルが入る可能性のある場所を総ざらい
        selectors = [
            "span.k-p-title", 
            "h3.s-jobTitle", 
            "p.s-jobTitle",
            "div.p-job__title"
        ]
        
        for selector in selectors:
            items = driver.find_elements(By.CSS_SELECTOR, selector)
            for item in items:
                text = item.text.strip()
                if len(text) >= 5: # 短すぎるゴミデータを除外
                    new_jobs.append(f"📌 {text}")
            
            if new_jobs: break # 何か見つかったらループを抜ける

    except Exception as e:
        print(f"解析エラー: {e}")
    
    driver.quit()

    if new_jobs:
        # 重複を削除して最大5件送信
        unique_jobs = list(dict.fromkeys(new_jobs))[:5]
        message = "【最新】沖縄のエンジニア求人を見つけました！\n\n" + "\n\n".join(unique_jobs)
        send_line(line_token, user_id, message)
        print(f"成功: {len(unique_jobs)}件をLINEに送りました。")
    else:
        print(f"求人タイトルが見つかりませんでした。別の構造を探す必要があります。")

def send_line(token, to, text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"to": to, "messages": [{"type": "text", "text": text}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    scrape_jobs()
