import re
import subprocess
import sys
import time

import usb.core
import usb.util


class Power:
    def __init__(self, sel: str, port_str: str):
        self.dev = self._get_device_by_selection(sel)
        self.ports = self._get_ports_by_string(port_str)

    def off(self):
        reqType = (0x01 << 5) | 0x03
        bReq = 0x01
        wVal = (1 << 3)
        # wIdx = self.port

        self._transfer(self.dev, reqType, bReq, wVal)


    def on(self):
        reqType = (0x01 << 5) | 0x03
        bReq = 0x03
        wVal = (1 << 3)
        # wIdx = self.port

        self._transfer(self.dev, reqType, bReq, wVal)


    def cycle(self):
        self.off()
        time.sleep(3)
        self.on()


    def _get_device_by_selection(self, sel: str) -> usb.core.Device:
        if ':' in sel:
            return self._get_device_by_ids(sel)
        else:
            return self._get_device_by_keyword(sel)

    def _get_device_by_keyword(self, dev_kw: str):
        kw = bytes(dev_kw.encode())

        device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$",
                               re.I)
        df = subprocess.check_output("lsusb")
        devices = []
        for i in df.split(b'\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                    devices.append(dinfo)

        for device in devices:
            if kw in device['tag']:
                vendor_id = device['id'].split(b':')[0].decode("utf-8")
                product_id = device['id'].split(b':')[1].decode("utf-8")
                return self._get_device_by_ids(vendor_id + ':' + product_id)
            
        raise usb.core.USBError('Device not found')

    def _get_device_by_ids(self, sel: str):
        try:
            vendor_id = sel.split(':')[0]
            product_id = sel.split(':')[1]
            vendor_id = int(vendor_id, 16)
            product_id = int(product_id, 16)
        except ValueError as e:
            print(e)
            sys.exit(1)

        try:
            dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)
        except usb.core.USBError as e:
            print(e)
            sys.exit(1)

        if dev is None:
            print('Device not found')
            sys.exit(1)
        return dev

    def _get_ports_by_string(self, port_str: str) -> set:
        port_str = port_str.replace(' ', '')
        ports = set()
        try:
            for port in port_str.split(','):
                if '-' in port:
                    start = int(port.split('-')[0])
                    end = int(port.split('-')[1])
                    for i in range(start, end + 1):
                        ports.add(i)
                else:
                    ports.add(int(port))
            return ports
        except Exception as e:
            print(e)
            sys.exit(1)


    def _transfer(self, dev, reqType, bReq, wVal):
        for wIdx in self.ports:
            try:
                dev.ctrl_transfer(reqType, bReq, wVal, wIdx, [])
            except usb.core.USBError as e:
                print(e, f'[reqType:{reqType}, bReq:{bReq}, wVal:{wVal}, wIdx:{wIdx}]')
            except AttributeError as e:
                print(e)
                sys.exit(1)
