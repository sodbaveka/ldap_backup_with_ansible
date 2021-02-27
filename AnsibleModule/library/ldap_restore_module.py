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
  description: Return 'Success' if datas are correctly processed

'''

from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, SUBTREE
import json
import pickle
import yaml
from ansible.module_utils.basic import AnsibleModule

class LdapRestoredAnnuary:
	"""
	A class to represent a LDAP annuary restored from a json file

	...

	Attributes
	----------
	server : Server object
		Definition of a Server object

	connexion : Connexion object
		Definition of a Connexion object

	uo_backup : List
		A list of 0rganizationalUnit objects

	users_backup : List
		A list of InetOrgPerson objects

	Methods
	-------
	import_from_json():
		To import datas from a json file

	deserialize_from_bin():
		To deserialize objects from a file called annuary_backup.bin

	push_data():
		To perform an Add operation to backup server

	delete_data():
		To perform an Delete operation to backup server
	"""

	def __init__(self, ldap_backup_host, connexion_username, connexion_password):
		"""
		Constructs all the necessary attributes for the LDAP restored annuary object

		...

		Attributes
		----------
		server : Server object
			Definition of a Server object

		connexion : Connexion object
			Definition of a Connexion object

		uo_backup : List
			A list of 0rganizationalUnit objects

		users_backup : List
			A list of InetOrgPerson objects
		"""

		self.server = Server(ldap_backup_host, get_info=ALL)
		self.connexion = Connection(self.server, connexion_username, connexion_password, auto_bind=True)
		self.uo_backup = []
		self.users_backup = []
		

	def import_from_json(self):
		"""To import datas from a json file"""
		try:
			with open('annuary_backup.json', 'rb') as file:
			    self.data = json.load(file)
			    for element in self.data:
			     	#self.content[element["objectClass"]].append()
			     	if element['attributes']["objectClass"] == 'organizationalUnit':
			     		uo_object = OrganizationalUnit(element)
			     		self.uo_backup.append(uo_object)
			     	elif element['attributes']["objectClass"] == 'inetOrgPerson':
			     		user_object = InetOrgPerson(element)
			     		self.users_backup.append(user_object)
			     	else:
			     		print("Importation error")
			print("Importation completed.")
		except (IOError, FileNotFoundError):
		     print('Missing file.')

	def push_data(self):
		"""To perform an Add operation to backup server""" 
		for element in self.uo_backup:
			self.connexion.add(element.dn, attributes = element.attributes)
			print("{} created!".format(element.dn))
		for element in self.users_backup:
			self.connexion.add(element.dn, attributes = element.attributes)
			print("{} created!".format(element.dn))
		print("Restoration completed.")

	def delete_data(self):
		"""To perform an Delete operation to backup server""" 
		for element in self.users_backup:
			self.connexion.delete(element.dn)
			print("{} deleted!".format(element.dn))
		for element in self.uo_backup:
			self.connexion.delete(element.dn)
			print("{} deleted!".format(element.dn))
		print("Removal completed.")

	def deserialize_from_bin(self):
		"""To deserialize objects from a file called annuary_backup.bin"""
		try:
			with open('annuary_backup.bin', 'rb') as file:
			    self.uo_backup = pickle.load(file)
			    self.users_backup = pickle.load(file)
			    print("Deserialization completed.")
			    #print(self.uo_backup, self.users_backup, sep='\n')
		except (IOError, pickle.UnpicklingError):
			print('Reading error.')



class OrganizationalUnit:
	"""
	A class to represent a LDAP Organizational Unit

	...

	Attributes
	----------
	dn : str
		Distinguished Name

	attributes : dict
		Dictionary of attributes

	objectClass : str
		Object class

	ou : str
		Organizational unit's name

	description : str
		A description of organizational unit

	Methods
	-------
	__str__(): 
		Redefinition of method __str__()
	"""

	def __init__(self, uo_dict):
		"""
		Constructs all the necessary attributes for the LDAP Organizational Unit object

		...

		Attributes
		----------
		dn : str
			Distinguished Name

		attributes : dict
			Dictionary of attributes

		objectClass : str
			Object class

		ou : str
			Organizational unit's name

		description : str
			A description of organizational unit

		"""

		
		self.dn = uo_dict['dn']
		self.attributes = uo_dict['attributes']
		self.objectClass = uo_dict['attributes']['objectClass'][0]
		self.ou = uo_dict['attributes']['ou'][0]
		self.description = uo_dict['attributes']['description'][0]

	def __str__(self):
		"""Redefinition of method __str__"""
		return "dn: {}\nobjectClass: {}\nou: {}\ndescription: {}\n".format(self.dn, self.objectClass, self.ou, self.description)



class InetOrgPerson:
	"""
	A class to represent a LDAP user (type InetOrgPerson)

	...

	Attributes
	----------
	dn : str
		Distinguished Name

	attributes : dict
		Dictionary of attributes

	objectClass : str
		Object class

	givenName : str
		Given name

	sn : str
		Surname

	cn : str
		Common name

	uid : str
		User ID

	userPassword : str
		User password

	Methods
	-------
	__str__():
		Redefinition of method __str__()
	"""

	def __init__(self, uo_dict):
		"""
		Constructs all the necessary attributes for the LDAP Organizational Unit object

		...

		Attributes
		----------
		dn : str
			Distinguished Name

		attributes : dict
			Dictionary of attributes

		objectClass : str
			Object class

		givenName : str
			Given name

		sn : str
			Surname

		cn : str
			Common name

		uid : str
			User ID

		userPassword : str
			User password

		"""

		
		self.dn = uo_dict['dn']
		self.attributes = uo_dict['attributes']
		self.objectClass = uo_dict['attributes']['objectClass'][0]
		self.givenName = uo_dict['attributes']['givenName'][0]
		self.sn = uo_dict['attributes']['sn'][0]
		self.cn = uo_dict['attributes']['cn'][0]
		self.uid = uo_dict['attributes']['uid'][0]
		self.userPassword = uo_dict['attributes']['userPassword'][0]

	def __str__(self):
		"""Redefinition of method __str__"""
		return "dn: {}\nobjectClass: {}\ngivenName: {}\nsn: {}\ncn: {}\nuid: {}\nuserPassword: {}\n".format(self.dn, self.objectClass, self.givenName, self.sn, self.cn, self.uid, self.userPassword)



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
    
    