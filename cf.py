#!/usr/bin/env python3

import json
import os
import subprocess
import sys

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

child = subprocess.run(['cargo', 'metadata'], capture_output=True)
metadata = json.loads(child.stdout)

member_ids = metadata['workspace_members']

members = []
for pkg in metadata['packages']:
    if pkg['id'] in member_ids:
        members.append(pkg['name'])

pkgs = {}

for pkg in metadata['packages']:
    pkgs[pkg['name']] = pkg

features = {}

for member_name in members:
    feats = {}
    member = pkgs[member_name]

    for dep in member['dependencies']:
        name = dep['name']
        feats[name] = dep['features']
        if dep['uses_default_features']:
            feats[name] += pkgs[dep['name']]['features'].get('default', [])

    features[member_name] = feats

print(json.dumps(features, indent=4))
