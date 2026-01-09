# MLflow_demo




## dependencies

* Ubuntu 22.04
* Python 3.10（標準で入ってるはず）
* 端末を2つ使う（A: サーバ、B: デモ実行）

---

## venv作ってMLflowを入れる

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install mlflow
```

確認：

```bash
mlflow --version
```

---

## MLflow Tracking Server を起動（ローカルDB/ローカル保存）

```bash
mkdir -p mlruns_artifacts

mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns_artifacts
```

* `mlflow.db` がメタデータDB（SQLite）
* `mlruns_artifacts/` がログやファイル（artifact）の置き場

ブラウザで開く：
`http://localhost:5000`

---

## デモ用スクリプト（Runに設定・指標・ログファイルを紐づけ）

別ターミナル（B）で：

```bash
cd ~/mlflow_demo
source .venv/bin/activate
```

実行：

```bash
python demo_run.py
```

ブラウザ（`http://localhost:5000`）で
Experiment → Runs が1件増えて、Params/Metrics/Artifacts が見えるはずです。

