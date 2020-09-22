# from modules import auth_module as am  # if you want to check only this module
from modules import pais as ps

file_name0 = 'b999.xlsx'

file_name1 = 'bTest202020.xlsx'

# a = am.FindConf(conf_name, key)
# print(a, am.CONN_ARR)
ps.doJob(file_name0, file_name1)
# doJob - return just answer, so you will have to open result file after receiving that answer
