#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This module reads all members data from file and filter them by preffered fields presence.
'''

import json

def FilterMembers(members, filterFields):
    result = []
    for member in members:
        if all(key in member for key in filterFields):
            result.append(member)
    return result

def ReadMembersFromFile(filename):
    members = []
    with open(filename, 'r') as inputFile:
        members = json.load(inputFile)
    return members

def WriteMembersToFile(filename, members):
    with open(filename, 'w') as outputFile:
        json.dump(members, outputFile, ensure_ascii=False)

def main():
    MEMBERS_FILE_NAME='vk_members.json'
    FILTERED_MEMBERS_FILE_NAME='vk_members_filtered.json'

    FILTER_FIELDS = ('city',
                     'home_town',
                     'bdate',
                     #'bdate_visibility',
                     #'sex'
    )

    members = ReadMembersFromFile(MEMBERS_FILE_NAME)
    print('We load `{}` members from `{}` file'.format(len(members),
                                                       MEMBERS_FILE_NAME))

    members = FilterMembers(members, FILTER_FIELDS)

    WriteMembersToFile(FILTERED_MEMBERS_FILE_NAME, members)
    print('We write `{}` members to `{}` file'.format(len(members),
                                                      FILTERED_MEMBERS_FILE_NAME))

if __name__ == '__main__':
    main()
