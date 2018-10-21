#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
`relation` - отношения.

1 — не женат/не замужем;
2 — есть друг/есть подруга;
3 — помолвлен/помолвлена;
4 — женат/замужем;
5 — всё сложно;
6 — в активном поиске;
7 — влюблён/влюблена;
8 — в гражданском браке;
0 — не указано.

`sex` - пол.

1 — женский;
2 — мужской;
0 — пол не указан.

`city` - текущий город проживания.
`home_town` - название родного города.
`country` - страна проживания.
`bdate` - дата рождения (в разных форматах, см. bdate_visibility).

`bdate_visibility` - видимость даты рождения.

1 — показывать дату рождения;
2 — показывать только месяц и день;
0 — не показывать дату рождения.

`first_name` - имя пользователя.
`last_name` - фамилия пользователя.
`screen_name` - короткое имя пользователя (если есть).
'''

import vk
import json
import time

def GetApi():
    '''
    That function creates an api which used for a communication with the vk servers.
    '''

    token = '501ee987501ee987501ee98776502ea9305501e501ee9870bd564d62705fe5a0b5f73ba'
    version='5.87'

    session = vk.Session(access_token=token)
    api = vk.API(session, v=version, lang='ru', timeout=10)

    return api

def GetGroupMembers(api, groupName, offset, count):
    '''
    That function fetches all group members with the predefined params.
    '''

    SEARCH_FIELDS = ('city',
                     'home_town',
                     'bdate',
                     'bdate_visibility',
                     'country',
                     'sex',
                     'relation',
                     'first_name',
                     'last_name',
                     'screen_name')

    return api.groups.getMembers(
        group_id=groupName,
        offset=offset,
        count=count,
        fields=','.join(SEARCH_FIELDS))

def GetGroupMembersTotalCount(api, groupName):
    '''
    That function sends a requests to the vk to get group information and
    fetch members count only.
    '''

    return api.groups.getById(
        group_id=groupName, fields='members_count')[0]['members_count']

def CalculateTotalRequestsCount(api, maxMembersPerRequest, groupName, totalMembers):
    '''
    That function tries to calculate total count of requests to the vk.
    Each request can get 1000 users only. It's a vk limitation.
    We use +1 for a situation when we have some remainder of the last chunk of users.
    '''

    return int(totalMembers / maxMembersPerRequest + 1)

def GetMembers(api, maxMembersPerRequest, groupName):
    '''
    That function gets all members of the group by chunks of max members per request.
    It reads all members into memory, because for iteratively write into the file
    would need reading from a file, modifying JSON and writing to the file.
    We can use different format liek a CSV, but try to rely on our memory :)
    Before requesting, we calculate how much requests we must done to get members.
    '''

    result = []

    for count in range(0, 2):
        members = GetGroupMembers(api,
                                  groupName=groupName,
                                  offset=count*maxMembersPerRequest,
                                  count=5)['items']

        if len(members) == 0:
            break

        print('We partially load `{}` members'.format(len(members)))

        [result.append(member) for member in members]
        time.sleep(1)

    return result

def main():
    '''
    That function:
    Get an api for sending requests to the VK.
    Fetch members from group.
    Save members into the file.
    '''

    MAX_MEMBERS_PER_REQUEST=1000
    GROUP_NAME='team'
    JSON_FILE_NAME='vk_members.json'

    print('Creating VK API object for interacting with VK server...')
    api = GetApi()

    totalMembers = GetGroupMembersTotalCount(api, GROUP_NAME)
    print('Total group members: {}'.format(totalMembers))

    totalRequests = CalculateTotalRequestsCount(api,
                                                MAX_MEMBERS_PER_REQUEST,
                                                GROUP_NAME,
                                                totalMembers)
    print('We need `{}` requests to the VK server.'.format(totalRequests))

    print('Receive VK members from `{}` group...'.format(GROUP_NAME))
    members = GetMembers(api, MAX_MEMBERS_PER_REQUEST, GROUP_NAME)
    print('We load `{}` members'.format(len(members)))
    if len(members) == 0:
        print('Nothing to save. Exit.')
        return

    print('Save members to `{}` file...'.format(JSON_FILE_NAME))
    with open(JSON_FILE_NAME, 'w') as outputFile:
        json.dump(members, outputFile, ensure_ascii=False)

    print('Done.')

if __name__ == '__main__':
    main()
