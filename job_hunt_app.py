import os
import requests

def diagnostic_test():
    line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = os.getenv('USER_ID')

    # メッセージ内容を「強制送信」に固定
    message = "【最終診断】このメッセージが見えたら接続成功です！"
    
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {line_token}"
    }
    data = {
        "to": user_id,
        "messages": [{"type": "text", "text": message}]
    }
    
    print("送信テストを開始します...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("💡結果: LINEへメッセージを送信しました！")
    else:
        print(f"❌結果: LINE送信失敗。理由: {response.text}")

if __name__ == "__main__":
    diagnostic_test()
