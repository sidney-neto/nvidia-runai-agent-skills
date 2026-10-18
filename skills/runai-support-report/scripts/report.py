#!/usr/bin/env python3
"""Redact an allowlisted incident record before emitting a local JSON report."""
import argparse
import json
import re
from pathlib import Path

SECRET_KEY = re.compile(r'token|password|passwd|secret|credential|private.?key|authorization|kubeconfig|client.?key|api.?key', re.I)
FIELDS = {'scope','captured_at','versions','findings','evidence','hypotheses','attempted_actions','remaining_questions'}


def redact(value):
    if isinstance(value, dict):
        return {str(k): '[REDACTED]' if SECRET_KEY.search(str(k)) else redact(v) for k,v in value.items()}
    if isinstance(value, list): return [redact(v) for v in value]
    if not isinstance(value, str): return value
    value = re.sub(r'-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----', '[REDACTED PRIVATE KEY]', value, flags=re.S)
    value = re.sub(r'(?i)(authorization[\"\x27]?\s*[:=]\s*)[^\r\n,;]+', r'\1[REDACTED]', value)
    value = re.sub(r'''(?i)(["']?(?:token|password|passwd|secret|api[_-]?key|client_secret)["']?\s*[:=]\s*)(["'])(?:\\.|(?!\2)[^\\])*\2''', r'\1"[REDACTED]"', value)
    value = re.sub(r'(?i)\bBearer\s+[^\s,;"\']+', 'Bearer [REDACTED]', value)
    value = re.sub(r'(?i)((?:token|password|passwd|secret|api[_-]?key|authorization|client_secret)\s*[=:]\s*)[^\s&,;"\']+', r'\1[REDACTED]', value)
    value = re.sub(r'(https?://)[^/\s@]+@', r'\1[REDACTED]@', value)
    value = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[REDACTED IP]', value)
    value = re.sub(r'\b[\w.-]+\.(?:internal|local|corp)\b', '[REDACTED HOST]', value)
    return value


def generate(data):
    if not isinstance(data, dict) or not {'scope','captured_at','findings'} <= data.keys():
        raise ValueError('incident requires scope, captured_at, findings')
    if data.keys() - FIELDS: raise ValueError('unexpected report fields; minimize input')
    result = redact(data)
    result['review_required'] = 'Inspect for organization-specific identifiers and unrecognized secrets before sharing; heuristic redaction is not complete.'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('input')
    args = parser.parse_args()
    try:
        path = Path(args.input)
        if path.stat().st_size > 2_000_000: raise ValueError('input too large')
        print(json.dumps(generate(json.loads(path.read_text())), indent=2, sort_keys=True, allow_nan=False))
    except (ValueError, TypeError, OSError): parser.exit(2, 'Invalid incident input; no input values echoed.\n')

if __name__ == '__main__': main()
