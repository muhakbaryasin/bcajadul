from collections import OrderedDict
import re

class ErrorCodeController(object):
	ERROR_NUMBER = OrderedDict([
			(1, ("ERROR", "Unkown error", ) ), # json syntax is not valid
			(51, ("ERROR", "Expecting value", ) ), # json syntax is not valid
			(52, ("ERROR", "Expecting property name enclosed in double quotes") ), # json syntax is not valid
			(53, ("ERROR", "Unterminated string starting at") ), # json syntax is not valid
			(54, ("ERROR", "Expecting ',' delimiter") ), # json syntax is not valid
			(55, ("ERROR", "Expecting ':' delimiter") ), # json syntax is not valid
			(56, ("ERROR", "Incorrect padding") ), # base64 failed to decode
			# regex matching
			(101, ("ERROR", "Params '{some_var}' does not match format for {some_var}") ),
			(102, ("ERROR", "Phone number {some_var} is not match format", "No. telp. yang dimasukkan tidak sesuai format. Ex:+62-856-96960xxx .") ),
			
			(201, ("DENIED", "Required params") ), # parameter is not complete
			(205, ("ERROR", "Unable to get best key", "Kursi tidak tersedia. Silahkan coba jadwal lain.") ),
			(206, ("DENIED", "Login {some_var} is inuse for {some_var}") ),
			
			
		])
	
	def __init__(self, message=None, exception=None):
		# unknown error
		self.error_code_no = 1
		self.error_status = 'ERROR'
		self.message2EndUser = None
		
		if message is not None or exception is not None:
			self.setMessage( message = message, exception = exception )
		
	def setMessage(self, message=None, exception=None):
		self.error_message = message
		if exception is not None:
			self.error_message = str( exception )
		
		self.findErrorCode()
		
	def createRegex(self, regex_string):
		regex_string = regex_string.replace(' ', '')
		gen_regex = '^'
		split_regex = regex_string.split('{some_var}')
		
		for iter, each in enumerate(split_regex):
			if iter == 1:
				gen_regex += '.*'
			
			gen_regex += each
			
			#if iter == len(split_regex) - 1 and iter > 0:
			#	gen_regex += '$'
				
		return gen_regex
	
		
	def findErrorCode(self):
		if self.error_message is None:
			raise Exception("MESSAGE is NONE")
		
		for error_code_no in self.ERROR_NUMBER:
			regex = self.createRegex( self.ERROR_NUMBER[error_code_no][1] )
			in_ = self.error_message.replace(' ', '')

			if re.search(regex, in_):
				self.error_code_no = error_code_no
				self.error_status = self.ERROR_NUMBER[error_code_no][0]
				try:
					self.message2EndUser = self.ERROR_NUMBER[error_code_no][2]
				except:
					pass
	
	def getErrorCodeNo(self):
		return self.error_code_no
		
	def getErrorStatus(self):
		return self.error_status
		
	def getMessage2EndUser(self):
		return self.message2EndUser
