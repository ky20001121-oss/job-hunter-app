import os
import requests
import xml.etree.ElementTree as ET

def scrape_rss():
    line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = os.getenv('USER_ID')

    # 今回は「Qiitaの最新IT記事」を取得する例です（確実に動きます）
    # 就職活動のネタや技術トレンドの把握に役立ちます！
    rss_url = "https://qiita.com/popular-items/feed"
    
    print(f"RSSフィードを取得開始: {rss_url}")
    new_items = []

    try:
        response = requests.get(rss_url)
        # XML形式のデータを解析
        root = ET.fromstring(response.content)
        
        # QiitaのフィードからタイトルとURLを抽出
        # ※XMLのタグ構造に合わせています
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry')[:5]:
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            link = entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']
            new_items.append(f"📖 {title}\n🔗 {link}")

    except Exception as e:
        print(f"エラー発生: {e}")

    if new_items:
        message = "【技術トレンド通知】今注目のIT記事をピックアップしました！\n\n" + "\n\n".join(new_items)
        send_line(line_token, user_id, message)
        print(f"成功: {len(new_items)}件を送信しました。")
    else:
        print("記事を取得できませんでした。")

def send_line(token, to, text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    payload = {"to": to, "messages": [{"type": "text", "text": text}]}
    res = requests.post(url, headers=headers, json=payload)
    print(f"LINE送信結果: {res.status_code}")

if __name__ == "__main__":
    scrape_rss()
