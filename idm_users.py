# Red Hat IDM user extract attributes v0.1
# Author: Andre Facina
# This python script will extract all users attributes from the Red Hat IDM (FreeIPA)
# Tested in Red Hat Identity Management version: 4.10.1

import csv
import ldap3

# Connection settings
# Put the IDM connection and credential here
server_uri = 'ldap://1.1.1.1'
bind_dn = 'cn=Directory Manager' 
bind_password = 'changeme'

base_dn = 'dc=example,dc=redhat,dc=com'
search_filter = '(objectClass=person)'
attributes = [
    'uid', 'givenName', 'sn', 'cn', 'homeDirectory', 'gecos', 'loginShell',
    'krbPrincipalName', 'mail', 'uidNumber', 'gidNumber', 'userPassword', 'memberOf'
] 

#Connection
server = ldap3.Server(server_uri)
connection = ldap3.Connection(server, user=bind_dn, password=bind_password)

if not connection.bind():
    print("Failed to bind to the server:", connection.result)
else:
    print("Connected to the server")

    connection.search(base_dn, search_filter, attributes=attributes)

    if connection.response:
        print("Found", len(connection.response), "users:")
        
        # Open a CSV file for writing
        with open('users.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            header = [
                'User login', 'First name', 'Last name', 'Full name', 'Display name', 'Initials',
                'Home directory', 'GECOS', 'Login shell', 'Principal name', 'Email address',
                'UID', 'GID', 'Password', 'Member of groups'
            ]
            csv_writer.writerow(header)
            
            for entry in connection.response:
                user_attributes = entry['attributes']
                user_login = user_attributes.get('uid', ['N/A'])[0]
                first_name = user_attributes.get('givenName', ['N/A'])
                last_name = user_attributes.get('sn', ['N/A'])
                full_name = f"{first_name[0]} {last_name[0]}" if first_name and last_name else 'N/A'
                display_name = full_name
                initials = f"{first_name[0]}{last_name[0]}" if first_name and last_name else 'N/A'
                home_directory = user_attributes.get('homeDirectory', ['N/A'])[0]
                gecos = user_attributes.get('gecos', ['N/A'])[0]
                login_shell = user_attributes.get('loginShell', ['N/A'])[0]
                principal_name = user_attributes.get('krbPrincipalName', ['N/A'])[0]
                email_list = user_attributes.get('mail', ['N/A'])
                email = email_list[0] if email_list else 'N/A'
                uid = str(user_attributes.get('uidNumber', ['N/A']))
                gid = str(user_attributes.get('gidNumber', ['N/A']))
                #password = user_attributes.get('userPassword', ['False'])[0]
                # This attribute will extract the user password in hash format, not recommended in production.
                member_of_groups = ', '.join(user_attributes.get('memberOf', ['N/A']))
                
                # Write user attributes to CSV file, if want user hashes add the password attribute also
                csv_writer.writerow([
                    user_login, first_name[0] if first_name else 'N/A',
                    last_name[0] if last_name else 'N/A', full_name, display_name, initials,
                    home_directory, gecos, login_shell, principal_name, email,
                    uid, gid, member_of_groups
                ])
                
                print("User Login:", user_login)
                print("First name:", first_name[0] if first_name else 'N/A')
                print("Last name:", last_name[0] if last_name else 'N/A')
                print("Full name:", full_name)
                print("Display name:", display_name)
                print("Initials:", initials)
                print("Home directory:", home_directory)
                print("GECOS:", gecos)
                print("Login shell:", login_shell)
                print("Principal name:", principal_name)
                print("Email address:", email)
                print("UID:", uid)
                print("GID:", gid)
                #print("Password:", password)
                print("Member of groups:", member_of_groups)
                print("-" * 20)
        
        print("User attributes written to users.csv")
    else:
        print("No users found")

    connection.unbind()

