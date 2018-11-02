from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from API.Authentication import Authentication
import time, json

#importing Database
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Database as db

class Devices(Resource):

    @staticmethod
    def computeDeviceId(ip, port):
        return str(abs(hash(ip + str(port))))

    @staticmethod # This method ignore tags
    def createDeviceJSON(device):
        return {
                    "port": device[1],
                    "username": device[2],
                    "ipAddress": device[0],
                    "ne_id": "%s:%d" % (device[0], device[1]), # hash(ipportrowid)te
                    "description": {
                        "contentType": "text",
                        "content": ""
                    },
                    "userProvidedSerialNumber": "",
                    "deviceId": device[4],
                    "serialNumber": "UCS8e9c95bf-a5e0-4657-80c6-%s" % device[4],
                    "hostname": "iox-caf-%s" % (device[4]),
                    "platformVersionDetails": {
                        "caf_version_info": {
                            "build_number": 7,
                            "branch": "r/1.7.0.0",
                            "revision": "0866bf2f310712517dea4a9df2e9030f8e0b1286"
                        },
                        "platform_version_info": {},
                        "caf_version_name": "ARYABHATTA",
                        "platform_version_number": "0",
                        "repo": {
                            "supported_versions": [
                                "1.0"
                            ],
                            "repo_version": "1.0"
                        },
                        "caf_version_number": "1.7.0.7"
                    },
                    "status": "DISCOVERED", #self.devices["iox-caf-%s" % (device[0])]["status"],
                    "errorMessage": "",
                    "useLocalImages": False,
                    "lastHeardTime": device[5],
                    "lostContact": device[6],
                    "tags": [
                    ],
                    "supportedFeature": [
                        #"dhcp_client_id",
                        #"swupdate",
                        #"dhcp_client_id_ipv6",
                        #"local_install",
                        #"layer_reg",
                        #"resize_disk",
                        #"batch_requests",
                        #"static_ipv4",
                        #"reset",
                        #"ztr_requests",
                        #"dual_stack_hybrid",
                        #"error_report",
                        #"docker_app_without_rootfs_tar",
                        #"platform_taillog"
                    ],
                    "apps": [],
                    "capability": {
                        "managementAPIVersion": "2.0",
                        "supportedApps": [
                            "DOCKER",
                            "LXC",
                            "PAAS"
                        ],
                        "nodes": [
                            {
                                "name": "x86_64",
                                "cartridges": [],
                                "cpu": {
                                    "available": 1143,
                                    "total": 1743
                                },
                                "memory": {
                                    "available": 1381,
                                    "total": 1637
                                },
                                "disk": {
                                    "available": 812,
                                    "total": 822
                                },
                                "totalVCPU": 2,
                                "maxVCPUPerApp": 2
                            }
                        ]
                    },
                    "supportedResourceProfiles": [
                        {
                            "default": {
                                "cpuShare": 200,
                                "memoryShare": 64,
                                "vCPU": 1
                            },
                            u"c1\uff0etiny": { # Thank you MongoDB for not managing dots in key name
                                "cpuShare": 100,
                                "memoryShare": 32,
                                "vCPU": 1
                            },
                            u"c1\uff0exlarge": {
                                "cpuShare": 1200,
                                "memoryShare": 256,
                                "vCPU": 1
                            },
                            u"c1\uff0emedium": {
                                "cpuShare": 400,
                                "memoryShare": 128,
                                "vCPU": 1
                            },
                            u"c1\uff0esmall": {
                                "cpuShare": 200,
                                "memoryShare": 64,
                                "vCPU": 1
                            },
                            u"c1\uff0elarge": {
                                "cpuShare": 600,
                                "memoryShare": 256,
                                "vCPU": 1
                            }
                        }
                    ],
                    "networks": [
                        {
                            "networkName": "iox-bridge0",
                            "networkDescription": {
                                "repofolder": "/software/caf/work/network",
                                "external_interface": "VPG0",
                                "name": "iox-bridge0",
                                "mirror_mode": False,
                                "private_route_table": "10",
                                "source_linux_bridge": "svcbr_0",
                                "subnet_mask": None,
                                "gateway_ip": None,
                                "app_ip_map": {},
                                "ip_end": None,
                                "network_type": "bridge",
                                "ip_start": None,
                                "description": " - bridge"
                            }
                        },
                        {
                            "networkName": "iox-nat0",
                            "networkDescription": {
                                "repofolder": "/software/caf/work/network",
                                "external_interface": "VPG0",
                                "name": "iox-nat0",
                                "mirror_mode": False,
                                "private_route_table": "10",
                                "source_linux_bridge": "svcbr_0",
                                "subnet_mask": "255.255.255.224",
                                "gateway_ip": "192.168.10.1",
                                "nat_range_cidr": "192.168.10.0/27",
                                "app_ip_map": {},
                                "ip_end": "192.168.10.30",
                                "network_type": "nat",
                                "ip_start": "192.168.10.2",
                                "description": " - nat"
                            }
                        }
                    ],
                    "usedSerialDevices": [],
                    "availableSerialDevices": [],
                    "availableUsbDevices": [],
                    "usedUsbDevices": [],
                    "_links": {
                        "apps": {
                            "href": "/api/v1/appmgr/devices/2d218045-5fbd-450d-bfff-1a85f385d6de/apps"
                        },
                        "techsupport": {
                            "href": "/api/v1/appmgr/devices/2d218045-5fbd-450d-bfff-1a85f385d6de/techsupport"
                        },
                        "self": {
                            "href": "/api/v1/appmgr/devices/2d218045-5fbd-450d-bfff-1a85f385d6de"
                        },
                        "logs": {
                            "href": "/api/v1/appmgr/devices/2d218045-5fbd-450d-bfff-1a85f385d6de/logs"
                        }
                    },
                    "readonly": False,
                    "ipv6Supported": False
                }
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('x-token-id', location='headers')
        args = parser.parse_args()
        data = request.json #{'port':'8888','ipAddress':device_ip,'username':'t','password':'t'}
        
        if db.checkToken(args["x-token-id"]):
            if data == None or\
                data["ipAddress"] == None or\
                data["port"] == None or\
                data["username"] == None or\
                data["password"] == None:
                return {"description": "ipAddress, port, username or password not defined"}, 401, {"ContentType": "application/json"}

            devid = str(self.computeDeviceId(data["ipAddress"], data["port"]))

            if db.deviceExists(devid):
                return {
                    "code": 1101,
                    "description": "A device with IP address, 10.10.20.51, already exists in the inventory."
                }, 409, {"ContentType": "application/json"}
                
            # Creating a device complete description using a dummy function
            device = [data["ipAddress"], int(data["port"]), data["username"], data["password"], self.computeDeviceId(data["ipAddress"], data["port"]), -1, 1]
            deviceDescription = self.createDeviceJSON(device)
            
            # Adding a password
            deviceDescription["password"] = data["password"] 
            db.addDevice(devid, deviceDescription)
            
            # Removing password before return it to client
            del deviceDescription["password"]
            return deviceDescription, 201, {'ContentType':'application/json'}
        else:
            return self.invalidToken()

    def delete(self, deviceid):
        parser = reqparse.RequestParser()
        parser.add_argument('x-token-id', location='headers')
        args = parser.parse_args()
        if db.checkToken(args["x-token-id"]):
            dev = db.getDevice(deviceid)
            db.deleteDevice(deviceid)
            del dev["_id"]
            return dev, 200, {"Content-Type": "application/json"}

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("limit", type=int)
        parser.add_argument("offset", type=int)
        parser.add_argument("searchByTags")
        parser.add_argument("searchByAnyMatch")
        parser.add_argument('x-token-id', location='headers')
        args = parser.parse_args()
        
        if db.checkToken(args["x-token-id"]):
            data = {"data": []}
            devices = db.getDevices(args["limit"] if args["limit"] != None else 1000, 
                                    args["offset"] if args["offset"] != None else 0,
                                    args["searchByTags"],
                                    args["searchByAnyMatch"])
            
            for device in devices:
                del device["password"] # removing password from the returned HTTP API object
                data["data"].append(device)

            return data, 200, {'ContentType':'application/json'} 
        else:
            return self.invalidToken()
        

    @staticmethod
    def invalidToken():
        return {"code":1703,"description":"Session is invalid or expired"}, 401, {'ContentType':'application/json'} 
