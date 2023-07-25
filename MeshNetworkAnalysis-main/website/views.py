from flask import Blueprint, render_template, request, flash
import os
import pyshark
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scapy.utils import PcapWriter
from datetime import datetime
import subprocess
import threading
import time

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST': 
        ip = request.form.get('ip')#Gets the note from the HTML 
        try:
            os.system("systemctl stop NetworkManager")
            os.system("sudo ip link set wlo1 down")
            os.system("sudo iwconfig wlo1 mode ad-hoc")
            os.system("sudo iwconfig wlo1 channel 1")
            os.system("sudo iwconfig wlo1 essid Kavach")
            os.system("sudo iwconfig wlo1 key 1234567890")
            os.system("sudo iwconfig wlo1 ap 12:3E:30:39:BE:A1")
            os.system("sudo ip link set wlo1 up")
            os.system(f"sudo ip addr add {ip}/16 dev wlo1")
            flash('Successfully joined Mesh Network', category='success')
        except:
            flash('Error joining Mesh Network', category='error') 
    return render_template("connect.html")


@views.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'POST': 
        ip = request.form.get('ip')#Gets the note from the HTML
        try: 
            if len(ip.split('.'))!=4:
                raise "Wrong Format"
            l = list(map(lambda x:str(x),list(range(0,10))))
            l.append('.')
            for i in ip:
                if i not in l:
                    raise "Wrong Format"
            os.system(f"ping -c 5 {ip}")
            flash('Successfully sent 5 ICMP packets', category='success')
        except:
            flash('Failed to send ICMP packets', category='error') 
    return render_template("ping.html")


@views.route('/scan', methods=['GET', 'POST'])
def scan():
    try:
        table = []
        if request.method == 'GET':
            os.system("nmcli dev wifi > list.txt")
            with open("list.txt") as w:
                x = w.readlines()
                for i in x:
                    y = i.split()
                    table.append((y[1],y[2],y[8]))   
                table.pop(0)
        return render_template("scan.html",table=table)
    except:
        flash('Cannot Scan with Network Manager off', category='error')
        return render_template("ping.html") 

@views.route('/scan-filt', methods=['GET', 'POST'])
def scanfilt():
    table = []
    os.system("nmcli dev wifi > list.txt")
    with open("list.txt") as w:
        x = w.readlines()
        for i in x:
            y = i.split()
            table.append((y[1],y[2],y[8]))
        table.pop(0)
        table = list(filter(lambda x:x[1]=="Ad-Hoc",table))        
    return render_template("scan.html",table=table)

@views.route('/reset', methods=['GET', 'POST'])
def reset():
    os.system("systemctl start NetworkManager")
    return render_template("connect.html")

@views.route('/analyse', methods=['GET', 'POST'])
def analyse():
    def merge():
        while True:
            try:
                directory = './files'
                source = ""
                for filename in os.listdir(directory):
                    f = os.path.join(directory, filename)
                    if os.path.isfile(f) and f.endswith(".pcap"):
                        r = f.replace(" ","")
                        if r!=f:
                            os.rename(f,r)
                        source+=" "+f
                os.system(f"sudo mergecap -a -w Kavach.pcap {source}")
            except:
                pass
            
            time.sleep(12)
            
    def plot():
        fig,ax = plt.subplots()
        x = [0]
        y = [0]
        ln, = ax.plot(x,y,'-')
        plt.xlabel('Time')
        plt.ylabel('Packet Count')
        plt.title('Network Traffic')
        # print("init")
        def animate(frame):
            name = datetime.now()
            # print("ani")
            capture = pyshark.LiveCapture(interface='wlo1',output_file=f"files/{name}.pcap")
            # print("captured")
            count =0
            capture.sniff(timeout=10)
            # print("cap")
            count = len(capture)
            # print("leng",count)
            ax.clear()
            x.append(x[-1]+10)
            y.append(count)
            ln, = ax.plot(x,y,'-')
            plt.xlabel('Time')
            plt.ylabel('Packet Count')
            plt.title('Network Traffic')
            

        ani = animation.FuncAnimation(fig,animate,interval=1000,repeat=False)
        plt.show()
    threading.Thread(target=merge, daemon=False).start()
    threading.Thread(target=plot, daemon=False).start()
    return render_template("ping.html")
    
