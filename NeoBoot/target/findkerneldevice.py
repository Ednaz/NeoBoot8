#!/usr/bin/python
#!/usr/bin/python

import os
import sys
import collections
import struct
import sys
import uuid

# http://en.wikipedia.org/wiki/GUID_Partition_Table#Partition_table_header_.28LBA_1.29
GPT_HEADER_FORMAT = """
8s signature
4s revision
L header_size
L crc32
4x _
Q current_lba
Q backup_lba
Q first_usable_lba
Q last_usable_lba
16s disk_guid
Q part_entry_start_lba
L num_part_entries
L part_entry_size
L crc32_part_array
"""

# http://en.wikipedia.org/wiki/GUID_Partition_Table#Partition_entries_.28LBA_2.E2.80.9333.29
GPT_PARTITION_FORMAT = """
16s type
16s unique
Q first_lba
Q last_lba
Q flags
72s name
"""

file = '/boot/STARTUP'
myfile = open(file, 'r')
data = myfile.read().replace('\n', '')
myfile.close()

rootfsdevice = data.split("=",1)[1].split(" ",1)[0]
kerneldevice = rootfsdevice[:-1] + str(int(rootfsdevice[-1:]) -1)

if os.access('/dev/kernel', os.R_OK):
	os.remove('/dev/kernel')
	os.symlink(kerneldevice, '/dev/kernel')
else:
	os.symlink(kerneldevice, '/dev/kernel')

# print kerneldevice
