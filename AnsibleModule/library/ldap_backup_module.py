#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Mickaël Duchet <sodbaveka@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
module: ldap_backup_module
short_description: Module that saves ldap datas
description: 
	- import informations on organizational units and users from an ldap directory,
	- save informations in files of different exploitable formats (ldif, json, yml).
version_added: "2.10"
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
'''

EXAMPLES = '''
- name: "Backup module launched"
    ldap_backup_module: 
      ldap_main_host: 'srv-ldap-01'
      connexion_username: 'cn=admin,dc=example,dc=com'
      connexion_password: 'p@ssword'
'''

RETURN = '''
meta:
	description: Return 'Success' if files are completed
'''

import ldap3
from ansible.module_utils.basic import AnsibleModule
from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, SUBTREE
import json
import pickle
import yaml

class LdapAnnuary:
	"""
	A class to represent a LDAP annuary

	...

	Attributes
	----------
	server : Server object
		Definition of a Server object

	connexion : Connexion object
		Definition of a Connexion object

	organizational_units_dicts : List
		Dictionaries of organizational units

	users_dicts : List
		Dictionaries of users

	organizational_units_objects : List
		A list of 0rganizationalUnit objects

	users_objects : List
		A list of InetOrgPerson objects

	data_ldif : str
		A String ldif file

	Methods
	-------
	__str__():
		Redefinition of method __str__

	fetch_ou_objects():
		To fetch a list of ou objects

	fetch_users_objects():
		To fetch a list of user objects

	fetch_ou_dicts():
		To fetch a list of ou dictionaries

	fetch_users_dicts(s):
		To fetch a list of users dictionaries

	write_data_ldif():
		To write informatons in file with ldif format

	copy_to_ldif_file():
		To create and write informations in ldif file

	copy_to_json_file():
		To create and write informations in json file

	copy_to_yaml_file():
		To create and write informations in yaml file	

	serialize_in_bin():
		To serialiaze, create and write informations in bin file	

	"""

	def __init__(self, ldap_main_host, connexion_username, connexion_password):
		"""
		Constructs all the necessary attributes for the LDAP annuary object

		...

		Attributes
		----------
		server : Server object
			Definition of a Server object

		connexion : Connexion object
			Definition of a Connexion object

		organizational_units_dicts : List
			Dictionaries of organizational units

		users_dicts : List
			Dictionaries of users

		organizational_units_objects : List
			A list of 0rganizationalUnit objects

		users_objects : List
			A list of InetOrgPerson objects

		data_ldif : str
			A String ldif file
		"""

		
		self.server = Server(ldap_main_host, get_info=ALL)
		self.connexion = Connection(self.server, connexion_username, connexion_password, auto_bind=True)
		self.organizational_units_dicts = self.fetch_ou_dicts()
		self.users_dicts = self.fetch_users_dicts()
		self.organizational_units_objects = self.fetch_ou_objects()
		self.users_objects = self.fetch_users_objects()
		self.data_ldif = self.write_data_ldif()
			

	def __str__(self):
		"""Redefinition of method __str__"""
		return self.data_ldif

	def fetch_ou_objects(self):
		"""To fetch a list of ou objects"""
		self.connexion.search(search_base = 'dc=sodbaveka,dc=com', search_filter = '(objectclass=organizationalUnit)', search_scope = SUBTREE, attributes=ALL_ATTRIBUTES)
		uo_list = []
		for element in self.connexion.response:
			uo_object = OrganizationalUnit(element)
			uo_list.append(uo_object)
		return uo_list

	def fetch_users_objects(self):
		"""To fetch a list of user objects"""
		self.connexion.search(search_base = 'dc=sodbaveka,dc=com', search_filter = '(objectclass=inetOrgPerson)', search_scope = SUBTREE, attributes=ALL_ATTRIBUTES)
		users_list = []
		for element in self.connexion.response:
			user_object = InetOrgPerson(element)
			users_list.append(user_object)
		return users_list

	def fetch_ou_dicts(self):
		"""To fetch a list of ou dictionaries"""
		self.connexion.search(search_base = 'dc=sodbaveka,dc=com', search_filter = '(objectclass=organizationalUnit)', search_scope = SUBTREE, attributes=ALL_ATTRIBUTES)
		return self.connexion.response

	def fetch_users_dicts(self):
		"""To fetch a list of users dictionaries"""
		self.connexion.search(search_base = 'dc=sodbaveka,dc=com', search_filter = '(objectclass=inetOrgPerson)', search_scope = SUBTREE, attributes = ALL_ATTRIBUTES)
		return self.connexion.response

	def write_data_ldif(self):
		"""To write informatons in file with ldif format"""
		ldif_file = ""
		# ##Method01
		# self.connexion.search(search_base = 'dc=sodbaveka,dc=com', search_filter = '(|(objectclass=organizationalUnit)(objectclass=inetOrgPerson))', search_scope = SUBTREE, attributes = ALL_ATTRIBUTES)
		# for entry in self.connexion.entries:
		# 	data = entry.entry_to_ldif().lstrip('version: 1\n').rstrip('# total number of entries: 1')
		# 	ldif_file += data
		##Method02
		for element in self.organizational_units_objects:
		 	ldif_file += "{}\n".format(element)
		for element in self.users_objects:
			ldif_file += "{}\n".format(element)
		return ldif_file.strip()

	def copy_to_ldif_file(self):
		"""To create and write informations in ldif file"""		
		file = open("annuary_backup.ldif","wt")
		file.write(self.data_ldif)
		file.close()
		print("Copy to ldif file completed.")

	def copy_to_json_file(self):
		"""To create and write informations in json file"""	
		file = open("annuary_backup.json","wt")
		# ##Method01 = example to create a string json file
		# file.write(simplejson.dumps(self.data_ldif))
		# ##Method02 = example by extracting data from a dictionary
		# new_list = []
		# for element in self.organizational_units_dicts:
		# 	new_dict = {}
		# 	new_dict['dn'] = element.get('dn')
		# 	new_dict['objectClass'] = element['attributes']['objectClass'][0]
		# 	new_dict['ou'] = element['attributes']['ou'][0]
		# 	new_dict['description'] = element['attributes']['description'][0]
		# 	new_list.append(new_dict)
		##Method03 = example by extracting data from an object
		new_list = []
		for element in self.organizational_units_objects:
			new_dict = {}
			new_dict['dn'] = element.dn
			new_dict['attributes'] = {}
			new_dict['attributes']['objectClass'] = element.objectClass
			new_dict['attributes']['ou'] = element.ou
			new_dict['attributes']['description'] = element.description
			new_list.append(new_dict)
		for element in self.users_objects:
			new_dict = {}
			new_dict['dn'] = element.dn
			new_dict['attributes'] = {}
			new_dict['attributes']['objectClass'] = element.objectClass
			new_dict['attributes']['givenName'] = element.givenName
			new_dict['attributes']['sn'] = element.sn
			new_dict['attributes']['cn'] = element.cn
			new_dict['attributes']['uid'] = element.uid
			new_dict['attributes']['userPassword'] = str(element.userPassword)
			new_list.append(new_dict)
		file.write(json.dumps(new_list, sort_keys=True, indent=4))
		file.close()
		print("Copy to json file completed.")

	def copy_to_yaml_file(self):
		"""To create and write informations in yaml file"""	
		file = open("annuary_backup.yaml","wt")
		new_list = []
		for element in self.organizational_units_objects:
			new_dict = {}
			new_dict['dn'] = element.dn
			new_dict['attributes'] = {}
			new_dict['attributes']['objectClass'] = element.objectClass
			new_dict['attributes']['ou'] = element.ou
			new_dict['attributes']['description'] = element.description
			new_list.append(new_dict)
		for element in self.users_objects:
			new_dict = {}
			new_dict['dn'] = element.dn
			new_dict['attributes'] = {}
			new_dict['attributes']['objectClass'] = element.objectClass
			new_dict['attributes']['givenName'] = element.givenName
			new_dict['attributes']['sn'] = element.sn
			new_dict['attributes']['cn'] = element.cn
			new_dict['attributes']['uid'] = element.uid
			new_dict['attributes']['userPassword'] = str(element.userPassword)
			new_list.append(new_dict)
		yaml.dump(new_list, file, sort_keys=True, indent=4)
		file.close()
		print("Copy to yaml file completed.")

	def serialize_in_bin(self):
		"""To serialiaze, create and write informations in bin file"""	
		try:
		    with open('annuary_backup.bin', 'wb') as file:
		        pickle.dump(self.organizational_units_objects, file, pickle.HIGHEST_PROTOCOL)
		        pickle.dump(self.users_objects, file, pickle.HIGHEST_PROTOCOL)
		        print("Serialization completed.")
		except (IOError, pickle.PicklingError):
			print('Writing error.')


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