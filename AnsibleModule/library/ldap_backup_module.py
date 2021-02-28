#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Mickaël Duchet <sodbaveka@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
module: ldap_backup_module
short_description: Module that saves ldap datas
description:
  - Import informations on organizational units and users from an ldap directory.
  - Save informations in files of different exploitable formats (ldif, json, yml).
version_added: 3.0
author: Mickaël Duchet (@sodbaveka)
options:
  ldap_main_host:
    description: server ip
    required: yes 
  connexion_username:
    description: connexion login to ldap annuary
    required: yes
  connexion_password:
    description: connexion password
    required: yes
notes: null
requirements: null

'''

EXAMPLES = '''
- name: Backup module launched
    ldap_backup_module: 
      ldap_main_host: "{{ldap_main_host}}"
      connexion_username: "{{admin_dn}}"
      connexion_password: "{{admin_password}}"
    register: result
    no_log: True
    
'''

RETURN = r'''
meta:
  description: Return 'Success' if files are completed

'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.LdapAnnuary import LdapAnnuary

def main():
	module = AnsibleModule(argument_spec=dict(ldap_main_host=dict(required=True), connexion_username=dict(required=True),connexion_password=dict(required=True)), supports_check_mode=True)
	ldap_main_host = module.params['ldap_main_host']
	connexion_username = module.params['connexion_username']
	connexion_password = module.params['connexion_password']
	
	try:
		ldap_annuary = LdapAnnuary(ldap_main_host, connexion_username, connexion_password)
		if ldap_annuary:
			ldap_annuary.copy_to_json_file()
			ldap_annuary.copy_to_yaml_file()
			ldap_annuary.copy_to_ldif_file()
	except ldap3.core.exceptions.LDAPBindError as login_error:
		print(str(login_error))
	except ldap3.core.exceptions.LDAPPasswordIsMandatoryError as password_error:
		print(str(password_error))

	module.exit_json(changed=False, meta='Success')

if __name__ == "__main__":
	main()