from .RequestController import RequestController

class BcaJadulController(RequestController):
	
	def __init__(self, request):
		RequestController.__init__(self, request)
		
		# Add your request controller tuple under this code
		self.REQ_MUTASI = ( ('username', self.ALPHANUMERIC), ('password', self.ALPHANUMERIC), ('rekening', self.TEXT), ('from_date', self.ISODATE), ('to_date', self.ISODATE) )
