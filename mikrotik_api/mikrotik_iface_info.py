#!/usr/bin/python3
import mikrotik_api
import json

HOST = 'mt1.localnet'
LOGIN = 'admin'
PASSWD = 'admin'
CMD = '/interface/print'
CMD_ARG = {} 

def main():
    res = mikrotik_api.execute(HOST, LOGIN, PASSWD, CMD, CMD_ARG)
    #print(res)
    for r in res:
        print(json.dumps(r, indent = 3))

if __name__ == '__main__':
    main()
