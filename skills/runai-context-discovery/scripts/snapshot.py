#!/usr/bin/env python3
"""Validate our local snapshot contract and retain raw version provenance. Offline."""
import argparse
from datetime import datetime
import json
import re
from pathlib import Path
from jsonschema import Draft202012Validator


def version(raw):
    if raw is None or raw == '':
        return {'state': 'missing', 'parts': None}
    match = re.fullmatch(r'v?(0|[1-9]\d*)\.(0|[1-9]\d*)(?:\.(0|[1-9]\d*))?', raw)
    if match:
        return {'state': 'release', 'parts': [int(x or 0) for x in match.groups()]}
    return {'state': 'unverified', 'parts': None}


def normalize(data):
    schema = json.loads((Path(__file__).resolve().parents[1] / 'assets/snapshot.schema.json').read_text())
    errors = list(Draft202012Validator(schema).iter_errors(data))
    if errors:
        raise ValueError('invalid local snapshot; check required fields, types, bounds and unknown keys')
    timestamp = data['captured_at']
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', timestamp):
        raise ValueError('timestamp requires a date, time and timezone')
    datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    result = json.loads(json.dumps(data, allow_nan=False))
    for component in result['components']:
        parsed = version(component['raw_version'])
        component['version_state'] = parsed['state']
        component['normalized_version'] = '.'.join(map(str, parsed['parts'])) if parsed['parts'] else None
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot')
    args = parser.parse_args()
    try:
        path = Path(args.snapshot)
        if path.stat().st_size > 2_000_000:
            raise ValueError('snapshot exceeds 2 MB limit')
        print(json.dumps(normalize(json.loads(path.read_text())), indent=2, sort_keys=True, allow_nan=False))
    except (ValueError, OSError):
        parser.exit(2, 'Invalid or unreadable snapshot; no input values echoed.\n')

if __name__ == '__main__': main()
