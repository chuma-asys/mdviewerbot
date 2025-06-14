# MDViewerBot

Slack上でMarkdownファイル（.md）を整形して表示するBotです。

## 起動方法

```bash
source venv/bin/activate
export $(cat .env | xargs)
python app.py


## 環境構築
あります！
Slack Bot（MDViewerBot）のようなPythonプロジェクトを始める際には、**最初に環境をしっかり整備しておくことがとても重要**です。以下に「最小で実用的」な Python プロジェクトの初期構成を、Slack Bot用途に特化して解説します。

---

## 🧱 Python Slack Bot プロジェクトの初期構成テンプレート

```
MDViewerBot/
├── app.py                     # メインアプリケーション
├── requirements.txt          # 必要なパッケージ定義
├── .env                      # シークレット設定（環境変数）
├── .gitignore                # Gitに含めないファイル
├── README.md                 # プロジェクト概要
├── .devcontainer/            # Codespaces用設定（任意）
│   └── devcontainer.json
└── docs/                     # GitHub Pages向けWebコンテンツ（任意）
```

---

## ✅ 1. Python環境の準備

```bash
python -m venv venv
source venv/bin/activate  # Windowsなら venv\Scripts\activate
```

---

## ✅ 2. 必要パッケージのインストールと `requirements.txt` 作成

```bash
pip install slack_bolt slack_sdk markdown python-dotenv requests
pip freeze > requirements.txt
```

📦 **含まれる主要パッケージ：**

* `slack_bolt`: SlackのBot SDK
* `slack_sdk`: 低レベルAPIも使いたい場合用
* `markdown`: `.md` をHTML化
* `requests`: `.md`ファイルのダウンロード用
* `python-dotenv`: `.env` の読み込み用

---

## ✅ 3. `.env` ファイルで秘密情報を管理（Git非公開）

```env
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
```

➡ `.gitignore` に以下を追加：

```
.env
venv/
__pycache__/
```

---

## ✅ 4. `README.md`（例）

````markdown
# MDViewerBot

Slack上でMarkdownファイル（.md）を整形して表示するBotです。

## 起動方法

```bash
source venv/bin/activate
export $(cat .env | xargs)
python app.py
````

## 必要な環境変数

* SLACK\_BOT\_TOKEN
* SLACK\_APP\_TOKEN

````

---

## ✅ 5. `app.py` の最小構成

```python
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv

load_dotenv()
app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_mention")
def handle_mention(event, say):
    say("こんにちは！MDViewerBotです。Markdownファイルがあれば貼ってください📄")

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
````

---

## ✅ 6. Codespaces向け（任意）

`.devcontainer/devcontainer.json` を追加して、GitHub Codespacesでもすぐ開発できるようにします。

```json
{
  "name": "MDViewerBot",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "postCreateCommand": "pip install -r requirements.txt"
}
```

---

## ✅ 7. Slack App連携の注意点（初期設定まとめ）

| 項目                      | 内容                                                 |
| ----------------------- | -------------------------------------------------- |
| **Bot Token Scopes**    | `chat:write`, `files:read`, `app_mentions:read` など |
| **Event Subscriptions** | ON → `file_shared`, `app_mention`                  |
| **Request URL**         | ngrokなどで作ったURLを設定                                  |
| **アプリのインストール**          | ワークスペースにインストール（ボタンで可）                              |

---

## ✨ オプション

* `logging` モジュールでログ管理
* `test/` ディレクトリでpytestなどのテスト追加
* `pyproject.toml` にツール統合（Black, Ruff, isortなど）

---

## 🎁 必要であれば…

* この構成をベースにしたGitHubテンプレートリポジトリを用意できます（Codespaces対応済）
* 自動起動スクリプトやMakefile、Slackの登録手順書も添付可能です

---

ご希望あれば「このままGitHubにテンプレ化してほしい」「このコードをZIPでまとめて」なども対応できます！どうしましょう？
```

