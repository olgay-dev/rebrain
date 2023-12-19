#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pykeadhcp import Kea
import copy

def main():
    server = Kea(host="http://kea.localnet", port=8000)
    config4 = server.dhcp4.config_get()
    if config4['result'] == 0:
        # get leases
        lease_ip_mac = {}
        lease4_all = server.dhcp4.api.send_command(command="lease4-get-all", service="dhcp4")
        if lease4_all['result'] == 0:
            leases = lease4_all['arguments']['leases']
            for lease in leases:
                if lease['subnet-id'] == 2:
                   lease_ip_mac.update({lease['ip-address']: lease['hw-address']})
        else:
            print("Can not get leases")
            return

        config = config4['arguments']
        config_copy = copy.deepcopy(config)

        for ip, mac in lease_ip_mac.items():
            subnets = config['Dhcp4']['subnet4']
            for subnet in subnets:
                if subnet['id'] == 2:
                    match = False
                    for reservation in subnet['reservations']:
                        if reservation['ip-address'] == ip:
                            match = True
                            break
                    if match == False:
                        subnet['reservations'].append({'hw-address': mac, 'ip-address': ip})
                        print(f"Add new reservation {ip} - {mac}")

        if config != config_copy:
            test_res = server.dhcp4.config_test(config)
            if test_res['result'] == 0:
                server.dhcp4.config_set(config)
                server.dhcp4.config_write("/etc/kea/kea-dhcp4.conf")
                print("Done")
            else:
                print("Config test failed!")

if __name__ == '__main__':
    main()