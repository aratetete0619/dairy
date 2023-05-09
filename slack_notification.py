import json
import requests
import datetime
import os


# Slack Webhook URL

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

WAKATIME_API_KEY = "waka_6ea5f9dd-d4a2-407a-bd0c-f5ad9ffd0c43"


# Slackメッセージを作成する関数
def create_slack_message(report):
    message = {
        "username": "荒井信輝 Nobuteru Arai",
        "icon_emoji": ":open_mouth:",
        "text": f"*本日の日報*\n\n"
                f"## 本日の目標（TODO目標/できるようになりたいこと）\n{report['goal']}\n"
                f"学習時間（Hour）: {learning_hours_text}\n"
                f"## 目標振り返り（TODO進捗/できるようになりたいこと振り返り）\n{report['reflection']}\n"
                f"## 詰まっていること（実現したいこと/現状/行ったこと/仮説）\n{report['blocker']}\n"
                f"## 学んだこと（新しい気付き、学び）\n{report['learning']}\n"
                f"## 感想（一日の感想、雑談）\n{report['impression']}\n"
                f"## 明日の目標（TODO目標/できるようになりたいこと）\n{report['tomorrow_goal']}"
    }
    return message


# WakaTime APIからデータを取得する関数
def get_wakatime_data():
    url = f"https://wakatime.com/api/v1/users/current/summaries?api_key={WAKATIME_API_KEY}&start={today}&end={today}"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(
            f"WakaTime APIからデータを取得できませんでした。HTTPエラーコード: {response.status_code}"
        )
    data = response.json()
    return data


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
        raise ValueError(
            f"Slackに通知を送信できませんでした。HTTPエラーコード: {response.status_code}")


# 日報のファイルパスを設定する
today = datetime.date.today().strftime('%Y-%m-%d')
home = os.environ['HOME']
report_path = f"{home}/Apprentice/diary/reports/{today}.json"

# 日報の内容を読み込む
report = load_report(report_path)


# WakaTimeデータを取得する
wakatime_data = get_wakatime_data()["data"][0]

# 学習時間を表示するテキスト
if "learning_hours" in report:
    learning_hours_text = (
        f"{wakatime_data['grand_total']['text']} (WakaTime)"
        if not report["learning_hours"]
        else f"{wakatime_data['grand_total']['text']} (WakaTime) / {report['learning_hours']} hours (Manual)"
    )
else:
    report["learning_hours"] = wakatime_data['grand_total']['hours']
    learning_hours_text = f"{wakatime_data['grand_total']['text']} (WakaTime)"


# Slackに通知を送信する
send_slack_notification(report)
