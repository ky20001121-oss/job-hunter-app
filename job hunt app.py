import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_send_message():
    # 1. 鍵の読み込み
    line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = os.getenv('USER_ID')

    # 2. ブラウザ起動（サイトが開けるかだけのテスト）
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    
    target_url = "https://en-gage.net/user/search/list/?keyword=求人&area=47"
    driver.get(target_url)
    page_title = driver.title  # サイトのタイトル（「エンゲージ」など）を取得
    driver.quit()

    # 3. 無条件でLINEを送信する
    # サイトから求人が拾えなくても、このメッセージを強制的に送ります
    message = f"【動作確認】\nシステムは動いています！\nサイト接続：成功\nサイト名：{page_title}\n\nこれが届いたら、次は求人抽出の修正だけです！"
    
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {line_token}"
    }
    data = {
        "to": user_id,
        "messages": [{"type": "text", "text": text}] # ここを修正しました
    }
    
    # 送信実行
    response = requests.post(url, headers=headers, json={"to": user_id, "messages": [{"type": "text", "text": message}]})
    
    if response.status_code == 200:
        print("LINEへメッセージを送信しました！スマホを確認してください。")
    else:
        print(f"LINE送信失敗。エラー内容: {response.text}")

if __name__ == "__main__":
    test_send_message()
