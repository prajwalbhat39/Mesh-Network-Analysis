import os 
os.system("nmcli dev wifi > list.txt")
l = []
import time 

with open("list.txt") as w:
    x = w.readlines()
    for i in x:
        print(i)
        y = i.split()
        l.append((y[1],y[2],y[8]))
l = list(filter(lambda x:x[1]=="Ad-Hoc",l))
print("Ad-Hoc Networks list: ")
for i in l:
    print(l[0])

# # importing the subprocess module
# import subprocess

# # using the check_output() for having the network term retrieval
# devices = subprocess.check_output(['netsh','wlan','show','network'])

# # decode it to strings
# devices = devices.decode('ascii')
# devices= devices.replace("\r","")

# # displaying the information
# print(devices)