import json
import os
import sys
import urllib.parse
import urllib.request

TOKEN = os.environ.get("APIFY_TOKEN")
if not TOKEN:
    print("set APIFY_TOKEN env")
    sys.exit(1)

HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def get(path):
    req = urllib.request.Request(f"https://api.apify.com{path}", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


queries = ["oece proveedor", "oece personeria", "sunat ruc representante", "sunat ruc socios", "oece proveedor ruc"]
seen = set()
hits = []
for q in queries:
    qs = urllib.parse.urlencode({"search": q, "limit": 20})
    try:
        data = get(f"/v2/actors?{qs}")
        if not hits:
            print("RAW keys:", list(data.keys()) if isinstance(data, dict) else type(data))
            print("RAW data:", json.dumps(data)[:1200])
    except Exception as e:
        print("err", q, e)
        continue
    for a in data.get("data", []):
        key = a.get("id") or a.get("actorId") or a.get("name")
        if not key or key in seen:
            continue
        seen.add(key)
        title = (a.get("title") or a.get("name") or "").strip()
        desc = (a.get("description") or "").strip().replace("\n", " ")[:160]
        hits.append({"title": title, "id": a.get("id"), "username": a.get("username"), "desc": desc})

print("actors encontrados:", len(hits))
for h in hits:
    print(f"- {h['title']}  ({h['username']}/{h['id']})")
    print(f"    {h['desc']}")
