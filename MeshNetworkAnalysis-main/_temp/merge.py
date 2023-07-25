import os
def merge():
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
