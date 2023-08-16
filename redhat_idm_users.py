# This script extracts all attributes of the users from Red Hat Identity Manager and then write this information into a CSV file named "users.csv". This CSV file contains rows where each row represents an user and each column represents an attribute of that user.
# Tested in Red Hat Identity Management version: 4.10.1
# Author: Andre Facina
# Usage: python3 redhat_idm_users.py --server IDM_IP_OR_HOSTNAME --bind_dn "cn=Directory Manager" --base_dn "dc=your_domain,dc=your_domain,dc=com"

import csv
import ldap3
import argparse
import getpass
import re

def main():
    parser = argparse.ArgumentParser(description="Red Hat Identity Manager user extract info to csv")
    parser.add_argument("--server", required=True, help="IDM Server IP or Hostname")
    parser.add_argument("--bind_dn", required=True, help="Bind DN, Example: cn=Directory Manager")
    parser.add_argument("--bind_password", help="Bind password. You can omit it and avoid clear text password")
    parser.add_argument("--base_dn", help="Base DN, Example: dc=example,dc=redhat,dc=com")

    args = parser.parse_args()

    if not args.bind_password:
        args.bind_password = getpass.getpass("Enter bind password: ")

    # Connection settings
    server = args.server
    bind_dn = args.bind_dn
    base_dn = args.base_dn
    bind_password = args.bind_password

    # Get the domain from the base_dn
    get_domain = re.findall(r"dc=([^,]+)", base_dn)
    domain = "_".join(get_domain)

    #print(domain)

    #base_dn = 'dc=example,dc=redhat,dc=com'
    search_filter = '(objectClass=person)'
    attributes = [
        'uid', 'givenName', 'sn', 'cn', 'ipaUniqueID', 'dn', 'homeDirectory', 'gecos', 'loginShell',
        'krbPrincipalName', 'mail', 'uidNumber', 'gidNumber', 'memberOf', 'ipaNTSecurityIdentifier'  #'userPassword'
    ]

    # Connection
    server = ldap3.Server(server)
    connection = ldap3.Connection(server, user=bind_dn, password=bind_password)

    if not connection.bind():
        print("Failed to bind to the server:", connection.result)
    else:
        print("Connected to the server")

        connection.search(base_dn, search_filter, attributes=attributes)

        if connection.response:
            print("Found", len(connection.response), "users:")
            
            # Open a CSV file for writing
            with open(f'users_{domain}.csv', 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                
                header = [
                    'User login', 'First name', 'Last name', 'Full name', 'dn', 'ipaUniqueID',
                    'Home directory', 'Login shell', 'Principal name', 'Email address',
                    'UID', 'GID', 'ipaNTSecurityIdentifier', 'Member of groups'
                ]
                csv_writer.writerow(header)
                
                # Extract the user's info 
                for entry in connection.response:
                    user_attributes = entry['attributes']
                    user_login = user_attributes.get('uid', ['N/A'])[0]
                    first_name = user_attributes.get('givenName', ['N/A'])
                    last_name = user_attributes.get('sn', ['N/A'])
                    full_name = f"{first_name[0]} {last_name[0]}" if first_name and last_name else 'N/A'
                    #full_name = user_attributes.get('displayName')
                    dn = user_attributes.get('dn')
                    ipaUniqueID = user_attributes.get('ipaUniqueID')[0]
                    display_name = full_name
                    #initials = f"{first_name[0]}{last_name[0]}" if first_name and last_name else 'N/A'
                    home_directory = user_attributes.get('homeDirectory') #, ['N/A'])[1]
                    login_shell = user_attributes.get('loginShell') #, ['N/A'])[1]
                    principal_name = user_attributes.get('krbPrincipalName', ['N/A'])[0]
                    email_list = user_attributes.get('mail', ['N/A'])
                    email = email_list[0] if email_list else 'N/A'
                    uid = str(user_attributes.get('uidNumber', ['N/A']))
                    gid = str(user_attributes.get('gidNumber', ['N/A']))
                    ipaNTSecurityIdentifier =  user_attributes.get('ipaNTSecurityIdentifier')
                    #password = user_attributes.get('userPassword') #, ['False'])[0] # The user's hashes
                    member_of_groups = ', '.join(user_attributes.get('memberOf', ['N/A']))
                    
                    # Write user attributes to CSV file
                    csv_writer.writerow([
                        user_login, first_name[0] if first_name else 'N/A',
                        last_name[0] if last_name else 'N/A', full_name, dn, ipaUniqueID,
                        home_directory, login_shell, principal_name, email,
                        uid, gid, ipaNTSecurityIdentifier,  member_of_groups
                    ])
                    
                    print("User Login:", user_login)
                    print("First name:", first_name[0] if first_name else 'N/A')
                    print("Last name:", last_name[0] if last_name else 'N/A')
                    print("Full name:", full_name)
                    #print("Display name:", display_name)
                    print("Distinguished Name:", dn)
                    print("ipaUniqueID:", ipaUniqueID)
                    print("Home directory:", home_directory)
                    print("Login shell:", login_shell)
                    print("Principal name:", principal_name)
                    print("Email address:", email)
                    print("UID:", uid)
                    print("GID:", gid)
                    #print("Password:", password)
                    print("ipaNTSecurityIdentifier:", ipaNTSecurityIdentifier)
                    print("Member of groups:", member_of_groups)
                    print("-" * 20)
            
            print("User attributes written to users_" + str(domain) + ".csv")
        else:
            print("No users found")

        connection.unbind()

if __name__ == "__main__":
    main()

