#!/usr/bin/env python3
import argparse, csv, json, pathlib, re
from datetime import date

def slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+","_",s)
    s = re.sub(r"_+","_",s).strip("_")
    return s

def read_profiles_md(folder: pathlib.Path) -> dict:
    profiles = {}
    if not folder.exists():
        return profiles
    for p in folder.glob("*.md"):
        profiles[p.stem] = p.read_text(encoding="utf-8").strip()
    return profiles

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dept", required=True)
    ap.add_argument("--csv", default="intake/faculty.csv")
    ap.add_argument("--profiles", default="intake/faculty_profiles")
    ap.add_argument("--out_index", default="data/faculty_index.json")
    ap.add_argument("--out_dir", default="data/faculty")
    args = ap.parse_args()

    csv_path = pathlib.Path(args.csv)
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    profiles = read_profiles_md(pathlib.Path(args.profiles))

    faculty_index = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fid = (row.get("id") or "").strip() or slug(row["name"])
            kws = [k.strip() for k in (row.get("keywords","") or "").replace("|",";").split(";") if k.strip()]
            record = {
                "id": fid,
                "name": row["name"].strip(),
                "title": (row.get("title","") or "").strip(),
                "affiliation": (row.get("affiliation") or args.dept).strip(),
                "homepage": (row.get("homepage","") or "").strip(),
                "keywords": kws,
                "summary": (row.get("summary","") or "").strip(),
                "profile_text": profiles.get(fid,""),
                "updated": date.today().isoformat(),
            }
            (out_dir / f"{fid}.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

            faculty_index.append({
                "id": record["id"],
                "name": record["name"],
                "title": record["title"],
                "summary": record["summary"],
                "keywords": record["keywords"],
            })

    pathlib.Path(args.out_index).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.out_index).write_text(json.dumps(faculty_index, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(faculty_index)} faculty cards to {args.out_index} and per-faculty JSON to {args.out_dir}/")

if __name__ == "__main__":
    main()
