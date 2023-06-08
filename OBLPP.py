import tkinter as tk
import subprocess

def open_business_card_gui():
    subprocess.Popen(["python", "BusinessCardGUI.py"])

root = tk.Tk()

# Create a button to open the BusinessCardGUI.py window
open_business_card_gui_button = tk.Button(root, text="Open Business Card GUI", command=open_business_card_gui)
open_business_card_gui_button.pack()

root.mainloop()