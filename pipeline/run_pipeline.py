"""Run collection, normalization, quality checks, and optional PostgreSQL load."""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from frontend import collector  # noqa: E402


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def quality_check(rows: list[dict]) -> dict:
    required = ("facility_name", "address", "city", "district")
    missing_required = sum(1 for row in rows if any(not str(row.get(key, "")).strip() for key in required))
    duplicate_keys = len(rows) - len({(row.get("facility_name", ""), row.get("address", "")) for row in rows})
    invalid_coordinates = 0
    for row in rows:
        try:
            if row.get("latitude") and not -90 <= float(row["latitude"]) <= 90:
                invalid_coordinates += 1
            if row.get("longitude") and not -180 <= float(row["longitude"]) <= 180:
                invalid_coordinates += 1
        except (TypeError, ValueError):
            invalid_coordinates += 1
    return {"missing_required": missing_required, "duplicate_keys": duplicate_keys, "invalid_coordinates": invalid_coordinates, "status": "CHECK_PASSED" if not (missing_required or duplicate_keys or invalid_coordinates) else "CHECK_FAILED"}


def write_outputs(payload: dict, rows: list[dict]) -> None:
    out = ROOT / "output"
    raw = out / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    for name, value in payload["raw"].items():
        (raw / f"{name}.json").write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = ["facility_name", "facility_type", "address", "city", "district", "phone", "homepage", "latitude", "longitude", "indoor_outdoor"]
    with (out / "facilities.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    (out / "facilities_normalized.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def load_postgres(rows: list[dict]) -> int:
    import psycopg

    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        raise RuntimeError("--load-db를 사용하려면 DATABASE_URL이 필요합니다.")
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE SCHEMA IF NOT EXISTS processed")
            cur.execute("""CREATE TABLE IF NOT EXISTS processed.facility_pipeline (
                facility_name text NOT NULL, facility_type text, address text,
                city text, district text, phone text, homepage text,
                latitude double precision, longitude double precision,
                indoor_outdoor text, collected_at timestamptz NOT NULL
            )""")
            cur.execute("TRUNCATE processed.facility_pipeline")
            with cur.copy("COPY processed.facility_pipeline (facility_name, facility_type, address, city, district, phone, homepage, latitude, longitude, indoor_outdoor, collected_at) FROM STDIN") as copy:
                now = utc_now()
                for row in rows:
                    copy.write_row((row.get("facility_name", ""), row.get("facility_type", ""), row.get("address", ""), row.get("city", ""), row.get("district", ""), row.get("phone", ""), row.get("homepage", ""), row.get("latitude") or None, row.get("longitude") or None, row.get("indoor_outdoor", ""), now))
        conn.commit()
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--nx", type=int, default=int(os.getenv("KMA_NX", "60")))
    parser.add_argument("--ny", type=int, default=int(os.getenv("KMA_NY", "127")))
    parser.add_argument("--station", default=os.getenv("AIRKOREA_STATION", ""))
    parser.add_argument("--load-db", action="store_true")
    args = parser.parse_args()
    started = utc_now()
    run_id = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}"
    raw: dict = {}
    errors: dict = {}
    jobs = {"facilities": lambda: collector.fetch_facilities(args.region, args.limit), "weather": lambda: collector.fetch_weather(args.nx, args.ny), "air": lambda: collector.fetch_air(args.station or args.region)}
    for name, fn in jobs.items():
        try:
            raw[name] = fn()
        except Exception as exc:
            raw[name] = {"error": str(exc)}
            errors[name] = str(exc)
    rows = collector.normalize_facilities(raw["facilities"]) if "error" not in raw["facilities"] else []
    quality = quality_check(rows)
    if errors:
        quality["status"] = "CHECK_FAILED"
        quality["source_errors"] = sorted(errors)
    payload = {"run_id": run_id, "collected_at": started, "region": args.region, "raw": raw, "facilities": rows, "quality": quality, "errors": errors}
    write_outputs(payload, rows)
    loaded = 0
    load_status = "skipped"
    if args.load_db and quality["status"] == "CHECK_PASSED":
        loaded = load_postgres(rows)
        load_status = "loaded"
    elif args.load_db:
        load_status = "blocked_by_quality_check"
    finished = utc_now()
    source_count = len(collector.items_from_response(raw["facilities"].get("data", {}))) if "error" not in raw["facilities"] else 0
    log = {"run_id": run_id, "started_at": started, "finished_at": finished, "region": args.region, "collected_count": source_count, "normalized_count": len(rows), "loaded_count": loaded, "quality_status": quality["status"], "load_status": load_status, "errors": errors}
    log_dir = ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    with (log_dir / f"pipeline-{datetime.now():%Y%m%d}.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(log, ensure_ascii=False) + "\n")
    print(json.dumps(log, ensure_ascii=False, indent=2))
    return 0 if quality["status"] == "CHECK_PASSED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
