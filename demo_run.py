import os
import time
import json
import random
import mlflow

def main():
    # MLflowサーバの場所（同一マシンならこれでOK）
    mlflow.set_tracking_uri("http://127.0.0.1:5000")

    # 「Experiment」= 運用メニュー（例：現場×ルート×ミッション）
    mlflow.set_experiment("siteA_route1_patrol")

    robot_id = os.getenv("ROBOT_ID", "robot_A")
    mission_slot = os.getenv("SLOT", "morning")

    # 実行時の「設定スナップショット」例（paramsに入れる）
    config = {
        "max_speed_mps": 0.8,
        "obstacle_margin_m": 0.4,
        "nav_mode": "autonomous_patrol",
        "route_id": "route1",
        "camera_fps": 10,
    }

    # Run開始（= 巡回1回）
    with mlflow.start_run(run_name=f"{robot_id}_{mission_slot}") as run:
        run_id = run.info.run_id

        # タグ：検索・フィルタ用（robot_id / 現場 / スロット等）
        mlflow.set_tag("robot_id", robot_id)
        mlflow.set_tag("slot", mission_slot)
        mlflow.set_tag("site_id", "siteA")

        # Params：設定（フラットなキーが扱いやすい）
        for k, v in config.items():
            mlflow.log_param(k, v)

        # Metrics：結果サマリ（例：時間・距離・異常数など）
        patrol_seconds = random.randint(3000, 3800)  # 約1時間のつもり
        distance_m = random.uniform(2200, 3200)
        anomalies = random.randint(0, 3)
        battery_start = random.randint(70, 95)
        battery_end = max(10, battery_start - random.randint(15, 35))

        mlflow.log_metric("patrol_seconds", patrol_seconds)
        mlflow.log_metric("distance_m", distance_m)
        mlflow.log_metric("anomaly_count", anomalies)
        mlflow.log_metric("battery_start_pct", battery_start)
        mlflow.log_metric("battery_end_pct", battery_end)

        # Artifact：ログや観測データ（今回はダミーを作って保存）
        os.makedirs("artifacts", exist_ok=True)

        log_text = [
            f"run_id={run_id}",
            f"robot_id={robot_id}",
            f"slot={mission_slot}",
            f"start_time={time.strftime('%Y-%m-%d %H:%M:%S')}",
            "event=patrol_started",
            "event=checkpoint_passed id=cp_01",
            "event=checkpoint_passed id=cp_02",
            "event=patrol_finished",
        ]
        log_path = "artifacts/patrol.log"
        with open(log_path, "w") as f:
            f.write("\n".join(log_text) + "\n")

        # 設定スナップショットを丸ごとJSONとしても残す（超おすすめ）
        cfg_path = "artifacts/config_snapshot.json"
        with open(cfg_path, "w") as f:
            json.dump(config, f, indent=2)

        mlflow.log_artifact(log_path, artifact_path="logs")
        mlflow.log_artifact(cfg_path, artifact_path="config")

        print("Logged run:", run_id)

if __name__ == "__main__":
    main()
