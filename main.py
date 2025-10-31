import tkinter as tk

RESET = False
CAT_RUNNING = "cat_running.gif"
CAT_STOPPED = "cat_resting.gif"
STUDY_TIME = 15

pomodoro_window = tk.Tk()
Flag = True

timer_running_frames = []
i = 0
while True:
    try:
        frame = tk.PhotoImage(file=CAT_RUNNING, format=f"gif -index {i}")
        timer_running_frames.append(frame)
        i += 1
    except tk.TclError:
        break

timer_stopped_frames = []
x = 0
while True:
    try:
        other_frame = tk.PhotoImage(file=CAT_STOPPED, format=f"gif -index {x}")
        timer_stopped_frames.append(other_frame)
        x += 1
    except tk.TclError:
        break

gif = timer_running_frames[0]
w, h = gif.width(), gif.height()
canvas = tk.Canvas(pomodoro_window, width=w, height=h, highlightthickness=0)
canvas.pack()

# Place the first frame and the text
image_item = canvas.create_image(0, 0, anchor="nw", image=gif)
text_item = canvas.create_text(
    w // 2, h // 2 - 50,
    text="Starting!",
    font=("Arial", 20, "bold"),
    fill="white"
)

def running_update(ind=0):
    global RESET
    global Flag
    if RESET:
        ind = 0
        RESET = False
    if Flag:
        frame = timer_running_frames[ind]
        ind = (ind + 1) % len(timer_running_frames)
    elif not Flag:
        frame = timer_stopped_frames[ind]
        ind = (ind + 1) % len(timer_stopped_frames)

    canvas.itemconfig(image_item, image=frame)
    pomodoro_window.after(100, running_update, ind)



def countdown():
    global RESET
    global Flag
    global STUDY_TIME

    STUDY_TIME -= 1
    minutes = STUDY_TIME // 60
    seconds = STUDY_TIME % 60
    new_study_time = f"{minutes}:{seconds}"
    canvas.itemconfig(text_item, text=new_study_time)
    if STUDY_TIME <= 0:
        RESET = True
        Flag = not Flag
        STUDY_TIME = 15 if Flag else 5

    pomodoro_window.after(1000, countdown)
def window_setup():
    pomodoro_window.title("Pomodoro Timer")
    pomodoro_window.config(bg="black")
    pomodoro_window.geometry(f"{w}x{h}")

def main():
    window_setup()
    running_update()
    countdown()
    pomodoro_window.mainloop()

if __name__ == "__main__":
    main()
