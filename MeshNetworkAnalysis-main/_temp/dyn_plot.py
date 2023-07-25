import pyshark
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scapy.utils import PcapWriter
from datetime import datetime
import subprocess

def plot():
	fig,ax = plt.subplots()
	x = [0]
	y = [0]
	ln, = ax.plot(x,y,'-')
	plt.xlabel('Time')
	plt.ylabel('Packet Count')
	plt.title('Network Traffic')
	print("init")
	def animate(frame):
		name = datetime.now()
		print("ani")
		capture = pyshark.LiveCapture(interface='wlo1',output_file=f"files/{name}.pcap")
		print("captured")
		count =0
		capture.sniff(timeout=10)
		print("cap")
		count = len(capture)
		print("leng",count)
		ax.clear()
		x.append(x[-1]+10)
		y.append(count)
		ln, = ax.plot(x,y,'-')
		plt.xlabel('Time')
		plt.ylabel('Packet Count')
		plt.title('Network Traffic')
		

	ani = animation.FuncAnimation(fig,animate,interval=1000,repeat=False)
	plt.show()
	
plot()

# subprocess.call(['open', '-W', '-a', 'Terminal.app', 'python', '--args', 'bb.py'])