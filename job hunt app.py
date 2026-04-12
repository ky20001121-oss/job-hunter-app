import os
import time
import csv
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- GitHub Secretsから設定を読み込む ---
LINE_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
USER_ID = os.environ.get('USER_ID')

def send_line_message(message_text):
    """LINE Messaging APIを使って通知を送る関数"""
    if not LINE_TOKEN or not USER_ID:
        print("エラー: LINEのトークンまたはユーザーIDが設定されていません。")
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    payload = {
        "to": USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message_text
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print("LINE通知を送信しました。")
    except Exception as e:
        print(f"LINE通知の送信に失敗しました: {e}")

def scrape_engage_jobs_auto():
    # --- クラウド(Linux)環境向けのブラウザ設定 ---
    options = Options()
    options.add_argument('--headless')  # 画面を表示しない
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # WebDriverのセットアップ
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # エンゲージの検索結果ページ（例：沖縄・エンジニア）へアクセス
        # 検索条件に合わせてURLを変更してください
        search_url = "https://en-gage.net/user/search/list/?keyword=エンジニア&area=47"
        driver.get(search_url)
        time.sleep(3)

        # 求人タイトルを取得（例として最初の3件）
        job_elements = driver.find_elements(By.CSS_SELECTOR, "h3.job_title")[:3]
        
        if job_elements:
            message = "【最新の求人情報】\n"
            for job in job_elements:
                message += f"・{job.text}\n"
            
            # LINEに送信
            send_line_message(message)
        else:
            print("新しい求人は見つかりませんでした。")

    except Exception as e:
        print(f"スクレイピング中にエラーが発生しました: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_engage_jobs_auto()