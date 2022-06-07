# Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# By accessing this sample code, which is considered “AWS Training Content” 
# as defined in the AWS Learner Terms and Conditions,
# https://aws.amazon.com/legal/learner-terms-conditions/, you agree that 
# the AWS Learner Terms and Conditions govern your use of this sample code.

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import csv
import json
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", action="store", required=True, dest="path", help="CSV file path")
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", required=True, dest="certPath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", required=True, dest="keyPath", help="Private key file path")
parser.add_argument("-t", "--topic", action="store", required=True, dest="topic", help="Targeted topic")
parser.add_argument("-d", "--delay", action="store", required=True, dest="delay", help="Delay in seconds")
parser.add_argument("-l", "--loop", action="store", default=False, dest="loop", help="Loop file read")
parser.add_argument("-i", "--clientId", action="store", dest="clientId", default="myClientID", help="A unqiue client id")
args = parser.parse_args()

# CLI argument assignments
path = args.path
host = args.host
rootCAPath = args.rootCAPath
certPath = args.certPath
keyPath = args.keyPath
topic = args.topic
delay = float(args.delay)
loop = bool(args.loop)
clientId = args.clientId

print(f"Publishing messages on topic: {topic}")

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, keyPath, certPath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
time.sleep(2)

# open and parse file
with open(path) as csvfile:
  reader = csv.DictReader(csvfile)
  iterate = True

  # loop while true
  while iterate:

    # iterate rows
    for row in reader:  
      # create payload object
      obj = {}

      # iterate row items
      for key in row.keys():
        obj[key.lower()] = row[key]
    
      # add timestamp
      obj['timestamp'] = time.time()

      # create JSON payload
      payload = json.dumps(obj, separators=(',',':'))

      # publish payload on MQTT topic
      myAWSIoTMQTTClient.publish(topic, payload, 1)

      # print payload to console
      print(f"{payload}")

      # delay loop
      time.sleep(delay)

    # loop if true otherwise exit
    if loop:
      csvfile.seek(0)
      csvfile.next()
    else:
      iterate = False

myAWSIoTMQTTClient.disconnect()
