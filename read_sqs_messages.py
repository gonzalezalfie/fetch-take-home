# This script has the goal of reading all the messages from AWS SQS.

# Set the working directory.

import sys

working_directory = sys.argv[1]

# Import the necessary modules and functions.

import boto3
import pandas as pd
from datetime import date
import json

# Connect to SQS using boto3.

sqs = boto3.client("sqs", 
                   endpoint_url = "http://localhost:4566/000000000000/login-queue")

resp = sqs.receive_message(
    QueueUrl = "http://localhost:4566/000000000000/login-queue", 
    AttributeNames = ["All"], 
    MaxNumberOfMessages = 10
)

# Retrieve all messages from the queue.

messages = []
while True:
    response = sqs.receive_message(
        QueueUrl = "http://localhost:4566/000000000000/login-queue", 
        AttributeNames = ["All"], 
        MaxNumberOfMessages = 10
        )
    if "Messages" not in response:
        break
    messages += response["Messages"]

# Create a data frame where we will store the data.

n = len(messages)

for i in range(n):
    messages[i]["Body"] = json.loads(messages[i]["Body"])

df = pd.DataFrame({
    "user_id": ["a"]*n, 
    "device_type" : ["a"]*n, 
    "ip" : ["a"]*n, 
    "device_id" : ["a"]*n, 
    "locale" : ["a"]*n, 
    "app_version" : [0]*n, 
    "create_date" : [date.fromtimestamp(100)]*n
    })

# Define 2 functions: 

# get_dict_value() gets a value from a dictionary if the key 
# actually exists. If it doesn't, it returns None.

# version_to_integer() transforms a version number into an integer.
# It replaces "." with 0, and in order to preserve an initial 0 value, 
# it adds 1000 to the number that comes before the first ".".
# For example: 
#    "6.4.8" becomes 10060408
#    "0.38" becomes 100038
# In that way we can notice when the initial digit was 0 because 
# we see 1000 in the beginning.

def get_dict_value(key, dictionary):
    return(dictionary[key] if key in dictionary.keys() else None)

def version_to_integer(version):
    if version is None:
        return(None)
    else:
        l = [int(x, 10) for x in version.split('.')]
        l.reverse()
        l[-1] = 1000+l[-1]
        return(sum(x * (100 ** i) for i, x in enumerate(l)))

# Get the data from the messages.

for i in range(n):
    df["user_id"][i] = get_dict_value("user_id", messages[i]["Body"])
    df["device_type"][i] = get_dict_value("device_type", messages[i]["Body"])
    df["ip"][i] = get_dict_value("ip", messages[i]["Body"])
    df["device_id"][i] = get_dict_value("device_id", messages[i]["Body"])
    df["locale"][i] = get_dict_value("locale", messages[i]["Body"])
    df["app_version"][i] = get_dict_value("app_version", messages[i]["Body"])
    df["create_date"][i] = date.fromtimestamp(int(get_dict_value("SentTimestamp", messages[i]["Attributes"])))

# Convert the version number into integers.

df.app_version = [version_to_integer(i) if i is not None else None for i in df.app_version]
df.app_version = df.app_version.astype("int", errors = "ignore")

# Save the data frame as csv file.

file_name = working_directory + "/messages_data.csv"

df.to_csv(file_name, index = False)

