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

    d = set()
    for member in members:
        if member['id'] in d:
            print('Warning! Duplicate! {}'.format(member['id']))
            exit
        d.add(member['id'])

if __name__ == '__main__':
    main()
