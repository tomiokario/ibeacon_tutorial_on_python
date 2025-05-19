# beaconをPythonから扱うためのチュートリアル

## how to start

0. 仮想環境を使いたい場合は，[how_to_use_venv.md](docs/venv/how_to_use_venv.md)を参照してください

1. 依存関係のインストール
```
pip install -r requirements.txt
```

2. 環境のチェック
```
python check_env.py
```

3. プログラムの実行
```
python xxxx.py
```

## ファイル名
ibeacon_monitor.py
- 閾値を超えるRSSIが検知されとき，タイムスタンプ，UUID，ビーコン名，RSSIをprintする
- ctrl + cで終了する

ibeacon_monitor_csv.py
- 10秒間bluetoothをスキャンして，検出された情報をcsvファイルに保存します