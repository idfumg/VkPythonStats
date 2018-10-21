#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def ReadMembersFromFile(filename):
    members = []
    try:
        with open(filename, 'r') as inputFile:
            members = json.load(inputFile)
    except Exception as e:
        print('Unexpected exception!', e)
        pass
    return members

def main():
    members = ReadMembersFromFile('vk_members.json')

    dups = set()
    d = set()
    for member in members:
        if member['id'] in d:
            print('Warning! Duplicate! {}'.format(member['id']))
            dups.add(member['id'])
        d.add(member['id'])

    print(dups)

if __name__ == '__main__':
    main()
