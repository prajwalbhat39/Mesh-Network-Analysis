import os
import tkinter as tk

def scan_for_networks():
    os.system("nmcli dev wifi > list.txt")
    network_list = []
    with open("list.txt") as w:
        wifi_list = w.readlines()
        for i in wifi_list:
            y = i.split()
            if len(y) > 8 and y[1] != "SSID" and y[2] != "MODE" and y[8] != "--":
                ssid = y[1]
                mode = y[2]
                frequency = y[8]
                network_list.append((ssid, mode, frequency))
    return network_list

def display_all_networks():
    network_list = scan_for_networks()
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "All Networks list:\n")
    if len(network_list) == 0:
        result_text.insert(tk.END, "No networks found.")
    else:
        for ssid, mode, frequency in network_list:
            result_text.insert(tk.END, f"SSID: {ssid}\nMode: {mode}\nFrequency: {frequency}\n\n")
    filter_button.config(text="Filter Ad-Hoc", command=display_adhoc_networks)

def display_adhoc_networks():
    network_list = scan_for_networks()
    adhoc_list = list(filter(lambda x:x[1]=="Ad-Hoc", network_list))
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Ad-Hoc Networks list:\n")
    if len(adhoc_list) == 0:
        result_text.insert(tk.END, "No Ad-Hoc networks found.")
    else:
        for ssid, mode, frequency in adhoc_list:
            result_text.insert(tk.END, f"SSID: {ssid}\nMode: {mode}\nFrequency: {frequency}\n\n")
    filter_button.config(text="Show All Networks", command=display_all_networks)

# Create the main window
root = tk.Tk()
root.title("Network Scanner")

# Create and place the widgets
filter_button = tk.Button(root, text="Filter Ad-Hoc", command=display_adhoc_networks)
filter_button.pack()

result_text = tk.Text(root)
result_text.pack()

# Start the event loop
root.mainloop()
