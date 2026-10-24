import customtkinter as ctk
from ui import WorkspaceLauncher


window = ctk.CTk()

app = WorkspaceLauncher(window)

window.mainloop()