#!/usr/bin/env python3
import argparse, json, pathlib

def load_json(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dept", required=True)
    ap.add_argument("--faculty", default="data/faculty_index.json")
    ap.add_argument("--opps", default="data/opportunities.json")
    ap.add_argument("--max_opps", type=int, default=25)
    ap.add_argument("--max_faculty", type=int, default=60)
    args = ap.parse_args()

    faculty = load_json(args.faculty)[:args.max_faculty]
    opps = load_json(args.opps)[:args.max_opps]

    print(f"""You are helping form collaborative grant teams for {args.dept}.
Use the faculty roster and the Grants.gov opportunities below.

Task
For each opportunity, propose:
- up to 5 strong PAIRS (exactly 2 faculty)
- up to 5 strong TEAMS (3 to 5 faculty)

Constraints
- Keep teams realistic: avoid reusing the same people everywhere unless justified.
- Use complementary expertise.
- Provide a short, specific rationale tied to the opportunity.
- Output MUST be valid JSON only. No commentary.

Output schema
{{
  "department": "{args.dept}",
  "generated_from": "faculty_index.json and opportunities.json",
  "teams": [
    {{
      "opportunity_id": 123,
      "opportunity_title": "…",
      "opportunity_number": "…",
      "team_type": "pair" or "team",
      "members": ["Faculty A", "Faculty B", "..."],
      "rationale": "2 to 4 sentences",
      "suggested_specific_aim": "1 to 2 sentences",
      "next_steps": ["…","…","…"],
      "confidence": 0.0
    }}
  ]
}}

Faculty roster (JSON)
{json.dumps(faculty, indent=2)}

Opportunities (JSON)
{json.dumps(opps, indent=2)}
""")

if __name__ == "__main__":
    main()
