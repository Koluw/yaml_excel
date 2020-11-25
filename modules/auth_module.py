import os
import sys
import random
import string

import yaml
import cryptography  # For proper handling some mistakes
from cryptography.fernet import Fernet

CONFIG_FILE = 'data.yaml'
CONN_ARR = {'TCN': '', 'DRV': '', 'SRV': '', 'DBN': '', 'UID': '', 'PWD': '', }
FIELDS_TO_HIDE = ('SRV', 'UID', 'PWD')


def find_config(selector_key):
	"""
	search for correct connection string for this current selector_key.
	all conn_strings are stored in yaml file.
	# :param CONFIG_FILE: file where we wants to store new data default value
	:param selector_key: Selector pointed to new(existing) key in Yaml connection string
	:return: type 0/1 to define if the execution was successful.
	:return: CONN_ARR copy for retrieving some data from DB. in case type = 1.
	"""
	# os.chdir(sys.path[1] + '\\conf\\')
	path_to_config = 'conf\\'  # os.path.join(os.path.expandvars("%userprofile%"), 'Documents\\')
	selector_key = selector_key.upper()
	local_arr = CONN_ARR.copy()
	result_string = ''
	answer_def = 0
	try:
		with open(path_to_config + CONFIG_FILE) as fn:
			configs = yaml.safe_load(fn)  # , Loader=yaml.FullLoader
			# print(configs)
			configs = configs['connectors']  # root for yaml
			for cons in configs:
				if cons == selector_key:
					curr_conn = configs[cons]
					try:
						f = Fernet(curr_conn['KEY'])
						for key in local_arr:
							try:
								if key in FIELDS_TO_HIDE:
									local_arr[key] = f.decrypt(str.encode(curr_conn[key])).decode()
								else:
									local_arr[key] = curr_conn[key]

							except KeyError:
								result_string = 'incompatible info inside connector'
								answer_def = 0
						# ##### If we want to re-create hashes for each key - next few rows shows how
						# finally:
						#     f = Fernet(curr_conn['KEY'])
						#     print(key, f.encrypt(str.encode(CONN_ARR[key])))
					except TypeError:
						result_string = 'incompatible key value for decode/encode'
						answer_def = 0
					answer_def = 1

				# print('this is connection string', CONN_ARR)
	# ######################### EXCEPTION BLOCK ######################### #
	except ValueError:
		result_string = 'invalid literal for type conversion'
		answer_def = 0
	except FileNotFoundError:
		result_string = 'check if the config file is present'
		answer_def = 0
	except yaml.parser.ParserError:
		result_string = 'some errors during parsing config'
		answer_def = 0
	except KeyError:
		result_string = 'file don\'t have corresponding value for DB_connection'
		answer_def = 0
	except TypeError:
		result_string = 'trying to go through range as like through dictionary'
		answer_def = 0
	except AttributeError:
		result_string = 'trying to check some Attribute which is absent'
		answer_def = 0
	except yaml.composer.ComposerError:
		result_string = 'some composer problems'
		answer_def = 0
	if answer_def == 0:
		print(result_string)
	return answer_def, local_arr


def put_entry(selector_key):
	"""
	If we need to add new connection string - this function is exactly suited for.
	# :param CONFIG_FILE: file where we wants to store new data
	:param selector_key: Selector pointed to new(existing) key in Yaml connection string
	:return: type 0/1 to define if the execution was successful.
	"""

	# ##### there are few ways to get the config file. through the os library and relative path.
	# os.chdir(sys.path[1] + '\\conf\\')  # going to exact address of config file
	path_to_config = 'conf\\'  # os.path.join(os.path.expandvars("%userprofile%"), 'Documents\\programs\\200820\\')
	selector_key = selector_key.upper()
	result_string = ''
	local_arr = CONN_ARR.copy()
	try:
		with open(path_to_config + CONFIG_FILE) as fn:
			configs = yaml.safe_load(fn)  # , Loader=yaml.FullLoader

	except yaml.parser.ParserError:
		answer_def = 0
		result_string = 'some errors during parsing config'
	except yaml.composer.ComposerError:
		answer_def = 0
		result_string = 'some composer problems'
	except FileNotFoundError:
		result_string = 'there was no previous config file, we\'ll create a new one'
		configs = {}
	# Do Insert new values or Update existing
	new_frnt_key = Fernet.generate_key()
	f = Fernet(new_frnt_key)
	for key in local_arr:
		try:
			if key in FIELDS_TO_HIDE:
				local_arr[key] = f.encrypt(str.encode(CONN_ARR[key])).decode()
		except KeyError:
			answer_def = 0
			result_string = 'incompatible info inside connector'
	configs['connectors'][selector_key] = local_arr.copy()
	configs['connectors'][selector_key]['KEY'] = new_frnt_key.decode()
	# ######################################
	# configs = {'TEST': ''}
	with open(path_to_config + CONFIG_FILE, 'w') as outfile:
		yaml.dump(configs, outfile, default_flow_style=False)
		answer_def = 1
	print(result_string) if result_string else None
	return answer_def


# conf_name = 'data.yaml'
# CONN_ARR['TCN'] = 'Yes'
# CONN_ARR['DRV'] = '{SQL Server}'
# CONN_ARR['SRV'] = 'sql_server'
# CONN_ARR['DBN'] = 'TestingDB'
# CONN_ARR['UID'] = 'testing_user'
# CONN_ARR['PWD'] = 'testing_pass'
# print(CONN_ARR)
# put_entry(conf_name, 'testing')
# print(CONN_ARR)
# find_conf(conf_name, 'test')
# print(CONN_ARR)
# find_conf(conf_name, 'testing')
# print(CONN_ARR)
