# -*- coding: utf-8 -*-
import sys, json
from google.oauth2 import service_account
import google.auth.transport.requests as gtr
import requests

KEY = sys.argv[1]
ACTION = sys.argv[2]
SITE = sys.argv[3] if len(sys.argv) > 3 else "https://giogas-pm.github.io/bodas/"
SCOPES = ["https://www.googleapis.com/auth/siteverification",
          "https://www.googleapis.com/auth/webmasters"]

creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
creds.refresh(gtr.Request())
H = {"Authorization": "Bearer " + creds.token, "Content-Type": "application/json"}

def show(r):
    print("HTTP", r.status_code)
    print(r.text[:1500])
    return r

if ACTION == "gettoken":
    body = {"verificationMethod": "FILE",
            "site": {"type": "SITE", "identifier": SITE}}
    show(requests.post("https://www.googleapis.com/siteVerification/v1/token",
                       headers=H, data=json.dumps(body)))

elif ACTION == "verify":
    body = {"site": {"type": "SITE", "identifier": SITE}}
    show(requests.post("https://www.googleapis.com/siteVerification/v1/webResource?verificationMethod=FILE",
                       headers=H, data=json.dumps(body)))

elif ACTION == "listverified":
    show(requests.get("https://www.googleapis.com/siteVerification/v1/webResource", headers=H))

elif ACTION == "addsite":
    import urllib.parse
    enc = urllib.parse.quote(SITE, safe="")
    show(requests.put("https://www.googleapis.com/webmasters/v3/sites/" + enc, headers=H))

elif ACTION == "listsites":
    show(requests.get("https://www.googleapis.com/webmasters/v3/sites", headers=H))

elif ACTION == "submitsitemap":
    import urllib.parse
    enc = urllib.parse.quote(SITE, safe="")
    sm = urllib.parse.quote(SITE + "sitemap.xml", safe="")
    show(requests.put("https://www.googleapis.com/webmasters/v3/sites/%s/sitemaps/%s" % (enc, sm), headers=H))

elif ACTION == "listsitemaps":
    import urllib.parse
    enc = urllib.parse.quote(SITE, safe="")
    show(requests.get("https://www.googleapis.com/webmasters/v3/sites/%s/sitemaps" % enc, headers=H))

elif ACTION == "adduser":
    # adiciona ggasparin53@gmail.com como owner delegado (para ver/gerir no painel do GSC)
    import urllib.parse
    rid = urllib.parse.quote(SITE, safe="")
    cur = requests.get("https://www.googleapis.com/siteVerification/v1/webResource/" + rid, headers=H).json()
    owners = set(cur.get("owners", []))
    owners.add("ggasparin53@gmail.com")
    body = {"id": cur.get("id"),
            "site": cur.get("site"),
            "owners": sorted(owners)}
    show(requests.put("https://www.googleapis.com/siteVerification/v1/webResource/" + rid,
                      headers=H, data=json.dumps(body)))

elif ACTION == "query":
    # impressões/cliques dos últimos 28 dias por página
    import urllib.parse, datetime
    enc = urllib.parse.quote(SITE, safe="")
    end = datetime.date.today(); start = end - datetime.timedelta(days=28)
    body = {"startDate": str(start), "endDate": str(end), "dimensions": ["page"], "rowLimit": 50}
    show(requests.post("https://www.googleapis.com/webmasters/v3/sites/%s/searchAnalytics/query" % enc, headers=H, data=json.dumps(body)))

elif ACTION == "inspect":
    url = sys.argv[4]
    r = requests.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect", headers=H,
                      data=json.dumps({"inspectionUrl": url, "siteUrl": SITE}))
    try:
        ix = r.json()["inspectionResult"]["indexStatusResult"]
        print(url.split(".io")[1], "|", ix.get("coverageState"), "| rastreado:", ix.get("lastCrawlTime", "nunca"))
    except Exception:
        show(r)
