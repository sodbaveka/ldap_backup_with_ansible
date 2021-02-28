#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Mickaël Duchet <sodbaveka@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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