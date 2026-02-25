#!/usr/bin/env python3
import json, sys

def die(msg):
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(2)

def main():
    if len(sys.argv) != 2:
        die("Usage: validate_teams.py data/teams.json")
    p = sys.argv[1]
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)

    teams = data.get("teams")
    if not isinstance(teams, list):
        die("teams.json must contain top level key 'teams' as a list")

    for i, t in enumerate(teams, start=1):
        for k in ["opportunity_id","opportunity_title","team_type","members","rationale","confidence"]:
            if k not in t:
                die(f"team {i} missing key: {k}")
        if t["team_type"] not in ["pair","team"]:
            die(f"team {i} team_type must be pair or team")
        if not isinstance(t["members"], list) or len(t["members"]) < 2:
            die(f"team {i} members must be a list with at least 2")
        if t["team_type"] == "pair" and len(t["members"]) != 2:
            die(f"team {i} is pair but has {len(t['members'])} members")
        if t["team_type"] == "team" and len(t["members"]) < 3:
            die(f"team {i} is team but has {len(t['members'])} members")
        c = t["confidence"]
        if not isinstance(c, (int,float)) or not (0 <= c <= 1):
            die(f"team {i} confidence must be between 0 and 1")

    print(f"OK: validated {len(teams)} team entries")

if __name__ == "__main__":
    main()
