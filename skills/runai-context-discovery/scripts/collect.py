#!/usr/bin/env python3
"""Optional live kubectl reader for explicitly named pods/nodes; never called offline."""
import argparse
from datetime import datetime, timezone
import json
import os
import re
import selectors
import subprocess
import time

FIELDS = {'pod': {'phase': '.status.phase'}, 'node': {'kubernetes_version': '.status.nodeInfo.kubeletVersion', 'container_runtime': '.status.nodeInfo.containerRuntimeVersion', 'allocatable_nvidia_gpu': '.status.allocatable.nvidia\\.com/gpu'}}


def commands(context, namespace, pods, nodes):
    if not context or context.startswith('-') or len(context)>256 or any(ord(c)<32 for c in context):
        raise ValueError('explicit context required')
    for value in [namespace, *pods, *nodes]:
        if not re.fullmatch(r'[a-z0-9](?:[a-z0-9.-]{0,251}[a-z0-9])?', value): raise ValueError('invalid target identifier')
    if not pods and not nodes: raise ValueError('at least one named target required')
    if len(pods) + len(nodes) > 20: raise ValueError('at most twenty targets per collection')
    result=[]
    for kind, names in (('pod',pods),('node',nodes)):
        for name in names:
            for field, path in FIELDS[kind].items():
                command=['kubectl','--context='+context,'--request-timeout=15s','get',kind,name]
                if kind=='pod': command.append('--namespace='+namespace)
                command.append('--output=jsonpath={'+path+'}')
                result.append((kind+'/'+name+'/'+field,command))
    return result


def run(command):
    # POSIX selectors bound both streams before accumulating output; no shell.
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        output={process.stdout:bytearray(),process.stderr:bytearray()}
        selector=selectors.DefaultSelector()
        for stream in output: selector.register(stream,selectors.EVENT_READ)
        deadline=time.monotonic()+20
        try:
            while selector.get_map():
                if time.monotonic()>deadline: raise subprocess.TimeoutExpired(command,20)
                for key,_ in selector.select(timeout=min(0.25,max(0,deadline-time.monotonic()))):
                    chunk=os.read(key.fileobj.fileno(),1024)
                    if not chunk: selector.unregister(key.fileobj);continue
                    output[key.fileobj].extend(chunk)
                    if sum(map(len,output.values()))>8192: raise ValueError('bounded output exceeded')
            code=process.wait(timeout=max(0.01,deadline-time.monotonic()))
            return code,output[process.stdout].decode(errors='replace'),output[process.stderr].decode(errors='replace')
        finally:
            selector.close()
            if process.poll() is None: process.kill();process.wait()


def collect(context, namespace, pods, nodes):
    evidence=[]
    for field,command in commands(context,namespace,pods,nodes):
        try:
            code,out,err=run(command)
            state='observed' if code==0 and out else 'missing'
            if code:
                state='permission-denied' if 'forbidden' in err.lower() or 'unauthorized' in err.lower() else 'unavailable'
            # Only these narrowly projected scalar values are retained, never stderr.
            value=out.strip() if state=='observed' and re.fullmatch(r'[a-zA-Z0-9._:+/\-]{1,256}',out.strip()) else None
            if state=='observed' and value is None: state='invalid-output'
        except FileNotFoundError: state,value='unavailable',None
        except subprocess.TimeoutExpired: state,value='timeout',None
        except (ValueError,OSError): state,value='invalid-output',None
        evidence.append({'field':field,'state':state,'value':value})
    return {'adapter':'kubectl named resource JSONPath scalar projection; not a Run:ai API adapter',
            'captured_at':datetime.now(timezone.utc).isoformat(),'context':context,'namespace':namespace,
            'partial':any(x['state']!='observed' for x in evidence),'evidence':evidence}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--context',required=True);parser.add_argument('--namespace',required=True)
    parser.add_argument('--pod',action='append',default=[]);parser.add_argument('--node',action='append',default=[])
    args=parser.parse_args()
    try:print(json.dumps(collect(args.context,args.namespace,args.pod,args.node),indent=2,sort_keys=True))
    except ValueError:parser.exit(2,'Invalid explicit targets; no input values echoed.\n')

if __name__=='__main__':main()
