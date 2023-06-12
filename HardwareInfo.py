import logging
import re
import socket
import time
from tkinter import *
from tkinter.ttk import *

import psutil

import EmailService as emServ

hardwarestatus_file_path = "C:/Monitoring Logs/app.log"
logging.basicConfig(filename=hardwarestatus_file_path, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

root = Tk()
root.title("Hardware Monitoring")
root.geometry("600x400")

cpu_label = Label(root, text="CPU-Auslastung: ")
cpu_label.pack()

ram_label = Label(root, text="RAM-Auslastung: ")
ram_label.pack()

drives_label = Label(root, text="Festplattenauslastung: ")
drives_label.pack()

drives_text = Text(root, height=5, width=60, state=DISABLED)
drives_text.pack()

net_label = Label(root, text="Netzwerkauslastung: ")
net_label.pack()

processes_label = Label(root, text="Laufende Prozesse: ")
processes_label.pack()

processes_text = Text(root, height=10, width=60, state=DISABLED)
processes_text.pack()

# Variables to store previous utilization values
prev_cpu_percent = -1
prev_ram_percent = -1
prev_drive_info = ""
prev_net_io = None
prev_processes = []


def send_email_wrapper(email_entry):
    email_address = email_entry.get()
    hostname = socket.gethostname()

    last_line_timestamp = None
    with open(hardwarestatus_file_path, 'r') as file:
        lines = file.readlines()
        if lines:
            last_line = lines[-1]
            timestamp_match = re.search(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', last_line)
            if timestamp_match:
                last_line_timestamp_str = timestamp_match.group(1)
                last_line_timestamp = time.mktime(time.strptime(last_line_timestamp_str, "%Y-%m-%d %H:%M:%S"))

        # Select log entries from the last 60 seconds
    if last_line_timestamp is not None:
        current_time = time.time()
        relevant_lines = []
        for line in lines:
            timestamp_match = re.search(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
            if timestamp_match:
                timestamp_str = timestamp_match.group(1)
                timestamp = time.mktime(time.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"))
                if current_time - timestamp <= 60:
                    relevant_lines.append(line)

        # Join the relevant lines to create the updated file_contents
        file_contents = ''.join(relevant_lines)
    else:
        # If no last line or timestamp found, use the entire file contents
        with open(hardwarestatus_file_path, 'r') as file:
            file_contents = file.read()

    emServ.send_email(email_address, file_contents, hostname)
    if emServ.send_email(email_address, file_contents, hostname) is True:
        return True
    else:
        return False


def emailSendWindow():
    sendWindow = Toplevel(root)
    sendWindow.title("Auslastungsbericht")
    sendWindow.geometry("400x112")
    emailLabel = Label(sendWindow, text="E-Mail Adresse:", anchor="center")
    emailLabel.pack(pady=3)
    emailEntry = Entry(sendWindow, width=50)
    emailEntry.pack(pady=3)
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    def send_email():
        if re.fullmatch(regex, emailEntry.get()):
            send_email_result = send_email_wrapper(emailEntry)
            if send_email_result is True:
                badEmailAddress.pack_forget()
                emailSentError.pack_forget()
                emailSentConformation.pack()
            else:
                badEmailAddress.pack_forget()
                emailSentConformation.pack_forget()
                emailSentError.pack()
        else:
            emailSentError.pack_forget()
            emailSentConformation.pack_forget()
            badEmailAddress.pack(pady=3)

    sendButton = Button(sendWindow, text="Senden", command=send_email)
    sendButton.pack(pady=3)

    badEmailAddress = Label(sendWindow, text="Falsches E-Mail Format! - Richtig: xx@xx.xx", foreground="red")
    emailSentError = Label(sendWindow, text="E-Mail konnte nicht gesendet werden!", foreground="red")
    emailSentConformation = Label(sendWindow, text="E-Mail erfolgreich versendet!", foreground="green")


def update_info():
    global prev_cpu_percent, prev_ram_percent, prev_drive_info, prev_net_io, prev_processes

    cpu_percent = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    drives = psutil.disk_partitions()
    net_io = psutil.net_io_counters()
    processes = psutil.process_iter(["pid", "name"])

    # Update log file
    logging.info("Update")

    # Update CPU utilization
    cpu_message = f"CPU-Auslastung: {cpu_percent}%"
    cpu_label.config(text=cpu_message)
    logging.info(cpu_message)
    prev_cpu_percent = cpu_percent

    # Update RAM utilization
    ram_usage = round(ram.used / 1024 ** 3, 2)  # in Gigabytes
    ram_total = round(ram.total / 1024 ** 3, 2)  # in Gigabytes
    ram_message = f"RAM-Auslastung: {ram_percent}%, Verwendet: {ram_usage} GB, Insgesamt: {ram_total} GB"
    ram_label.config(text=ram_message)
    logging.info(ram_message)
    prev_ram_percent = ram_percent

    # Update drives utilization
    drive_info = ""
    for drive in drives:
        drive_usage = psutil.disk_usage(drive.mountpoint)
        drive_percent = drive_usage.percent
        drive_free = round(drive_usage.free / 1024 ** 3, 2)  # in Gigabytes
        drive_total = round(drive_usage.total / 1024 ** 3, 2)  # in Gigabytes
        drive_message = f"Laufwerk {drive.device}: Auslastung: {drive_percent}%, Frei: {drive_free} GB, Insgesamt: {drive_total} GB\n"
        drive_info += drive_message
        logging.info(drive_message)
    drives_text.config(state=NORMAL)
    drives_text.delete("1.0", END)
    drives_text.insert(END, drive_info)
    drives_text.config(state=DISABLED)
    prev_drive_info = drives

    # Update network utilization
    net_message = f"Netzwerkauslastung: Gesendet: {net_io.bytes_sent} Bytes, Empfangen: {net_io.bytes_recv} Bytes"
    net_label.config(text=net_message)
    logging.info(net_message)
    prev_net_io = net_io

    # Update processes information
    process_info = ""
    for process in processes:
        process_pid = process.info["pid"]
        process_name = process.info["name"]
        process_message = f"Prozess: {process_name} (PID: {process_pid})\n"
        process_info += process_message
        logging.info(process_message)
    processes_text.config(state=NORMAL)
    processes_text.delete("1.0", END)
    processes_text.insert(END, process_info)
    processes_text.config(state=DISABLED)
    prev_processes = list(processes)

    root.after(10000, update_info)  # update every 3 seconds


send_email_button = Button(root, text="Send via Email", command=emailSendWindow)
send_email_button.pack(pady=5)

update_info()

root.mainloop()
