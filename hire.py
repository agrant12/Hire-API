import requests, json, sys
from settings import username, password

class Resource:
	"""Class to determine which url resource to use when accessing the API"""
	def resource(self, username, password):
		
		if username and password:
			resource = 'http://hiringapi.dev.voxel.net/v2/'
			V2(resource, username, password)
		else:
			resource = 'http://hiringapi.dev.voxel.net/v1/'
			V1(resource)

class API:
	"""Base class for V1 and V2 api resources"""

	#V2 Authentication 
	def auth(self, url):
		r = requests.get(url)
		json = r.json()

		if r.status_code == requests.codes.ok:
			status = json['status']
			self.printer(status)
		else:
			msg = json['msg']
			self.error(r.status_code, msg)

	#Retrieve List of keys
	def list(self, url):
		r = requests.get(url)
		json = r.json()

		if r.status_code == requests.codes.ok:
			status = json['status'] 
			self.printer(status)
		else:
			msg = json['msg']
			self.error(r.status_code, msg)

	# Get Key Value
	def get(self, url, key):
		r = requests.get(url)
		json = r.json()

		if r.status_code == requests.codes.ok:
			json = r.json()
			status = json[key]
			self.printer(status)
		else:
			msg = json['msg']
			self.error(r.status_code, msg)

	#Set Key and Value
	def set(self, url):
		r = requests.post(url)
		json = r.json()

		if r.status_code == requests.codes.ok:
			status = json['status'] 
			self.printer(status)
		else:
			msg = json['msg']
			self.error(r.status_code, msg)

	#Delete Key
	def delete(self, url):
		r = requests.delete(url)
		json = r.json()

		if r.status_code == requests.codes.ok:
			status = json['status'] 
			self.printer(status)
		else:
			msg = json['msg']
			self.error(r.status_code, msg)

	#Print Response
	def printer(self, data):
		sys.stdout.write(data + "\n")
        sys.stdout.flush()

    #Display if Error Thrown
	def error(self, status_code, error):
		print Exception("error %s %s" % (status_code, error))
		
class V1(API):
	"""" V1 Resource Class """
	def __init__(self, resource):
		with open('input/commands.txt', 'r') as f:
			for line in f:
				# Referance API Base Class and pass it along to Processor
				api = API()
				self.processor(api, resource, line)
		f.closed

	def set(self, api, resource, arg1, arg2):
		url = resource + 'key?key=' + arg1 + '&value=' + arg2
		api.set(url)

	def list(self, api, resource):
		url = resource + 'list'
		api.list(url)

	def get(self, api, resource, arg1):
		url = resource + 'key?key=' + arg1
		api.get(url, arg1)

	def delete(self, api, resource, arg1):
		url = resource + 'key?key=' + arg1
		api.delete(url)

	funcdict = {
		'set' : set,
		'list': list,
		'get': get,
		'delete': delete
	}

	#Process String into Commands and Arguments
	def processor(self, api, resource, *args):
		for w in args:
			params = w.split()
			func = params[0]

			if len(params) == 3:
				arg1 = params[1]
				arg2 = params[2]
				self.funcdict[func]('self', api, resource, arg1, arg2)
			elif len(params) == 2:
				arg1 = params[1]
				self.funcdict[func]('self', api, resource, arg1)
			else:
				self.funcdict[func]('self', api, resource)
				
class V2(API):
	"""" V2 Resource Class """
	def __init__(self, resource, username, password):
		api = API()

		r = requests.get(resource + 'auth?user=' + username + '&pass=' + password)
		
		if r.status_code == requests.codes.ok:
			json = r.json()
			token = json['token']
			with open('input/commands2.txt', 'r') as f:
				for line in f:
					self.processor(api, token, resource, line)
			f.closed
		else:
			json = r.json()
			msg = json['msg']
			print Exception("error %s %s" % (r.status_code, msg))

	def auth(self, api, token, resource, arg1, arg2):
		url = resource + 'auth?user=' + arg1 + '&pass=' + arg2
		api.auth(url)

	def set(self, api, token, resource, arg1, arg2):
		url = resource + 'key?token=' + token + '&key=' + arg1 + '&value=' + arg2
		api.set(url)

	def list(self, api, token, resource):
		url = resource + 'list?token=' + token
		api.list(url)

	def get(self, api, token, resource, arg1):
		url = resource + 'key?token=' + token + '&key=' + arg1
		api.get(url, arg1)

	def delete(self, api,token, resource, arg1):
		url = resource + 'key?token=' + token + '&key=' + arg1
		api.delete(url)

	funcdict = {
		'auth': auth,
		'set' : set,
		'list': list,
		'get': get,
		'delete': delete
	}

	#Process String into Commands and Arguments
	def processor(self, api, token, resource, *args):
		for w in args:
			params = w.split()
			func = params[0].strip(',')

			if len(params) == 3:
				arg1 = params[1]
				arg2 = params[2]
				self.funcdict[func]('self', api, token, resource, arg1, arg2)
			elif len(params) == 2:
				arg1 = params[1]
				self.funcdict[func]('self', api, token, resource, arg1)
			else:
				self.funcdict[func]('self', api, token, resource)

if __name__ == '__main__':
	r = Resource()
	r.resource(username, password)
