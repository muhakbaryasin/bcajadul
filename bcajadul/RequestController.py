import re
import datetime
import iso8601

import logging
log = logging.getLogger(__name__)

class RequestController(object):
	def __init__(self, request):
		self.request = request

		self.EMAIL = 'EMAIL'
		self.ALPHABET = 'ALPHABET'
		self.ALPHABET_SPACE = 'ALPHABET_SPACE'
		self.NUMERIC = 'NUMERIC'
		self.TEXT = 'TEXT'
		self.ALPHANUMERIC = 'ALPHANUMERIC'
		self.ALPHANUMERIC_SPACE = 'ALPHANUMERIC_SPACE'
		self.ISODATE = 'ISODATE'
		self.ISODATETIME = 'ISODATETIME'
		self.ISOTIME = 'ISOTIME'
		self.TIME = 'TIME'
		self.BOOLEAN = 'BOOLEAN'
		self.INITIAL_CODE = 'INITIAL_CODE'
	
	def isIsoDate(self, input_):
		try:
			datetime.datetime.strptime(input_, '%Y-%m-%d')
			return True
		except:
			return False
	
	def isIsoDatetime(self, input_):
		try:
			datetime.datetime.strptime(input_, '%Y-%m-%dT%H:%M:%S.%f')
			iso8601.parse_date(input_)
			return True
		except:
			log.exception('Date format')
			return False
	
	def isTime(self, input_):
		try:
			datetime.datetime.strptime(input_, '%H:%M')
			return True
		except:
			log.exception('Time format')
			return False

	def isAlphaNumeric(self, input_):
		# alphanumeric regex
		return re.compile(r"^\w+$").match(input_)
	
	def isAlphaNumericWithSpace(self, input_):
		# alphanumeric regex
		return re.compile(r"^[A-Za-z0-9\s]+$").match(input_)

	def isNumeric(self, input_):
		# numeric regex
		return re.compile(r"^[-+]?[0-9]+$").match(input_)

	def isAlphabet(self, input_):
		# alphabet regex
		return re.compile(r"^[a-zA-Z]+$").match(input_)
	
	def isAlphabetWithSpace(self, input_):
		# alphabet with space regex
		return re.compile(r"^[a-zA-Z\s]+$").match(input_)

	def isEmail(self, input_):
		# email regex
		return re.compile(r"[^@]+@[^@]+\.[^@]+").match(input_)
	
	def isText(self, input_):
		# text regex
		return (re.compile(r"^[A-Za-z0-9\/\s\t\n.,:;?!'\()%\"\-\+@]+$").match(input_))

	def isBoolean(self, input_):
		return (re.compile(r"^[0-1]+$").match(input_))
	
	def isInitialCode(self, input_):
		return (re.compile(r"^[A-Z]+$").match(input_))
	
	def checkComplete(self, requirement):
		required_item = []
		
		for item in requirement:
			if item[0] not in self.request.params:
				required_item.append( item[0] )
				continue
				
			input_type_is_fit = False
			
			if item[1] == self.EMAIL:
				input_type_is_fit = self.isEmail(self.request.params[ item[0] ])
			elif item[1] == self.NUMERIC:
				input_type_is_fit = self.isNumeric(self.request.params[ item[0] ])
			elif item[1] == self.ALPHABET:
				input_type_is_fit = self.isAlphabet(self.request.params[ item[0] ])
			elif item[1] == self.ALPHANUMERIC:
				input_type_is_fit = self.isAlphaNumeric(self.request.params[ item[0] ])
			elif item[1] == self.ALPHANUMERIC_SPACE:
				input_type_is_fit = self.isAlphaNumericWithSpace(self.request.params[ item[0] ])
			elif item[1] == self.ALPHABET_SPACE:
				input_type_is_fit = self.isAlphabetWithSpace(self.request.params[ item[0] ])
			elif item[1] == self.ISODATE:
				input_type_is_fit = self.isIsoDate(self.request.params[ item[0] ])
			elif item[1] == self.ISODATETIME:
				input_type_is_fit = self.isIsoDatetime(self.request.params[ item[0] ])
			elif item[1] == self.TIME:
				input_type_is_fit = self.isTime(self.request.params[ item[0] ])
			elif item[1] == self.TEXT:
				input_type_is_fit = self.isText(self.request.params[ item[0] ])
			elif item[1] == self.BOOLEAN:
				input_type_is_fit = self.isBoolean(self.request.params[ item[0] ])
			elif item[1] == self.INITIAL_CODE:
				input_type_is_fit = self.isInitialCode(self.request.params[ item[0] ])

			else:
				raise Exception("Something wrong with your input type - {}".format(item[1]))
			
			if not input_type_is_fit:
				raise Exception("Params '{}' value '{}' does not match format for {}".format(item[0], self.request.params[ item[0] ], item[1]) )
			
		if len( required_item ) > 0:
			your_req_params = []
			
			for param in self.request.params:
				your_req_params.append( param )
			
			raise Exception( 'Required params: ' + ', '.join( required_item ) + '. Your request params: ' + ', '.join(your_req_params) )
