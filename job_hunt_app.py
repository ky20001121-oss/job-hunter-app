import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_jobs():
    line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = os.getenv('USER_ID')

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # ロボット感を消すための設定
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # シンプルに「エンジニア」で検索
    search_url = "https://en-gage.net/user/search/list/?keyword=%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2&area=47"
    
    print(f"検索を開始します: {search_url}")
    driver.get(search_url)

    new_jobs = []
    try:
        # 💡 ここが重要：h3タグ（求人タイトル）が表示されるまで最大20秒待つ
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
        
        # ページが安定するまで少し追加待機
        time.sleep(3)

        # 求人のタイトルをすべて取得
        items = driver.find_elements(By.TAG_NAME, "h3")
        
        for item in items:
            text = item.text.strip()
            # 短すぎる文字（メニュー名など）を除外
            if len(text) > 8: 
                new_jobs.append(f"📌 {text}")
                if len(new_jobs) >= 5: break # 最大5件
                
    except Exception as e:
        print(f"待機中にタイムアウトまたはエラー: {e}")

    driver.quit()

    if new_jobs:
        message = "【本番通知】沖縄のエンジニア求人を検出しました！\n\n" + "\n\n".join(new_jobs)
        send_line(line_token, user_id, message)
        print(f"成功: {len(new_jobs)}件送信しました。")
    else:
        # もしダメなら今のページのタイトルを表示してヒントにする
        print(f"取得失敗。現在のページタイトル: {driver.title}")

def send_line(token, to, text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"to": to, "messages": [{"type": "text", "text": text}]}
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    scrape_jobs()
