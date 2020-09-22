import os
import sys
import random
import string

import yaml
import cryptography  # For some mistakes
from cryptography.fernet import Fernet

CONN_ARR = {'TCN': '', 'DRV': '', 'SRV': '', 'DBN': '', 'UID': '', 'PWD': '', }


def FindConf(config_name, selector_key):
	"""
	search for correct connectiong string for this current selector_key.
	all conn_strings are stored in yaml file.
	:param config_name: file where we wants to store new data
	:param selector_key: Selector pointed to new(existing) key in Yaml connection string
	:return: fills CONN_ARR for retreiving some data from DB.
	"""
	path_to_config = ''  # os.path.join(os.path.expandvars("%userprofile%"), 'Documents\\')
	selector_key = selector_key.upper()
	try:
		with open(path_to_config + config_name) as fn:
			configs = yaml.safe_load(fn)  # , Loader=yaml.FullLoader
			# print(configs)
			configs = configs['connectors']  # root for yaml
			for cons in configs:
				if cons == selector_key:
					curr_conn = configs[cons]
					try:
						f = Fernet(curr_conn['KEY'])
						for key in CONN_ARR:
							try:
								if key in ('DBN', 'UID', 'PWD'):
									CONN_ARR[key] = f.decrypt(str.encode(curr_conn[key])).decode()
								else:
									CONN_ARR[key] = curr_conn[key]
							except KeyError:
								print('incompatible info inside connector')
						# ##### If we want to re-create hashes for each key - next few rows shows how
						# finally:
						#     f = Fernet(curr_conn['KEY'])
						#     print(key, f.encrypt(str.encode(CONN_ARR[key])))
					except TypeError:
						print('incompatible key value for decode/encode')
				# print('this is connection string', CONN_ARR)
	# ######################### EXCEPTION BLOCK ######################### #
	except ValueError:
		print('invalid literal for int()')
	except FileNotFoundError:
		print('check if the file is present')
	except yaml.parser.ParserError:
		print('some errors during parsing config')
	except KeyError:
		print('file don\'t have corresponding value for DB_connection')
	except TypeError:
		print('trying to go through range as like through dictionary')
	except AttributeError:
		print('trying to check some Attribute which is absent')
	except yaml.composer.ComposerError:
		print('some composer problems')


def PutEntry(config_name, selector_key):
	"""
	If we need to add new connection string - this function is exactly suited for.
	:param config_name: file where we wants to store new data
	:param selector_key: Selector pointed to new(existing) key in Yaml connection string
	:return:
	"""
	os.chdir(sys.path[1] + '\\conf\\')  # going to exact address of config file
	path_to_config = ''  # os.path.join(os.path.expandvars("%userprofile%"), 'Documents\\programs\\200820\\')
	selector_key = selector_key.upper()
	try:
		with open(path_to_config + config_name) as fn:
			configs = yaml.safe_load(fn)  # , Loader=yaml.FullLoader
		# Do Insert new values or Update existing
		new_frnt_key = Fernet.generate_key()
		f = Fernet(new_frnt_key)
		for key in CONN_ARR:
			try:
				if key in ('DBN', 'UID', 'PWD'):
					CONN_ARR[key] = f.encrypt(str.encode(CONN_ARR[key])).decode()
			except KeyError:
				print('incompatible info inside connector')
		configs['connectors'][selector_key] = CONN_ARR.copy()
		configs['connectors'][selector_key]['KEY'] = new_frnt_key.decode()
		pass
	except yaml.parser.ParserError:
		print('some errors during parsing config')
	except yaml.composer.ComposerError:
		print('some composer problems')
	# ######################################
	# configs = {'TEST': ''}
	with open(config_name, 'w') as outfile:
		yaml.dump(configs, outfile, default_flow_style=False)


# conf_name = 'data.yaml'
# CONN_ARR['TCN'] = 'Yes'
# CONN_ARR['DRV'] = '{SQL Server}'
# CONN_ARR['SRV'] = 'sql_server'
# CONN_ARR['DBN'] = 'TestingDB'
# CONN_ARR['UID'] = 'testing_user'
# CONN_ARR['PWD'] = 'testing_pass'
# print(CONN_ARR)
# PutEntry(conf_name, 'testing')
# print(CONN_ARR)
# FindConf(conf_name, 'test')
# print(CONN_ARR)
# FindConf(conf_name, 'testing')
# print(CONN_ARR)
