#!/bin/bash

python3 read_sqs_messages.py $1

python3 mask_data.py $1

python3 upload_to_postgres.py $1


