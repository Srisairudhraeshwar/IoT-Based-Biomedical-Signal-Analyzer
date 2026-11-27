import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time

class BiomedicalDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("IoT Biomedical Signal Analyzer")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        self.ser = None
        self.is_running = False

        # --- Connection Frame ---
        conn_frame = tk.Frame(root, pady=15)
        conn_frame.pack(fill="x", padx=20)

        tk.Label(conn_frame, text="ESP32 Port:", font=("Arial", 11, "bold")).pack(anchor="w")

        input_row = tk.Frame(conn_frame, pady=5)
        input_row.pack(fill="x")

        self.port_entry = tk.Entry(input_row, width=18, font=("Arial", 11))
        self.port_entry.insert(0, "COM3")
        self.port_entry.pack(side="left", padx=(0, 10))

        self.connect_btn = tk.Button(input_row, text="Connect", width=10, command=self.toggle_connection, bg="#e1e4e8")
        self.connect_btn.pack(side="left")

        self.status_lbl = tk.Label(input_row, text="Status: Disconnected", fg="red", font=("Arial", 10))
        self.status_lbl.pack(side="right")

        # --- Telemetry Display Frame ---
        data_frame = tk.LabelFrame(root, text=" Live Sensor Telemetry ", font=("Arial", 11, "bold"), padx=15, pady=15)
        data_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.ecg_label = tk.Label(data_frame, text="ECG Signal Value: --", font=("Consolas", 12))
        self.ecg_label.pack(anchor="w", pady=5)

        self.ir_label = tk.Label(data_frame, text="Optical IR Value (SpO2/BPM): --", font=("Consolas", 12))
        self.ir_label.pack(anchor="w", pady=5)

        self.lead_status = tk.Label(data_frame, text="Sensor State: Waiting for connection...", fg="blue", font=("Arial", 11, "italic"))
        self.lead_status.pack(anchor="w", pady=10)

    def toggle_connection(self):
        if not self.is_running:
            port = self.port_entry.get().strip()
            try:
                self.ser = serial.Serial(port, 115200, timeout=1)
                time.sleep(2)
                self.is_running = True
                self.connect_btn.config(text="Disconnect", bg="#ffcccc")
                self.status_lbl.config(text="Status: Connected", fg="green")
                
                # Start background thread to read serial data
                self.thread = threading.Thread(target=self.read_serial_data, daemon=True)
                self.thread.start()
            except Exception as e:
                messagebox.showerror("Connection Error", f"Could not connect to {port}:\n{e}")
        else:
            self.is_running = False
            if self.ser and self.ser.is_open:
                self.ser.close()
            self.connect_btn.config(text="Connect", bg="#e1e4e8")
            self.status_lbl.config(text="Status: Disconnected", fg="red")
            self.lead_status.config(text="Sensor State: Disconnected", fg="blue")

    def read_serial_data(self):
        while self.is_running:
            if self.ser and self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if "ECG_STATUS" in line:
                        self.root.after(0, lambda: self.lead_status.config(text=f"State: Leads Disconnected", fg="orange"))
                    elif "ECG:" in line and "IR:" in line:
                        parts = line.split(',')
                        ecg_val = parts[0].split(':')[1]
                        ir_val = parts[1].split(':')[1]
                        
                        self.root.after(0, lambda e=ecg_val, i=ir_val: self.update_display(e, i))
                except Exception:
                    pass

    def update_display(self, ecg, ir):
        self.ecg_label.config(text=f"ECG Signal Value: {ecg}")
        self.ir_label.config(text=f"Optical IR Value (SpO2/BPM): {ir}")
        self.lead_status.config(text="Sensor State: Streaming Live Data", fg="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = BiomedicalDashboard(root)
    root.mainloop()
