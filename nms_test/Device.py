##!/usr/bin/python
# -*- coding: utf-8 -*-

"""Main class to handle devices"""

from easysnmp import snmp_set, snmp_get, snmp_walk, Session

class DeviceClass:

    DEFAULT_SNMP_COMMUNITY_RO = 'rebrain'
    DEFAULT_SNMP_COMMUNITY_RW = 'rebrainme'
    DEFAULT_SNMP_VERSION = 2
    DEFAULT_SNMP_PORT = 161

    MODEL_OID = '.1.3.6.1.2.1.1.1.0'
    SYSNAME_OID = '.1.3.6.1.2.1.1.5.0'
    SELF_MAC_OID = '.1.3.6.1.2.1.2.2.1.6.1'

    def __init__(self, sql, device_id):
        self.device_id = device_id
        self.sql = sql
        self._info = {}
        self._info_loaded = False


    def info(self):
        """Information about device, returns dictionary"""

        if self._info_loaded:
            return self._info
        else:
            # read from database
            self._info = self._load_info_from_db()
            self._info_loaded = True
            return self._info

    def flush_info_load(self):
        """This function should be executed when device info changed"""
        print(f'device id {self.device_id} executing flush_info_load()')
        self._info_loaded = False

    def _load_info_from_db(self):
        """Actual load info about device from database"""

        query = f"SELECT * FROM device WHERE id={self.device_id}"
        return self.sql.select_row(query) or {}

    # SNMP functions
    def snmpget(self, oid):
        """Execute snmpget and return SNMPVariable object"""
        return snmp_get(oid, hostname=self.info().get('management_ip'), \
                        community=self.info().get('snmp_community_ro') or self.DEFAULT_SNMP_COMMUNITY_RO, \
                        version=self.info().get('snmp_version') or self.DEFAULT_SNMP_VERSION)

    def snmpwalk(self, oid):
        """Execute snmpwalk and return a list of SNMPVariable objects"""
        return snmp_walk(oid, hostname=self.info().get('management_ip'), \
                        community=self.info().get('snmp_community_ro') or self.DEFAULT_SNMP_COMMUNITY_RO, \
                        version=self.info().get('snmp_version') or self.DEFAULT_SNMP_VERSION)

    def snmpset(self, oid, value):
        """Execute snmpset with a given value"""
        return snmp_set(oid, value, hostname=self.info().get('management_ip'), \
                        community=self.info().get('snmp_community_rw') or self.DEFAULT_SNMP_COMMUNITY_RW, \
                        version=self.info().get('snmp_version') or self.DEFAULT_SNMP_VERSION)

    ### END OF SNMP FUNCTIONS

    def convert_to_hexstr(self, unicode_str):
        hex_arr = []
        for b in unicode_str:
            hex_arr.append(("%0.2X" % ord(b)))
        return ':'.join(hex_arr)

    def update_info_from_snmp(self):
        """Read info via snmp and update in DB"""

        item_to_oid_dict = {'model': self.MODEL_OID, 'sysname': self.SYSNAME_OID, 'mac': self.SELF_MAC_OID}

        cur_info = self.info()

        device_ip = cur_info.get('management_ip')

        if not device_ip:
            return 

        query_params = []

        ###  

        for item, oid in item_to_oid_dict.items():

            cur_value = cur_info.get(item)
            snmp_value = self.snmpget(oid).value

            if item == 'model':
                snmp_value = snmp_value.split(' ')[0]
            if item == 'sysname':
                snmp_value = snmp_value.split('.')[0]
            if item == 'mac':
                snmp_value = self.convert_to_hexstr(snmp_value)

            if snmp_value != cur_value:
                if item == 'sysname' and snmp_value != f"SW-{self.device_id}":
                    snmp_value = f"SW-{self.device_id}"
                    # fix sysname on device
                    print(f"Set new sysname {snmp_value}")
                    self.snmpset(oid, snmp_value)

                # update item
                print(f"Need to upadte {item} in db: {cur_value} -> {snmp_value}")
                query_params.append(f"{item}='{snmp_value}'")

                
        ###

        if query_params:
            query_params = ', '.join(query_params)
            query = f"UPDATE device SET {query_params} WHERE id={self.device_id}"
            self.sql.execute_query(query, commit=True)
            self.flush_info_load()

        return self.info() # return updated device info


