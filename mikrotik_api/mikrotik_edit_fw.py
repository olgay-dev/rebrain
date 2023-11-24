#!/usr/bin/python3
import mikrotik_api

HOSTS = [
'mt1.localnet', 
'mt2.localnet',
'mt3.localnet',
'mt4.localnet',
'mt5.localnet',
'mt6.localnet', 
'mt7.localnet',
'mt8.localnet',
'mt9.localnet',
'mt10.localnet',
]
LOGIN = 'admin'
PASSWD = 'admin'
NEW_MAC = '00:0C:29:32:E6:95'

def get_allowed_mac_list(host, login, passwd, connection=None):
	cmd = '/ip/firewall/filter/print'
	res = mikrotik_api.execute(host, login, passwd, cmd, connection=connection)
	allowed_mac_list = []
	for r in res:
		if r['action'] == 'accept':
			allowed_mac_list.append(r['src-mac-address'])
	return allowed_mac_list

def main():
	for host in HOSTS:
		# 1 - get current allowed_mac_list
		cur_allowed_mac_list = get_allowed_mac_list(host, LOGIN, PASSWD)
		print("%s allowed MAC addresses:\n%s, \nAdding %s..." % (host, cur_allowed_mac_list, NEW_MAC))

		if NEW_MAC not in cur_allowed_mac_list:
			# 2 - add new MAC to allowed_mac_list
			s = mikrotik_api.execute(host, LOGIN, PASSWD, '', return_connection=True)
			cmd = '/ip/firewall/filter/add'
			cmd_arg = {'chain': 'input', 'src-mac-address': NEW_MAC, 'action': 'accept', 'place-before': 0}
			mikrotik_api.execute(host, LOGIN, PASSWD, cmd, cmd_arg, connection=s)

		    # 3 - get new allowed_mac_list
			print("---> %s\n" % get_allowed_mac_list(host, LOGIN, PASSWD, s))
		else:
			print("---> MAC already exists in firewall filter rules!\n")


if __name__ == '__main__':
    main()
