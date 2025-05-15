import os
import datetime
import json
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # クエリパラメータを取得
    gad_source = request.args.get('gad_source')
    gad_campaignid = request.args.get('gad_campaignid')

    # 条件チェック
    if gad_source and gad_campaignid:
        # 現在時刻をUNIXタイムスタンプエポックマイクロ秒で取得
        # Pythonのdatetime.timestamp()は秒単位なので、1,000,000を掛ける
        session_start_time_usec = int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1_000_000)

        # ログデータを辞書として準備
        log_data = {
            "gad_source": gad_source,
            "gad_campaignid": gad_campaignid,
            "landing_page_url": request.url, # 完全なURL
            "session_start_time_usec": session_start_time_usec,
            "landing_page_referrer": request.referrer or "N/A", # リファラがない場合は "N/A"
            "landing_page_user_agent": request.user_agent.string
        }

        # Cloud Loggingは標準出力/標準エラー出力へのJSON文字列を構造化ログとして解釈する
        print(json.dumps(log_data))

    # HTMLページをレンダリングして返す
    return render_template('index.html')

if __name__ == "__main__":
    # Cloud RunがPORT環境変数を設定するので、それに従う
    # ローカル開発時はデフォルトで8080を使用
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)