from database import create_database
from dashboard import Dashboard

import tkinter as tk


create_database()

root = tk.Tk()

Dashboard(root)

root.mainloop()