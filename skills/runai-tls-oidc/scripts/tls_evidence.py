#!/usr/bin/env python3
"""Compare supplied host/application TLS evidence; never opens a connection."""
def analyze(data):
    for key in ('administrator_tls_verified','application_tls_verified'):
        if data.get(key) is not None and type(data[key]) is not bool: raise ValueError('TLS evidence must be boolean or null')
    app = data.get('application_tls_verified')
    return {'state': 'application_tls_verified' if app is True else 'application_trust_unverified',
            'administrator_tls_verified': data.get('administrator_tls_verified'),
            'uncertainty': 'Host TLS success does not establish application trust or OIDC userinfo authorization.',
            'next_action': 'Inspect the served chain, SNI/hostname, application CA bundle and issuer/userinfo configuration. Container access requires separate scope.'}

import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    args = parser.parse_args()
    try:
        path = Path(args.input)
        if path.stat().st_size > 2_000_000: raise ValueError('input too large')
        result = analyze(json.loads(path.read_text()))
        print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    except (ValueError, KeyError, TypeError, OSError):
        parser.exit(2, 'Invalid or incomplete offline input; no input values echoed.\n')

if __name__ == '__main__': main()
