import sys
import subprocess
import os
from os import path
from datetime import datetime
from shutil import copyfile
sevenZipExecutable = "7z"
codeExecutable = "code"

try:
	nameProgram = sys.argv[0]
	nInput = len(sys.argv[1:])
	inputs = sys.argv[1:]
	HelpStr = ['\nUsage:\n        python runProcess_v2.py [Option 1 Option 2]\n\n',\
					'The options are mandatory:',\
					'  - Option 1 is the name of the ticket',\
					'  - Option 2 is the name of the zip data\n\n\n']
					
	if (nInput > 2):
		print('Too many input parametres. Use \'-help\' to read the correct options')
		sys.exit()
	elif (nInput == 0):
		for h in HelpStr:
			print (h)
		sys.exit()
	elif (nInput == 1):
		if (inputs[0] == '-help'):
			for h in HelpStr:
				print (h)
			sys.exit()
		else:
			print('Input is not valid. Use \'-help\' to read the correct options')
			sys.exit()
	else:
		print('\n\n' + str(nInput))
		ticket = inputs[0]
		data = inputs[1]
		cwd = os.getcwd()
		dst = cwd + os.sep + 'ticket' + os.sep + ticket
		src = cwd + os.sep + data

		# cmd = ['7z', 'e', src]
		subprocess.call('cls', shell=True)
		cmd = sevenZipExecutable + ' x ' + src + ' -o' + dst
		
		# print (cmd)
		print (dst)
		print (src)
		if (path.exists(src) and not path.exists(dst) \
			and path.isfile(src)):
			print ('\n' + str(datetime.now()) +\
					'      Processing ...\n')
			cmdVS = codeExecutable + ' ' + dst
			os.system(cmd)
			os.system(cmdVS)
			
			print ('\n' + str(datetime.now()) +\
					'      Finish!\n')
			sys.exit()
		if not path.exists(src):
			print('No data at {}\n'.format(src))
			print(path, src)
			print('Check it')
		if path.exists(dst):
			print('Destination path ({}) already exists'.format(dst))
except Exception as e:
	print(str(datetime.now()) + " runProcess_v2: Error occurred! \n")
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print("Type error: " + str(e))
	print('File Name:', fname, 'Line Numer:', exc_tb.tb_lineno, end = '\n\n')
	