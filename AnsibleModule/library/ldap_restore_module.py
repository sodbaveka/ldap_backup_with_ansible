#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Mickaël Duchet <sodbaveka@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r'''
module: ldap_restore_module
short_description: Module that restores ldap datas.
description:
- Import informations on organizational units and users from an json file.
- Push datas to backup server.
version_added: 3.0
author: Mickaël Duchet (@sodbaveka)
options:
  ldap_backup_host:
    description: backup server ip
    required: yes
  connexion_username:
    description: connexion login to ldap annuary
    required: yes
  connexion_password:
    description: connexion password
    required: yes
  choosen_action:
    description: Type 'push' to restore annuary in backup server, or 'delete' to erase data, according to json file
    required: yes
notes: null
requirements: null

'''

EXAMPLES = '''
 - name: Restoration module launched
    ldap_restore_module: 
      ldap_backup_host: "{{item}}"
      connexion_username: "{{admin_dn}}"
      connexion_password: "{{admin_password}}"
      choosen_action: 'push'
    register: result
    no_log: True
    with_items: "{{ groups['hosts'] }}"   

'''

RETURN = r'''
meta:
  description: 
  - Return 'Successful copy' if datas are correctly copied.
  - Return 'Successful erasure' if datas are correctly erased.
  - Return 'Bad option' if choosen_action is incorrectly completed.

'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.LdapRestoredAnnuary import LdapRestoredAnnuary

def main():
	module = AnsibleModule(argument_spec=dict(choosen_action=dict(required=True), ldap_backup_host=dict(required=True), connexion_username=dict(required=True),connexion_password=dict(required=True)), supports_check_mode=True)
	ldap_backup_host = module.params['ldap_backup_host']
	connexion_username = module.params['connexion_username']
	connexion_password = module.params['connexion_password']
	choosen_action = module.params['choosen_action']

	try:
	    ldap_restored_annuary = LdapRestoredAnnuary(ldap_backup_host, connexion_username, connexion_password)
	    if ldap_restored_annuary:
	    	print("User authenticated.\nWelcome {}.".format(ldap_restored_annuary.connexion.extend.standard.who_am_i()))
	    	# ldap_restored_annuary.deserialize_from_bin()
	    	ldap_restored_annuary.import_from_json()
	    	if choosen_action == 'push':
	    		ldap_restored_annuary.push_data()
	    		msg='Successful copy'
	    	elif choosen_action == 'delete':
	    		ldap_restored_annuary.delete_data()
	    		msg='Successful erasure'
	    	else:
	    		msg='Bad option'
	    	
	except ldap3.core.exceptions.LDAPBindError as login_error:
		print(str(login_error))
	except ldap3.core.exceptions.LDAPPasswordIsMandatoryError as password_error:
		print(str(password_error))

	module.exit_json(changed=False, meta=msg)
	
if __name__ == "__main__":
	main()
    
    