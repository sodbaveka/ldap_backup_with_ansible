#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Mickaël Duchet <sodbaveka@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, SUBTREE
import pickle
import json
from ansible.module_utils.OrganizationalUnit import OrganizationalUnit
from ansible.module_utils.InetOrgPerson import InetOrgPerson

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