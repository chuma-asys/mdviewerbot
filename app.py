import os
import re
import requests
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv
from markdown import markdown
from datetime import datetime

# 環境変数読み込み
load_dotenv()

# Slack Boltの初期化
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)
handler = SlackRequestHandler(app)
flask_app = Flask(__name__)

# GitHub情報
GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
REPO_NAME = os.environ["REPO_NAME"]

# イベントエンドポイント
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# メンション応答
@app.event("app_mention")
def handle_mention(event, say):
    say("👋 こんにちは！Markdownファイルを投稿してくれたら整形してURLを返します！")

# Markdownファイル検出時の処理
@app.event("file_shared")
def handle_file_shared(event, say, client):
    file_id = event["file"]["id"]
    file_info = client.files_info(file=file_id)["file"]
    file_name = file_info["name"]
    file_type = file_info.get("filetype", "")

    if file_type != "markdown" and not file_name.endswith(".md"):
        say("📄 Markdownファイルではありませんでした。")
        return

    say("📄 Markdownファイルを受け取りました！（処理中...）")

    headers = {
        "Authorization": f"Bearer {os.environ['SLACK_BOT_TOKEN']}"
    }
    url = file_info["url_private_download"]
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        say("❌ ファイルの取得に失敗しました。")
        return

    md_content = response.text
    html_body = markdown(md_content)

    # ファイル名整形（例：20250614_1432_filename.html）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r"[^a-zA-Z0-9_-]", "", file_name.replace(".md", ""))
    output_name = f"{timestamp}_{slug}.html"
    output_path = os.path.join("docs", output_name)

    html_template = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{file_name}</title>
  <style>
    body {{ font-family: sans-serif; padding: 2rem; }}
    h1, h2, h3 {{ border-bottom: 1px solid #ddd; }}
    pre, code {{ background: #f8f8f8; padding: 0.5rem; border-radius: 4px; }}
  </style>
</head>
<body>
{html_body}
</body>
</html>"""

    # HTML保存
    os.makedirs("docs", exist_ok=True)
    with open(output_path, "w") as f:
        f.write(html_template)

    # GitHubにコミット＆プッシュ
    commit_msg = f"Add Markdown view: {output_name}"
    os.system("git add docs")
    os.system(f'git commit -m "{commit_msg}"')
    os.system("git push origin main")

    # 公開URLを生成してSlackに返信
    view_url = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/{output_name}"
    say(f"✅ Markdownファイルを整形・保存しました！こちらでご覧いただけます：\n{view_url}")

# Flaskサーバー起動
if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=3000)
