#!/usr/bin/python

DOCUMENTATION = '''
---
module: asm_server_technologies
author: Pedro Correia (@correiap)
version_added: "1.0"
short_description: Get the SelfLink associated with an ASM Server Technology
description:
    - This module retrives the SelfLink associated with an ASM Server Technology. It takes the Management IP or Hostname of the F5 BIG-IP Device,
      the Authentication Token and the name of the Server Technology. Then it performs a loop to fetch the SelfLink based on the Server Technology Name.
references:
      F5 iControl REST API User Guide Version 13.0
requirements:
    - none
options:
    host:
        description:
            - The IP address or hostname of the F5 appliance
        required: true
    token:
        description:
            - F5 Authentication Token
        required: true
    server_technology:
        description:
            - Server Technology Name
        required: true
'''

EXAMPLES = '''
    - name: Get Server Technology SelfLink
      asm_server_technologies:
        host: "{{ HOSTNAME }}"
        token: "{{ TOKEN }}"
        server_technology: "{{ ST_NAME }}"
	  register: st_selflink
	  
    - name: Assign ASM Hash to Variable 
      set_fact:
        ASM_HASH: "{{asm_hash.ASM_Hash}}"
'''


import sys
import time
import json
import requests



from ansible.module_utils.basic import *

def genURI (mgmtip):

	URI = "https://" + mgmtip + "/mgmt/tm/asm/server-technologies"

	return (URI)

def getInfo (URI, token):

	headers = {'content-type': "application/json", 'x-f5-auth-token': token}

	r = requests.get(URI, headers=headers, verify=False)

	content = r.json()

	return (content)

def asmHash (asmInfo, server_technology):

    count = 0
    st_selflink = ""
    
    while server_technology != asmInfo['items'][count]['serverTechnologyDisplayName']:
        count +=1

    st_selflink =  asmInfo['items'][count]['selfLink']
    return st_selflink

def main():
	
	module_args = AnsibleModule(
        	argument_spec = dict(
            		mgmtip = dict(required=True),
            		token = dict(required=True),
            		server_technology  = dict(required=True, no_log=True)
         	),
        	check_invalid_arguments=False,
        	add_file_common_args=True
	)
    
    	result = dict(
        	changed=False,
        	original_message='',
        	message=''
    	)



    #function to generate URI
	URI = genURI (module_args.params["mgmtip"])

	#function to make GET request
	asmInfo = getInfo (URI, module_args.params["token"])

	#function to extract st_selflink information
	st_selflink = asmHash (asmInfo, module_args.params["server_technology"])

	module_args.exit_json(changed=False, ST_SELFLINK=st_selflink)

if __name__ == '__main__':
    main()

