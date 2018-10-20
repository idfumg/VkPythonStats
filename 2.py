#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vk
import json
import time

SEARCH_FIELDS = ('city', 'home_town', 'bdate')
GROUP_NAME='team'
MAX_MEMBERS_PER_REQUEST=1000
JSON_FILE_NAME='vk_data.json'

def GetApi():
    '''
    That function creates an api which used for a communication with the vk servers.
    '''

    token = '501ee987501ee987501ee98776502ea9305501e501ee9870bd564d62705fe5a0b5f73ba'
    version='5.87'

    session = vk.Session(access_token=token)
    api = vk.API(session, v=version, lang='en', timeout=10)

    return api

def GetGroupMembersCount(api):
    '''
    That function sends a requests to the vk to get group information and
    fetch members count only.
    '''

    return api.groups.getById(
        group_id=GROUP_NAME, fields='members_count')[0]['members_count']

def GetGroupMembers(api, groupName, offset, count):
    '''
    That function fetches all group members with the predefined params.
    '''

    return api.groups.getMembers(
        group_id=groupName,
        offset=offset,
        count=count,
        fields=','.join(SEARCH_FIELDS))

# def FilterMembers(members):
#     result = []
#     for member in members:
#         if all(key in member for key in SEARCH_FIELDS):
#             result.append(member)
#     return result

def CalculateTotalRequestsCount(api):
    '''
    That function tries to calculate total count of requests to the vk.
    Each request can get 1000 users only. It's a vk limitation.
    We use +1 for a situation when we have some remainder of the last chunk of users.
    '''
    totalMembers = GetGroupMembersCount(api)
    return int(totalMembers / MAX_MEMBERS_PER_REQUEST + 1)

def GetMembers(api):
    '''
    That function gets all members of the group
    '''

    result = []

    #    totalRequests = CalculateTotalRequestsCount(api)

    for count in range(0, 3):
        members = GetGroupMembers(api,
                                  groupName=GROUP_NAME,
                                  offset=count*MAX_MEMBERS_PER_REQUEST,
                                  count=5)['items']
        [result.append(member) for member in members]
        time.sleep(1)

    return result

def main():
    '''
    That function:
    1. Get an api for sending requests to the vk.
    2. Calculate how much requests we must done to get members.
    3. Fetch max members per request for the all members in the current group.
    4. At the end we save the received data in the file.
    5. Program returns a current offset.
    '''

    api = GetApi()

    members = GetMembers(api)

    with open(JSON_FILE_NAME, 'a') as outputFile:
        json.dump(members, outputFile)

    with open(JSON_FILE_NAME, 'r') as inputFile:
        members = json.load(inputFile)
        print('We load `{}` members'.format(len(members)))

if __name__ == '__main__':
    main()
