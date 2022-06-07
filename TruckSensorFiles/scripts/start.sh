# Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# By accessing this sample code, which is considered “AWS Training Content” 
# as defined in the AWS Learner Terms and Conditions,
# https://aws.amazon.com/legal/learner-terms-conditions/, you agree that 
# the AWS Learner Terms and Conditions govern your use of this sample code.

# stop script on error
set -e

# install AWS Device SDK for Python if not already installed
if [ ! -d ./aws-iot-device-sdk-python ]; then
    printf "\nInstalling AWS IoT Device SDK for Python...\n"
    git clone https://github.com/aws/aws-iot-device-sdk-python.git
    pushd aws-iot-device-sdk-python
    sudo python3 setup.py install
    popd
fi

# install jq if not already installed
if ! command -v jq &> /dev/null 
then
    printf "jq could not be found, installing...\n"
    sudo yum install jq
fi

echo -n "Enter the device name > "
read response
if [ -n "$response" ]; then
    device=$response
fi

if [ -z "$device" ]; then
        echo -e "\n Usage $0 \n"
        exit 0
fi

aws iot describe-endpoint > /tmp/iotendpoint.json
iot_endpoint=$(jq -r ".endpointAddress" /tmp/iotendpoint.json)
# run pub/sub sample app using certificates downloaded in package
printf "\nRunning truck sensor sample application...\n"
python3 /home/ec2-user/environment/scripts/trucksensor.py -p /home/ec2-user/environment/data/trucksensordata.csv -e $iot_endpoint -r /home/ec2-user/environment/certs/root-CA.crt -c /home/ec2-user/environment/certs/$device.cert.pem -k /home/ec2-user/environment/certs/$device.private.key -t truck/freezer -d 2 -l True