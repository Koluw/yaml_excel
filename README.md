# yaml_excel
In yaml we will store some connection_info to DB. Because of security needs data will be stored as hash. Some field will be exactly key for unhash the real data
Excel part will be used for read some data from Excel, manipulate with them and put in another place of Excel and store file.
At the moment this part will be almost deprecated - simple read and save in 2 procedures.
#Hash
Since there is a difference between two string's length, there are few results after hash.
The one when length of source string less than 15 symbols, we receive 90 symbols hash with "==" at the end.<br>
In case we wants to hide string with bigger length - then we will receive 110 symbols with "=" at the end.<br>
If you are going to hide it - don't forget about this feature.