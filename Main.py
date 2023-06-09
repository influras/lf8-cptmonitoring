import psutil

import logging
import tkinter as tk

log_file = "C:/Monitoring Logs/app.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# I bims der Kai und ich bin jetzt auch dabei!

def update_info():
    # Löscht die vorherigen Werte in der Konsole

    cpu_percent = psutil.cpu_percent()
    cpu_message = f"CPU-Auslastung: {cpu_percent}%"
    cpu_label.config(text=cpu_message)
    logging.info(cpu_message)

    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    ram_usage = round(ram.used / 10243, 2)  # in Gigabytes
    ram_total = round(ram.total / 10243, 2)  # in Gigabytes
    ram_message = f"RAM-Auslastung: {ram_percent}%, Verwendet: {ram_usage} GB, Insgesamt: {ram_total} GB"
    ram_label.config(text=ram_message)
    logging.info(ram_message)

    drives = psutil.disk_partitions()
    drive_info = ""
    for drive in drives:
        drive_usage = psutil.disk_usage(drive.mountpoint)
        drive_percent = drive_usage.percent
        drive_free = round(drive_usage.free / 10243, 2)  # in Gigabytes
        drive_total = round(drive_usage.total / 10243)  # in Gigabytes
        drive_message = f"Laufwerk {drive.device}: Auslastung: {drive_percent}%, Frei: {drive_free} GB, Insgesamt: {drive_total} GB\n"
        drive_info += drive_message
        logging.info(drive_message)
    drives_text.config(state=tk.NORMAL)
    drives_text.delete("1.0", tk.END)
    drives_text.insert(tk.END, drive_info)
    drives_text.config(state=tk.DISABLED)

    net_io = psutil.net_io_counters()
    net_message = f"Netzwerkauslastung: Gesendet: {net_io.bytes_sent} Bytes, Empfangen: {net_io.bytes_recv} Bytes"
    net_label.config(text=net_message)
    logging.info(net_message)

    processes = psutil.process_iter(["pid", "name"])
    process_info = ""
    for process in processes:
        process_pid = process.info["pid"]
        process_name = process.info["name"]
        process_message = f"Prozess: {process_name} (PID: {process_pid})\n"
        process_info += process_message
        logging.info(process_message)
    processes_text.config(state=tk.NORMAL)
    processes_text.delete("1.0", tk.END)
    processes_text.insert(tk.END, process_info)
    processes_text.config(state=tk.DISABLED)

    root.after(1000, update_info)  # Aktualisiere alle 3 Sekunden


root = tk.Tk()
root.title("Hardware Monitoring")
root.geometry("600x400")

cpu_label = tk.Label(root, text="CPU-Auslastung: ")
cpu_label.pack()

ram_label = tk.Label(root, text="RAM-Auslastung: ")
ram_label.pack()

drives_label = tk.Label(root, text="Festplattenauslastung: ")
drives_label.pack()

drives_text = tk.Text(root, height=5, width=60, state=tk.DISABLED)
drives_text.pack()

net_label = tk.Label(root, text="Netzwerkauslastung: ")
net_label.pack()

processes_label = tk.Label(root, text="Laufende Prozesse: ")
processes_label.pack()

processes_text = tk.Text(root, height=10, width=60, state=tk.DISABLED)
processes_text.pack()

send_email_button = tk.Button(root, text="Send via Email", )
send_email_button.pack(pady=5)

update_info()  # Starte die Aktualisierung der Informationen

root.mainloop()