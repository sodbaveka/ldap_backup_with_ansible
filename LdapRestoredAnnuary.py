from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, SUBTREE
from OrganizationalUnit import OrganizationalUnit
from InetOrgPerson import InetOrgPerson
import pickle

class LdapRestoredAnnuary:
	"""
	A class to represent a LDAP annuary restored from a bin file called data.bin

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
	deserialize_from_file()
		To deserialize objects from a file called data.bin

	push_data()
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
		
	def deserialize_from_file(self):
		"""To deserialize objects from a file called data.bin"""
		try:
		    with open('data.bin', 'rb') as file:
		        self.uo_backup = pickle.load(file)
		        self.users_backup = pickle.load(file)
		        #print(self.uo_backup, self.users_backup, sep='\n')
		except (IOError, pickle.UnpicklingError):
		    print('Reading error.')

	def push_data(self):
		"""To perform an Add operation to backup server""" 
		for element in self.uo_backup:
			self.connexion.add(element.dn, attributes = element.attributes)
			print("{} created!".format(element.dn))
		for element in self.users_backup:
			self.connexion.add(element.dn, attributes = element.attributes)
			print("{} created!".format(element.dn))

	def delete_data(self):
		"""To perform an Delete operation to backup server""" 
		for element in self.users_backup:
			self.connexion.delete(element.dn)
			print("{} deleted!".format(element.dn))
		for element in self.uo_backup:
			self.connexion.delete(element.dn)
			print("{} deleted!".format(element.dn))