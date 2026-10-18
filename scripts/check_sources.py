#!/usr/bin/env python3
"""Opt-in public-source freshness report. Never updates reviewed source records."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import hashlib
import json
from pathlib import Path
import urllib.request
from urllib.parse import urlparse

HOSTS={'prometheus.io','docs.nvidia.com','run-ai-docs.nvidia.com','github.com','raw.githubusercontent.com','agentskills.io','developers.openai.com','learn.chatgpt.com','kubernetes.io','docs.vllm.ai','docs.openssl.org','v1-34.docs.kubernetes.io','v1-35.docs.kubernetes.io'}

def validate_url(url):
    parts=urlparse(url)
    if parts.scheme!='https' or parts.hostname not in HOSTS or parts.username or parts.password or parts.port not in (None,443):
        raise ValueError('source must be an allowlisted public HTTPS URL without credentials')

class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        validate_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def fetch(record):
    try:
        validate_url(record['url'])
        request=urllib.request.Request(record['url'],headers={'User-Agent':'runai-skills-source-review/0.1'})
        with urllib.request.build_opener(Redirects).open(request,timeout=15) as response:
            body=response.read(6_000_001)
            if len(body)>6_000_000:raise ValueError('source exceeds bound')
            return {'status':'available','resolved_url':response.url,'sha256':hashlib.sha256(body).hexdigest()}
    except (OSError,ValueError):return {'status':'unavailable'}

def assess(record,observed,today,max_age):
    states=[]
    if observed['status']=='unavailable':states.append('unavailable')
    else:
        if observed.get('resolved_url')!=record.get('resolved_url'):states.append('redirected')
        if not record.get('sha256'):states.append('no-baseline')
        elif observed.get('sha256')!=record['sha256']:states.append('changed')
    if not record.get('reviewed_at') or (today-date.fromisoformat(record['reviewed_at'])).days>max_age:states.append('aging')
    return {'id':record['id'],'states':states or ['unchanged'],'reviewed_evidence':record,
            'observed':observed,'checked_at':today.isoformat(),'validation_required':bool(states)}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('ledger');parser.add_argument('--max-age-days',type=int,default=90)
    args=parser.parse_args()
    records=json.loads(Path(args.ledger).read_text())['sources']
    with ThreadPoolExecutor(max_workers=4) as pool:observations=list(pool.map(fetch,records))
    report=[assess(record,observed,date.today(),args.max_age_days) for record,observed in zip(records,observations)]
    print(json.dumps({'sources':report,'note':'No compatibility rules or reviewed evidence were changed. HTML/build hashes may change without semantic changes; human review is required.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
