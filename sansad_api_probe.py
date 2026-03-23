
import json
import sys
import time
import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://sansad.in/",
}

KEYWORD = "damodar"

LS_CANDIDATES = [
    ("https://sansad.in/api/ls/questions",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5, "searchIn": "1",
      "sortBy": "debateDate", "sortOrder": "desc"}),

    ("https://sansad.in/getServiceData",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5, "searchIn": "1",
      "house": "ls"}),

    ("https://sansad.in/api/questions/ls",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5}),

    ("https://sansad.in/ls/api/questions",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5}),

    # Some parliament sites use query-string only without path
    ("https://sansad.in/api/ls/facetSearch",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5, "searchIn": "1"}),

    ("https://sansad.in/api/ls/questions/facetSearch",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5, "searchIn": "1"}),

    ("https://sansad.in/api/ls/questionanswers",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5}),
]

RS_CANDIDATES = [
    ("https://sansad.in/api/rs/questions",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5, "searchIn": "1",
      "sortBy": "keywordCount", "sortOrder": "desc"}),

    ("https://sansad.in/api/questions/rs",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5}),

    ("https://sansad.in/rs/api/questions",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5}),

    ("https://sansad.in/api/rs/facetSearch",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5, "searchIn": "1"}),

    ("https://sansad.in/api/rs/questions/facetSearch",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5, "searchIn": "1"}),

    ("https://sansad.in/api/rs/questionanswers",
     {"keyword": KEYWORD, "pageNo": 1, "pageSize": 5}),
]


def probe(session: requests.Session, label: str, candidates: list) -> dict | None:
    print(f"\n{'='*60}")
    print(f"  Probing {label}")
    print(f"{'='*60}")
    for url, params in candidates:
        try:
            r = session.get(url, params=params, headers=HEADERS, timeout=15)
            ct = r.headers.get("Content-Type", "")
            print(f"\n  URL   : {r.url}")
            print(f"  Status: {r.status_code}  Content-Type: {ct}")

            if r.status_code == 200 and "json" in ct:
                data = r.json()
                print(f"  ✅ JSON HIT! Top-level keys: {list(data.keys())}")
                # Find records list
                for k in ("questions", "lstQuestion", "data", "results",
                          "records", "items", "content"):
                    if data.get(k) and isinstance(data[k], list) and data[k]:
                        rec = data[k][0]
                        print(f"  First record ({k}[0]) keys: {list(rec.keys())}")
                        print(f"\n  --- Raw JSON (first 3000 chars) ---")
                        print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
                        return {"url": url, "params": params, "data": data}
                # No known list key found — still print
                print(f"  ⚠️  JSON received but no recognised list key found.")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
                return {"url": url, "params": params, "data": data}

            elif r.status_code == 200:
                print(f"  Status 200 but not JSON. Body (200 chars): {r.text[:200]}")
            else:
                print(f"  ✗ HTTP {r.status_code}")

        except requests.RequestException as exc:
            print(f"  ✗ Error: {exc}")

        time.sleep(0.5)

    print(f"\n  ❌ No working endpoint found for {label}.")
    return None


def main():
    session = requests.Session()
    print(f"Probing sansad.in API endpoints for keyword='{KEYWORD}'…\n")

    ls_result = probe(session, "Lok Sabha (LS)", LS_CANDIDATES)
    rs_result = probe(session, "Rajya Sabha (RS)", RS_CANDIDATES)

    print("\n\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    if ls_result:
        print(f"✅  LS API : {ls_result['url']}")
    else:
        print("❌  LS API : not found automatically")

    if rs_result:
        print(f"✅  RS API : {rs_result['url']}")
    else:
        print("❌  RS API : not found automatically")


    # Write report
    report = {
        "ls": ls_result if ls_result else "not_found",
        "rs": rs_result if rs_result else "not_found",
    }
    with open("api_probe_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    print("\nFull probe report saved to: api_probe_report.json")


if __name__ == "__main__":
    main()
