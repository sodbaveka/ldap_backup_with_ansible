from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, SUBTREE
import json
import simplejson
from OrganizationalUnit import OrganizationalUnit
from InetOrgPerson import InetOrgPerson
import pickle

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

	Methods
	-------
	name(additionnale):
		descript
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
		self.organizational_units_dicts = self.get_ou_dicts()
		self.users_dicts = self.get_users_dicts()
		self.data_ldif = self.get_data_ldif()
		self.organizational_units_objects = self.get_ou_objects()
		self.users_objects = self.get_users_objects()
			

	def __str__(self):
		return self.data_ldif

	def get_ou_objects(self):
		self.connexion.search(search_base = 'dc=sodbaveka,dc=com', search_filter = '(objectclass=organizationalUnit)', search_scope = SUBTREE, attributes=ALL_ATTRIBUTES)
		uo_list = []
		for element in self.connexion.response:
			uo_object = OrganizationalUnit(element)
			uo_list.append(uo_object)
		return uo_list

	def get_users_objects(self):
		self.connexion.search(search_base = 'dc=sodbaveka,dc=com', search_filter = '(objectclass=inetOrgPerson)', search_scope = SUBTREE, attributes=ALL_ATTRIBUTES)
		users_list = []
		for element in self.connexion.response:
			user_object = InetOrgPerson(element)
			users_list.append(user_object)
		return users_list

	def get_ou_dicts(self):
		self.connexion.search(search_base = 'dc=sodbaveka,dc=com', search_filter = '(objectclass=organizationalUnit)', search_scope = SUBTREE, attributes=ALL_ATTRIBUTES)
		uo_list = []
		for element in self.connexion.response:
			uo_list.append(element)
		return uo_list

	def get_users_dicts(self):
		self.connexion.search(search_base = 'dc=sodbaveka,dc=com', search_filter = '(objectclass=inetOrgPerson)', search_scope = SUBTREE, attributes = ALL_ATTRIBUTES)
		users_list = []
		for element in self.connexion.response:
			users_list.append(element)
		return users_list

	def get_data_ldif(self):
		ldif_file = ""
		self.connexion.search(search_base = 'dc=sodbaveka,dc=com', search_filter = '(|(objectclass=organizationalUnit)(objectclass=inetOrgPerson))', search_scope = SUBTREE, attributes = ALL_ATTRIBUTES)
		for entry in self.connexion.entries:
			data = entry.entry_to_ldif().lstrip('version: 1\n').rstrip('# total number of entries: 1')
			ldif_file += data
		return ldif_file.strip()

	def copy_to_ldif_file(self):		
		file = open("annuary_backup.ldif","wt")
		file.write(self.data_ldif)
		file.close()

	def copy_to_json_file(self):
		file = open("annuary_backup.json","wt")
		file.write(simplejson.dumps(self.data_ldif))
		file.close()

	def serialize_in_file(self):
		try:
		    with open('data.bin', 'wb') as file:
		        pickle.dump(self.organizational_units_objects, file, pickle.HIGHEST_PROTOCOL)
		        pickle.dump(self.users_objects, file, pickle.HIGHEST_PROTOCOL)
		except (IOError, pickle.PicklingError):
		    print('Writing error.')