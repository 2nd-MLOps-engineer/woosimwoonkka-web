"""Small APScheduler entrypoint for repeatable evaluation runs."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    from apscheduler.schedulers.blocking import BlockingScheduler

    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True)
    parser.add_argument("--interval-hours", type=int, default=6)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    scheduler = BlockingScheduler(timezone="Asia/Seoul")

    def run_once() -> None:
        subprocess.run([sys.executable, str(ROOT / "pipeline" / "run_pipeline.py"), "--region", args.region, "--limit", str(args.limit), "--load-db"], check=False)

    run_once()
    scheduler.add_job(run_once, "interval", hours=args.interval_hours, id="woosimwoonkka-pipeline", max_instances=1, coalesce=True)
    print(f"scheduler started: every {args.interval_hours}h, region={args.region}")
    scheduler.start()


if __name__ == "__main__":
    main()
