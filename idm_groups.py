# This script will extract both group information and their corresponding members from Red Hat IDM. It will then compile this data into an organized groups.xlsx file, where each sheet will represent a group along with its respective members.
# Author: Andre Facina
# Version 0.1
# Tested in Red Hat Identity Management version: 4.10.1

import ldap3
from openpyxl import Workbook
import re

# Connection settings, in the next version I will put it as an option
server_uri = 'ldap://1.1.1.1'
bind_dn = 'cn=Directory Manager'
bind_password = 'changeme'

base_dn = 'dc=example,dc=redhat,dc=com'
group_search_filter = '(objectClass=groupofnames)'
group_attributes = ['cn', 'member']

# Connection
server = ldap3.Server(server_uri)
connection = ldap3.Connection(server, user=bind_dn, password=bind_password)

if not connection.bind():
    print("Failed to bind to the server:", connection.result)
else:
    print("Connected to the server")

    groups = []
    connection.search(base_dn, group_search_filter, attributes=group_attributes)
    if connection.response:
        for entry in connection.response:
            groups.append(entry['attributes'])

    workbook = Workbook()

    for group in groups:
        group_name = group.get('cn', ['N/A'])[0]
        
        sanitized_group_name = re.sub(r'[\/:*?"<>|]', '_', group_name)
        
        sheet = workbook.create_sheet(sanitized_group_name)

        members = group.get('member', [])
        for index, member in enumerate(members, start=1):
            sheet.cell(row=index, column=1, value=member)

    workbook.save('groups.xlsx')

    print("Groups written to groups.xlsx")

    connection.unbind()


