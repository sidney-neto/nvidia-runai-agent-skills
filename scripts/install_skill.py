#!/usr/bin/env python3
"""Copy one complete skill into an explicitly chosen discovery directory; no overwrite."""
import argparse
from pathlib import Path
import shutil

def install(name,destination):
    root=Path(__file__).resolve().parents[1]/'skills'
    if name not in {p.name for p in root.iterdir() if p.is_dir()}:raise ValueError('unknown canonical skill')
    target=destination/name
    if target.exists() or target.is_symlink():raise FileExistsError('skill already exists; review changes manually')
    destination.mkdir(parents=True,exist_ok=True)
    shutil.copytree(root/name,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    return target

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('skill');parser.add_argument('--destination',type=Path,required=True)
    args=parser.parse_args()
    try:print(install(args.skill,args.destination))
    except (ValueError,FileExistsError,OSError):parser.exit(2,'Installation failed; existing skill was not replaced.\n')

if __name__=='__main__':main()
