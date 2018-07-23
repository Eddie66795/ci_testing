import boto3
import os
import sys
import json
import string
from jinja2 import Template

path_input_from_user = (sys.argv[1])
template = (sys.argv[2])
client = boto3.client('ssm')
firsttoken = " "
t = Template(template)


def get_response(path_input, token):

    response = client.get_parameters_by_path(
        Path='%s' % (path_input),
        Recursive=True,
        WithDecryption=True,
        NextToken=token
    )
    get_info(response)


def get_info(response_in):
    count = 0
    for item in response_in['Parameters']:
        value = response_in['Parameters'][count]['Value']
        fullName = response_in['Parameters'][count]['Name']
        split_path = fullName.split('/')
        name = fullName.split('/')[-1]
        if os.path.exists(split_path[1]):
            file1 = open('%s' % (split_path[1]), 'a')
            output_str = ("%s='%s'\n" % (name, value))
            output = (t.render(v=value, n=name))
            file1.write("%s\n" % (output))
        else:
            file1 = open('%s' % (split_path[1]), 'w')
            output = (t.render(v=value, n=name))
            file1.write("%s\n" % (output))
        file1.close()
        count = count+1
    print "Wrote " + str(count) + " variables to secrets file " + os.getcwd() + "/" + split_path[1]
    try:
        print "Token: " + response_in['NextToken']
        get_response(path_input_from_user, response_in['NextToken'])
    except KeyError:
        print "Token not found, no more data - Exiting"


get_response(path_input_from_user, " ")
