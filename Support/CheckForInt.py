import tkinter as tk
from tkinter import messagebox


def CheckForInt(int_var: tk.IntVar, name: str, from_num: int, to_num: int) -> bool:
    temp = None
    try:
        temp = int_var.get()
    except tk.TclError:
        messagebox.showerror("ERROR", f"请在{name}处输入数字!")
        return False

    if temp < from_num or temp > to_num:
        messagebox.showerror("ERROR", f"请确保在{name}输入的数字\n在{from_num}~{to_num}之间!")
        return False

    return True
