##!/usr/bin/python
# -*- coding: utf-8 -*-

from mysql import MysqlClass
from Device import DeviceClass

ARP_OID = '.1.3.6.1.2.1.4.22.1.2'

sql = MysqlClass()
sql.connect()

###

sql_user_info = {}
query = "SELECT ip, mac FROM user"
sql_res = sql.execute_query(query)
for row in sql_res:
    sql_user_info.update({row['ip']: row['mac']})

device_ids = sql.select_list("SELECT id FROM device WHERE layer='agg'", 'id')

for device_id in device_ids:

    device = DeviceClass(sql, device_id)
    arp_entries = device.snmpwalk(ARP_OID)

    for arp_entry in arp_entries:
        ip = arp_entry.oid_index.split('.', 1)[-1]
        if ip in sql_user_info:
            new_mac = device.convert_to_hexstr(arp_entry.value)
            old_mac = sql_user_info.get(ip)

            if new_mac != old_mac:
                print(f"Need to update MAC for {ip}: {old_mac} -> {new_mac}")
                query = f"UPDATE user SET mac='{new_mac}' WHERE ip='{ip}'"
                sql.execute_query(query, commit=True)

###

sql.disconnect()