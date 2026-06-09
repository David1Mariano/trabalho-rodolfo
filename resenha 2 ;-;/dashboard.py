import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sqlite3
from simulator import generate_telemetry
from database import save_telemetry
from mission_statistics import mission_statistics
from report_generator import generate_report

class Dashboard:

    def __init__(self, root):

        self.root = root

        root.title("NASA Mission Control")
        root.geometry("1200x700")
        root.configure(bg="#0B0F1A")

        self.create_widgets()

        self.create_graphs()

        self.update_dashboard()

    def generate_pdf(self):

        generate_report()

        self.log_event(
            "📄 PDF REPORT GENERATED"
        )

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="🚀 NASA MISSION CONTROL CENTER",
            bg="#0B0F1A",
            fg="#00E5FF",
            font=("Consolas", 22, "bold")
        )
    
        title.pack(pady=10)

        self.info_frame = tk.Frame(
            self.root,
            bg="#0B0F1A"
        )
        self.report_button = tk.Button(
            self.root,
            text="📄 Generate Mission Report",
            font=("Consolas", 12, "bold"),
            bg="#00E5FF",
            command=self.generate_pdf
        )

        self.report_button.pack(
            pady=10
        )
        self.info_frame.pack(pady=20)

        self.temp_label = self.create_card(
            "TEMPERATURE",
            0
        )

        self.energy_label = self.create_card(
            "ENERGY",
            1
        )

        self.comm_label = self.create_card(
            "COMMUNICATION",
            2
        )

        self.status_label = self.create_card(
            "STATUS",
            3
        )

        log_title = tk.Label(
            self.root,
            text="MISSION LOG",
            bg="#0B0F1A",
            fg="white",
            font=("Consolas", 14, "bold")
        )

        log_title.pack()

        self.log = tk.Text(
            self.root,
            height=15,
            bg="black",
            fg="#00FF00",
            font=("Consolas", 10)
        )

        self.log.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.stats_frame = tk.Frame(
            self.root,
            bg="#111827",
            bd=3,
            relief="ridge"
        )

        self.stats_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.stats_label = tk.Label(
            self.stats_frame,
            text="Waiting for statistics...",
            bg="#111827",
            fg="white",
            justify="left",
            font=("Consolas", 11)
        )

        self.stats_label.pack(
            padx=10,
            pady=10,
            anchor="w"
        )

    def create_card(self, title, column):

        frame = tk.Frame(
            self.info_frame,
            bg="#111827",
            bd=3,
            relief="ridge"
        )

        frame.grid(
            row=0,
            column=column,
            padx=15
        )

        tk.Label(
            frame,
            text=title,
            bg="#111827",
            fg="white",
            font=("Consolas", 12, "bold")
        ).pack(padx=30, pady=10)

        value = tk.Label(
            frame,
            text="---",
            bg="#111827",
            fg="#00FFAA",
            font=("Consolas", 18, "bold")
        )

        value.pack(pady=15)

        return value

    def log_event(self, message):

        self.log.insert(
            tk.END,
            message + "\n"
        )

        self.log.see(tk.END)

    def update_dashboard(self):

        telemetry = generate_telemetry()
        save_telemetry(
            telemetry["temperature"],
            telemetry["energy"],
            telemetry["communication"],
            telemetry["status"]
        )

        self.temp_label.config(
            text=f"{telemetry['temperature']} °C"
        )

        self.energy_label.config(
            text=f"{telemetry['energy']} %"
        )

        self.comm_label.config(
            text=f"{telemetry['communication']} %"
        )

        self.status_label.config(
            text=telemetry["status"]
        )

        if telemetry["status"] == "CRITICAL":

            self.status_label.config(
                fg="red"
            )

            self.log_event(
                "🚨 CRITICAL TEMPERATURE DETECTED"
            )

        elif telemetry["status"] == "WARNING":

            self.status_label.config(
                fg="orange"
            )

            self.log_event(
                "⚠ TEMPERATURE ABOVE NORMAL"
            )

        else:

            self.status_label.config(
                fg="#00FFAA"
            )
        self.update_statistics()
        self.update_graphs()
        self.root.after(
            2000,
            self.update_dashboard
        )

    def create_graphs(self):
        self.graph_frame = tk.Frame(
            self.root,
            bg="#0B0F1A"
        )

        self.graph_frame.pack(
            fill="both",
            expand=True,
            padx=20
        )

        self.fig = Figure(
            figsize=(10,4),
            dpi=100
        )

        self.ax_temp = self.fig.add_subplot(121)
        self.ax_energy = self.fig.add_subplot(122)

        self.canvas = FigureCanvasTkAgg(
            self.fig,
            master=self.graph_frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    def update_graphs(self):
        conn = sqlite3.connect(
            "mission.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id,
                   temperature,
                   energy
            FROM telemetry
            ORDER BY id DESC
            LIMIT 20
            """)

        rows = cursor.fetchall()

        conn.close()

        rows.reverse()

        ids = [r[0] for r in rows]
        temps = [r[1] for r in rows]

        energies = [r[2] for r in rows]             
        self.ax_temp.clear()
        self.ax_energy.clear()
        self.ax_temp.plot(
            ids,
            temps,
            marker="o",
            color="#FF5733"
        )
        self.ax_temp.set_title(
            "Temperature Over Time"
        )
        self.ax_temp.set_xlabel(
            "Reading Number"
        )
        self.ax_temp.set_ylabel(
            "Temperature (°C)"
        )
        self.ax_temp.grid(
            True,
            linestyle="--",
            alpha=0.5
        )
        self.ax_energy.plot(
            ids,
            energies,
            marker="o",
            color="#33C1FF"
        )
        self.ax_energy.set_title(
            "Energy Over Time"
        )
        self.ax_energy.set_xlabel(
            "Reading Number"
        )
        self.ax_energy.set_ylabel(
            "Energy (%)"
        )
        self.ax_energy.grid(
            True,
            linestyle="--",
            alpha=0.5
        )
        self.fig.tight_layout()
        self.canvas.draw()
        
    def update_statistics(self):

        stats = mission_statistics()

        temp = stats["temperature"]

        text = f"""
LIVE STATISTICS

Mean: {temp['mean']}
Median: {temp['median']}
Std Dev: {temp['std_dev']}
CV: {temp['cv']}%

Q1: {temp['q1']}
Q2: {temp['q2']}
Q3: {temp['q3']}
"""

        self.stats_label.config(
            text=text
        )