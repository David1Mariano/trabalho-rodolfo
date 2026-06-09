import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime

# =========================
# CONFIGURAÇÃO
# =========================

root = tk.Tk()
root.title("NASA Mission Control")
root.geometry("1200x700")
root.configure(bg="#0B0F1A")

# =========================
# ESTILO
# =========================

style = ttk.Style()
style.theme_use("clam")

TITLE_FONT = ("Consolas", 18, "bold")
DATA_FONT = ("Consolas", 16, "bold")

# =========================
# CABEÇALHO
# =========================

titulo = tk.Label(
    root,
    text="🚀 MISSION CONTROL CENTER",
    bg="#0B0F1A",
    fg="#00E5FF",
    font=TITLE_FONT
)
titulo.pack(pady=10)



main_frame = tk.Frame(root, bg="#0B0F1A")
main_frame.pack(fill="both", expand=True)



def criar_painel(nome, linha, coluna):

    frame = tk.Frame(
        main_frame,
        bg="#111827",
        relief="ridge",
        bd=3
    )

    frame.grid(
        row=linha,
        column=coluna,
        padx=10,
        pady=10,
        sticky="nsew"
    )

    titulo = tk.Label(
        frame,
        text=nome,
        bg="#111827",
        fg="white",
        font=("Consolas", 12, "bold")
    )

    titulo.pack(pady=10)

    valor = tk.Label(
        frame,
        text="---",
        bg="#111827",
        fg="#00FFAA",
        font=DATA_FONT
    )

    valor.pack(pady=15)

    return valor

temp_label = criar_painel("TEMPERATURA", 0, 0)
energia_label = criar_painel("ENERGIA", 0, 1)
com_label = criar_painel("COMUNICAÇÃO", 0, 2)
status_label = criar_painel("STATUS", 0, 3)


log_frame = tk.Frame(
    main_frame,
    bg="#111827",
    relief="ridge",
    bd=3
)

log_frame.grid(
    row=1,
    column=0,
    columnspan=4,
    sticky="nsew",
    padx=10,
    pady=10
)

tk.Label(
    log_frame,
    text="EVENT LOG",
    bg="#111827",
    fg="white",
    font=("Consolas", 12, "bold")
).pack()

log = tk.Text(
    log_frame,
    height=15,
    bg="black",
    fg="#00FF00",
    font=("Consolas", 10)
)

log.pack(fill="both", expand=True)



def registrar(msg):

    horario = datetime.now().strftime("%H:%M:%S")

    log.insert(
        tk.END,
        f"[{horario}] {msg}\n"
    )

    log.see(tk.END)


def analisar():

    temperatura = round(random.uniform(18, 40), 1)
    energia = round(random.uniform(30, 100), 1)
    comunicacao = round(random.uniform(40, 100), 1)

    temp_label.config(text=f"{temperatura} °C")
    energia_label.config(text=f"{energia} %")
    com_label.config(text=f"{comunicacao} %")

    status = "NOMINAL"
    cor = "#00FFAA"

    if temperatura > 32:
        registrar(
            "⚠ ALERTA: Temperatura crítica detectada"
        )
        status = "RISCO"
        cor = "orange"

    if energia < 50:
        registrar(
            "🔋 ALERTA: Energia abaixo do ideal"
        )
        status = "RISCO"
        cor = "orange"

    if comunicacao < 60:
        registrar(
            "📡 ALERTA: Comunicação instável"
        )
        status = "RISCO"
        cor = "orange"

    if temperatura > 36:
        registrar(
            "🚨 EMERGÊNCIA: Superaquecimento"
        )
        status = "CRÍTICO"
        cor = "red"

    status_label.config(
        text=status,
        fg=cor
    )

    root.after(2000, analisar)

# =========================
# GRID RESPONSIVO
# =========================

for i in range(4):
    main_frame.columnconfigure(i, weight=1)

main_frame.rowconfigure(1, weight=1)

registrar("Sistema inicializado")
registrar("Missão Alpha conectada")

analisar()

root.mainloop()