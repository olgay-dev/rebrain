#!/usr/bin/python3
import telnetlib
import time

HOST = '192.168.1.253'
PORT = 23
LOGIN = 'admin'
PASSWD = 'admin'
CMD = 'show iproute'

def tn_connect(host, port, login, password):
    tn = telnetlib.Telnet(host, port)
    tn_auth(tn, login, password)
    tn.write(b'disable clipaging\r\n')
    tn.expect([b'#'], 5)
    return tn

def tn_auth(tn, login, password):
    auth_try = 3
    auth_ok = False
    try:
        while auth_try > 0:
            r = tn.expect([b'username:', b'UserName:', b'Username:'], 5)
            tn.write(bytes(login, 'utf-8'))
            tn.write(b'\r\n')
            time.sleep(0.5)
            r = tn.expect([b'password:', b'PassWord:', b'Password:'], 5)
            tn.write(bytes(password, 'utf-8'))
            tn.write(b'\r\n')
            time.sleep(0.5)
            r = tn.expect([b'#'], 5)
            print(r)
            if r[0] == 0:
                auth_ok = True
                print('Auth OK')
                return
            else:
                print("Auth Failed")
                auth_try -= 1
    except Exception as e:
        logger.exception(f'error: {e}')

def tn_disconnect(tn):
    tn.write(b'logout\r\n')
    tn.close()

def main():
    tn = tn_connect(HOST, PORT, LOGIN, PASSWD)
    time.sleep(0.5)
    cmd = CMD
    tn.write(bytes(cmd, 'utf-8'))
    tn.write(b'\r\n')
    r = tn.expect([b'#'], 5)
    print(r[2].decode())
    tn_disconnect(tn)
    
if __name__ == '__main__':
    main()
