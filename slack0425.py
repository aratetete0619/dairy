import json
import requests
import datetime
import os

# Slack Webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
WAKATIME_API_KEY = "waka_10997b33-3b1e-46ab-9275-51ead8efd29b"

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

# WakaTime APIからデータを取得する関数


def get_wakatime_data(specific_date):
    url = f"https://wakatime.com/api/v1/users/current/summaries?api_key={WAKATIME_API_KEY}&start={specific_date}&end={specific_date}"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(
            f"WakaTime APIからデータを取得できませんでした。HTTPエラーコード: {response.status_code}"
        )
    data = response.json()
    return data


# 日報のファイルパスを設定する
specific_date = "2023-04-26"
home = os.environ['HOME']
report_path = f"{home}/Apprentice/diary/reports/{specific_date}.json"

# 日報の内容を読み込む
report = load_report(report_path)

# WakaTimeデータを取得する
wakatime_data = get_wakatime_data(specific_date)["data"][0]


# 学習時間を表示するテキスト
learning_hours_text = (
    f"{wakatime_data['grand_total']['text']} (WakaTime)"
    if not report["learning_hours"]
    else f"{wakatime_data['grand_total']['text']} (WakaTime) / {report['learning_hours']} hours (Manual)"
)


# Slackに通知を送信する
send_slack_notification(report)
