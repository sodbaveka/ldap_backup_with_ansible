class InetOrgPerson:
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
		self.givenName = uo_dict['attributes']['givenName'][0]
		self.sn = uo_dict['attributes']['sn'][0]
		self.cn = uo_dict['attributes']['cn'][0]
		self.uid = uo_dict['attributes']['uid'][0]
		self.userPassword = uo_dict['attributes']['userPassword'][0]

	def __str__(self):
		return "dn: {}\nobjectClass: {}\ngivenName: {}\nsn: {}\ncn: {}\nuid: {}\nuserPAssword: {}\n".format(self.dn, self.objectClass, self.givenName, self.sn, self.cn, self.uid, self.userPassword)