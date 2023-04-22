import json
import requests
import datetime

# Slack Webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# Slackメッセージを作成する関数
def create_slack_message(report):
    message = {
        "username": "荒井信輝 Nobuteru Arai",
        "icon_emoji": ":thinking_face:",
        "text": f"*本日の日報*\n\n"
                f"本日の目標（TODO目標/できるようになりたいこと）: {report['goal']}\n"
                f"学習時間（Hour）: {report['learning_hours']} hours\n"
                f"目標振り返り（TODO進捗/できるようになりたいこと振り返り）: {report['reflection']}\n"
                f"詰まっていること（実現したいこと/現状/行ったこと/仮説）: {report['blocker']}\n"
                f"学んだこと（新しい気付き、学び）: {report['learning']}\n"
                f"感想（一日の感想、雑談）: {report['impression']}\n"
                f"明日の目標（TODO目標/できるようになりたいこと）: {report['tomorrow_goal']}"
    }
    return message

# JSONファイルから日報の内容を読み込む関数
def load_report(report_path):
    with open(report_path, "r") as f:
        report = json.load(f)
    return report

# Slackに通知を送信する関数
def send_slack_notification(report):
    slack_message = create_slack_message(report)
    response = requests.post(SLACK_WEBHOOK_URL, json=slack_message)
    if response.status_code != 200:
        raise ValueError(f"Slackに通知を送信できませんでした。HTTPエラーコード: {response.status_code}")

# 日報のファイルパスを設定する
today = datetime.date.today().strftime('%Y-%m-%d')
report_path = f"diary/reports/{today}.json"

# 日報の内容を読み込む
report = load_report(report_path)

# Slackに通知を送信する
send_slack_notification(report)
