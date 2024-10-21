from tkinter import *
from tkinter import messagebox
import ttkbootstrap as tb

window = tb.Window(themename="darkly")
# window.geometry('500x450')
window.iconbitmap('res/pomodoro-logo.ico')

# ---------------------------- CONSTANTS ------------------------------- #
# PINK = "#e2979c"
# RED = "#e7305b"
# GREEN = "#1a0"
# YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
RECORD_PATH = 'res/record.txt'
reps = 0
afterid = tb.StringVar()


# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global reps
    global afterid
    window.after_cancel(afterid)
    label.config(text="Timer", bootstyle="success")
    canvas.itemconfig(timer_text, text="00:00")
    check_mark.config(text="")
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global reps
    reps += 1
    work = WORK_MIN * 60
    short = SHORT_BREAK_MIN * 60
    long = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long)
        messagebox.showerror('Break', 'Take a long break')
        label.config(text="Break", bootstyle="danger")
    elif reps % 2 == 0:
        count_down(short)
        messagebox.showinfo('Break', 'Take a short break')
        label.config(text="Break", bootstyle="warning")
    else:
        count_down(work)
        messagebox.showinfo('Work', 'Get to work')
        label.config(text="Work", bootstyle="success")


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    global reps
    timer = []

    minutes = int(count / 60)
    seconds = count % 60
    timer.append(str((minutes - 24) * - 1))
    timer.append(str((seconds - 60) * - 1))
    print(timer)

    set_high_score(timer)

    if seconds < 10:
        seconds = f"0{seconds}"
    if minutes < 10:
        minutes = f"0{minutes}"

    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    if count > 0:
        global afterid
        afterid = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        mark = ""
        work_sessions = int(reps / 2)
        for i in range(work_sessions):
            mark += "✔"
            check_mark.config(text=mark)


# ---------------------------- Read high score file ---------------------------- #
def get_high_score(filepath):
    try:
        with open(filepath, 'r') as file:
            file = file.readlines()
    except:
        set_high_score(filepath, "")

    return "1:00"


# ---------------------------- Update new high score ---------------------------- #

def set_high_score(content, filepath="res/record.txt"):
    with open(filepath, 'w') as file:
        file.writelines(content)


# ---------------------------- UI SETUP ------------------------------- #
# --------Style Setup------- #
my_style = tb.Style()
my_style.configure('success.TButton', font=("Segoe UI", 18))
my_style.configure('danger.Outline.TButton', font=("Segoe UI", 18))

### ---------- High score Labels --------------- ###
high_score_lbl = tb.Label(text=f"Best lap\n{get_high_score(RECORD_PATH)}", font=("Segoe UI", 10))
high_score_lbl.grid(column=0, row=0, pady=10)

# --------Title------- #
label = tb.Label(text="Timer", font=("Segoe UI", 35, "bold"), bootstyle="success")
label.grid(column=1, row=0, pady=20)

# --------Tomato image------- #
canvas = tb.Canvas(width=200, height=224, highlightthickness=0)
tomato_img = PhotoImage(file="res/tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# --------Start button------- #
button_start = tb.Button(text="Start", command=start_timer, style="success.TButton")
button_start.grid(column=0, row=3, padx=20)

# --------Reset Button------- #
button_reset = tb.Button(text="Reset", command=reset_timer, style="danger.Outline.TButton")
button_reset.grid(column=2, row=3, padx=20)

# --------Check marks setup------- #
check_mark = tb.Label(font=("Segoe UI", 15, "bold"))
check_mark.grid(column=1, row=4, pady=20)

window.mainloop()
