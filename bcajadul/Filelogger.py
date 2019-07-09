import sys
import os

import time
import datetime

class FileLogger(object):
	def __init__(self, file_log_name = None, reference = None, data = None, exception = None, mode = None):
		if file_log_name is not None and data is not None and mode is not None:
			limiter = "=============================================================\n"
			timestampString = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%y %H:%M:%S') + "\n"
			shuter = "\n\n"
			
			line_number = ''
			data_ = limiter + timestampString
			
			mode_is_byte = False
			data_is_byte = False
			
			if mode.find('b') > -1:
				mode_is_byte = True
				shuter = shuter.encode('UTF-8')
			
			if type( data ) is bytes:
				data_is_byte = True
				if not mode_is_byte:
					mode = mode.replace( 'b', '' )
			
			if exception is not None:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				line_number = " :\n\t - " + fname + " at " + str(exc_tb.tb_lineno)
				data_ += str(reference) + line_number + "\n\t - " 
				
				if data_is_byte:
					data_ = data_.encode('UTF-8')
								
				data_ += data
				
				if data_is_byte:
					data_ += ("\n\t - " + str(exception) + "\n\n").encode('UTF-8')
				else:
					data_ += "\n\t - " + str(exception) + "\n\n"
			else:
				data_ += "\n\t - "
				if data_is_byte:
					data_ = data_.encode('UTF-8')
			
			data_ += data + shuter
			
			here = os.path.dirname(__file__)
			file_log_path = os.path.join(here, 'Log', file_log_name)
			
			file = open(file_log_path, mode)
			try:
				if	file.write(data_):
					file.close()
			except:
				pass
