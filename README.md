# MDViewerBot

Slack上でMarkdownファイル（.md）を整形して表示するBotです。

## 起動方法

```bash
source venv/bin/activate
export $(cat .env | xargs)
python app.py
