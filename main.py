# coding=utf-8

import base64
import requests
import time
import sys
import traceback
import json
import re

################
#    CONFIG    #
################

# Detailed config about ssr client see
# https://github.com/shadowsocksrr/shadowsocks-rss/wiki/config.json

# Update Interval (seconds)
updateInterval = 1800

# Subscribe Address
# Format: [["config_file_prefix1", "subscribe_address1"], ["config_file_prefix2", "subscribe_address2"]]
subscription = [["test", "https://raw.githubusercontent.com/erguotou520/electron-ssr/redesign/docs/assets/subscribe.txt"],
              ["config_file_prefix1", "https://subscribe_address1"],
              ["config_file_prefix2", "https://subscribe_address2"]]

# Config File
config_file = "config.json"

# User-Agent
userAgent = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"

# Keywords
# use ',' to split
enable_filter = False
keywords = ""

# Local Port
local_port = 1080

# Speed limit for each connection
# 0 to be unlimited
speed_limit_per_con = 0

# Speed limit for each user
# 0 to be unlimited
speed_limit_per_user = 0

# TCP timeout (seconds)
timeout = 120

# UDP timeout (seconds)
udp_timeout = 60

# IPv6 prior
dns_ipv6 = False

# Display connection verbose info
connect_verbose_info = 0

# Redirect
redirect = ""

# TCP fast open
fast_open = False

# Log Export
exportLog = False

# Log Export File
exportLogfile = ""

# Show error traceback
showTraceback = False

# Debug Switch
isDebug = False

# Request timeout
request_timeout = 4


class Server:
    def __init__(self, server, server_port, password, method, protocol, protocol_param, obfs, obfs_param):
        self.server = server
        self.server_ipv6 = "::"
        self.server_port = server_port
        self.local_address = "127.0.0.1"
        self.local_port = local_port

        self.password = password
        self.method = method
        self.protocol = protocol
        self.protocol_param = protocol_param
        self.obfs = obfs
        self.obfs_param = obfs_param
        self.speed_limit_per_con = speed_limit_per_con
        self.speed_limit_per_user = speed_limit_per_user

        self.additional_ports = {}
        self.additional_ports_only = False
        self.timeout = timeout
        self.udp_timeout = udp_timeout
        self.dns_ipv6 = dns_ipv6
        self.connect_verbose_info = connect_verbose_info
        self.redirect = redirect
        self.fast_open = fast_open

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)


def print_log(content):
    print(time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time())) + content)
    sys.stdout.flush()
    if exportLog:
        f_log = open(exportLogfile, "a")
        f_log.write(time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time())) + str(content) + '\n')
        f_log.close()
    return


if __name__ == "__main__":
    if enable_filter:
        keywords = keywords.split(',')
        for i in range(len(keywords)):
            keywords[i] = keywords[i].strip()
        print_log("Apply filters: " + str(keywords))

    headers = {
        "User-Agent": userAgent
    }
    while (True):
        loaded_counter = 0
        for k in range(len(subscription)):
            try:
                servers = []
                subscribeAddress = subscription[k][1]
                if not isDebug:
                    # fetch data
                    subscribeContent = requests.get(subscribeAddress, headers=headers, timeout=request_timeout)

                    # convert data type
                    encodeContent = str(subscribeContent.text).strip()
                else:
                    encodeContent = "c3NyOi8vTVRJM0xqQXVNQzR4T2pFeU16UTZZWFYwYUY5aFpYTXhNamhmYldRMU9tRmxjeTB4TWpndFkyWmlP" \
                                    "blJzY3pFdU1sOTBhV05yWlhSZllYVjBhRHBaVjBab1dXMUthUzhfYjJKbWMzQmhjbUZ0UFZsdVNteFpWM1F6" \
                                    "V1ZSRmVFeHRNWFphVVNaeVpXMWhjbXR6UFRWeVYwdzJTeTFXTlV4cGREVndZVWdtWjNKdmRYQTlaRWRXZW1S" \
                                    "Qg0Kc3NyOi8vTVRreUxqRTJPQzR4TURBdU1UbzRPRGc0T205eWFXZHBianBoWlhNdE1qVTJMV05tWWpwd2JH" \
                                    "RnBianBrUjFaNlpFRXZQMmR5YjNWd1BXUkhWbnBrUVE"

                decodeContent = base64.urlsafe_b64decode(encodeContent + "=" * ((4 - len(encodeContent) % 4) % 4))

                # convert data type
                decodeText = decodeContent.decode("ascii")

                # split data
                decodeArray = decodeText.split('\n')

                for i in range(len(decodeArray)):
                    decodeArray[i] = str(decodeArray[i].replace("ssr://", "", 1)).strip()

                for i in range(len(decodeArray)):
                    # ignore blank line
                    if len(decodeArray[i]) == 0:
                        continue

                    try:
                        decodeArray[i] += (((4 - len(decodeArray[i]) % 4)) % 4) * "="
                        if isDebug:
                            print_log(decodeArray[i])
                            print_log(base64.urlsafe_b64decode(decodeArray[i].encode("utf-8")).decode("utf-8"))
                        decodeArray[i] = base64.urlsafe_b64decode(decodeArray[i].encode("utf-8")).decode("utf-8").split(":")
                    except:
                        traceback.print_exc()
                        continue

                    if isDebug:
                        print_log(str(decodeArray[i]))
                    server = decodeArray[i][0]

                    try:
                        if isDebug:
                            print_log("server = " + server)
                        server_port = int(decodeArray[i][1])
                        if isDebug:
                            print_log("server_port = " + str(server_port))
                        password = base64.urlsafe_b64decode(decodeArray[i][5].split("/?")[0] + "=" * (
                                (4 - (len(decodeArray[i][5].split("/?")[0]) % 4)) % 4)).decode("utf-8")
                        if isDebug:
                            print_log("password = " + password)
                        method = decodeArray[i][3]
                        if isDebug:
                            print_log("method = " + method)
                        protocol = decodeArray[i][2]
                        if isDebug:
                            print_log("protocol = " + protocol)

                        if decodeArray[i][5].find("protoparam") == -1 or len(re.findall(r"protoparam=([a-zA-Z0-9\-]+)&", decodeArray[i][5])) == 0:
                            protocol_param = ""
                        else:
                            protocol_param = base64.urlsafe_b64decode(
                                re.findall(r"protoparam=([a-zA-Z0-9\-]+)&", decodeArray[i][5])[0]).decode("utf-8")
                        if isDebug:
                            print_log("protocol_param = " + protocol_param)
                        obfs = decodeArray[i][4]
                        if isDebug:
                            print_log("obfs = " + obfs)
                        if decodeArray[i][5].find("obfsparam") == -1 or len(re.findall(r"obfsparam=([a-zA-Z0-9\-]+)&", decodeArray[i][5])) == 0:
                            obfs_param = ""
                        else:
                            obfs_param = base64.urlsafe_b64decode(
                                str(re.findall(r"obfsparam=([a-zA-Z0-9\-]+)&", decodeArray[i][5])[0]) + "=" * ((4 - len(
                                    str(re.findall(r"obfsparam=([a-zA-Z0-9\-]+)&", decodeArray[i][5])[0]))) % 4)).decode(
                                "utf-8")
                        if isDebug:
                            print_log("obfs_param = " + obfs_param)

                        if decodeArray[i][5].find("remarks") == -1 or len(re.findall(r"remarks=([a-zA-Z0-9\\\-.:\s]+)", decodeArray[i][5])) == 0:
                            remarks = ""
                        else:
                            remarks = base64.urlsafe_b64decode(
                                re.findall(r"remarks=([a-zA-Z0-9\\\-\.:\s\_]+)", decodeArray[i][5])[0] + "=" * (4 - len(
                                    str(re.findall(r"remarks=([a-zA-Z0-9\\\-\.\s\_]+)", decodeArray[i][5])[0])) % 4)).decode(
                                "utf-8")
                        if isDebug:
                            print_log("remarks = " + remarks)
                        if decodeArray[i][5].find("group") == -1 or len(re.findall(r"group=([a-zA-Z0-9\\\-\.:\s\_]+)", decodeArray[i][5])) == 0:
                            group = ""
                        else:
                            group = base64.urlsafe_b64decode(
                                str(re.findall(r"group=([a-zA-Z0-9\\\-\.:\s\_]+)", decodeArray[i][5])[0]) + "=" * ((4 - (len(
                                    str(re.findall(r"group=([a-zA-Z0-9\\\-\.:\s\_]+)", decodeArray[i][5])[0])) % 4)) % 4)).decode(
                                "utf-8")
                        if isDebug:
                            print_log("group = " + group)

                        server = Server(server, server_port, password, method, protocol, protocol_param, obfs, obfs_param)
                        # print(server.toJSON())

                        if enable_filter:
                            for j in range(len(keywords)):
                                if not remarks.find(keywords[j]) == -1:
                                    servers.append(server)
                                    print_log("Loaded server #" + str(loaded_counter) + "\t [" + remarks + "]")
                                    loaded_counter += 1
                                    break

                            if not server in servers:
                                print_log("Reject server \t [" + remarks + "]")
                        else:
                            servers.append(server)
                            print_log("Loaded server #" + str(loaded_counter) + "\t [" + remarks + "]")
                            loaded_counter += 1
                    except:
                        traceback.print_exc()
                        print_log("#" + str(i) + " server resolved failed.")
            except Exception as e:
                if showTraceback:
                    traceback.print_exc()
                print_log("Failed fetch subscription page - " + subscribeAddress)

            for i in range(len(servers)):
                file = open(subscription[k][0] + "_" + config_file + str(i), "w")
                file.write(servers[i].toJSON())
                file.close()

        print_log("Finished.")
        if isDebug:
            break
        time.sleep(updateInterval)