# This script has the goal of masking the ip and the device_id variables.

# Set the working directory.

import sys

working_directory = sys.argv[1]

# Import the necessary functions.

import pandas as pd
from msticpy.data.data_obfus import hash_ip
from msticpy.data.data_obfus import hash_item


# Read the messages_data.csv file, which contains the data from SQS.

messages_data_file_name = working_directory + "/messages_data.csv"

df_masked = pd.read_csv(messages_data_file_name)

# Mask the ip variable with the hash_ip funciton 
# and the device_id variable with the hash_item function.

df_masked.ip = [hash_ip(i) for i in df_masked.ip]
df_masked.device_id = [hash_item(i, "-") for i in df_masked.device_id]

# Rename the ip and device_id variables to masked_ip and 
# masked_device_id.

df_masked = df_masked.rename(columns = {"ip": "masked_ip", 
                                 "device_id":"masked_device_id"})

# Save the masked data to the masked_data.csv file.

file_name = working_directory + "/masked_data.csv"

df_masked.to_csv(file_name, index = False)

