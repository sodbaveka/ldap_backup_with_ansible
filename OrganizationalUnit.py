class OrganizationalUnit:
	"""
	A class to represent a LDAP Organizational Unit

	...

	Attributes
	----------
	server : Server object
		Definition of a Server object

	Methods
	-------
	name(additionnale):
		descript
	"""

	def __init__(self, uo_dict):
		"""
		Constructs all the necessary attributes for the LDAP Organizational Unit object

		...

		Attributes
		----------
		server : Server object
			Definition of a Server object

		"""

		
		self.dn = uo_dict['dn']
		self.attributes = uo_dict['attributes']
		self.objectClass = uo_dict['attributes']['objectClass'][0]
		self.ou = uo_dict['attributes']['ou'][0]
		self.description = uo_dict['attributes']['description'][0]

	def __str__(self):
		return "dn: {}\nobjectClass: {}\nou: {}\ndescription: {}\n".format(self.dn, self.objectClass, self.ou, self.description)