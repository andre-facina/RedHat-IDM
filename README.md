# RedHat-IDM

#### redhat_idm_users.py 

The script **redhat_idm_users.py** will retrieve comprehensive user information from Red Hat IDM and subsequently generate a **users_your_domain.csv** file.

Usage: **python3 redhat_idm_users.py --server IDM_IP_OR_HOSTNAME --bind_dn "cn=Directory Manager" --base_dn "dc=your_domain,dc=your_domain,dc=com"**




#### idm_groups.py

The **idm_groups.py** script will extract both group information and their corresponding members from Red Hat IDM. It will then compile this data into an organized groups.xlsx file, where each sheet will representa group along with its respective members.

Usage: **python3 idm_groups.py  --server IDM_IP_OR_HOSTNAME --bind_dn "cn=Directory Manager"**





The **Directory Manager** user is the default user in the IDM 
