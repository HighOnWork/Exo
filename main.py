import tkinter as tk

CAT_RUNNING = "cat_running.gif"
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

gif = timer_running_frames[0]
w, h = gif.width(), gif.height()
canvas = tk.Canvas(pomodoro_window, width=w, height=h, highlightthickness=0, bg="black")
canvas.pack()

# Place the first frame and the text
image_item = canvas.create_image(0, 0, anchor="nw", image=gif)
text_item = canvas.create_text(
    w // 2, h // 2 - 50,
    text="Starting!",
    font=("Arial", 20, "bold"),
    fill="white"
)

def update(ind=0):
    frame = timer_running_frames[ind]
    canvas.itemconfig(image_item, image=frame)
    ind = (ind + 1) % len(timer_running_frames)
    pomodoro_window.after(100, update, ind)

def countdown():
    global Flag
    global STUDY_TIME

    STUDY_TIME -= 1
    minutes = STUDY_TIME // 60
    seconds = STUDY_TIME % 60
    new_study_time = f"{minutes}:{seconds}"
    canvas.itemconfig(text_item, text=new_study_time)
    if STUDY_TIME <= 0:
        if Flag:
            Flag = False
        elif not Flag:
            Flag = True
        if Flag:
            STUDY_TIME = 15
        elif not Flag:
            STUDY_TIME = 5
    pomodoro_window.after(1000, countdown)
def window_setup():
    pomodoro_window.title("Pomodoro Timer")
    pomodoro_window.config(bg="black")
    pomodoro_window.geometry(f"{w}x{h}")

def main():
    window_setup()
    update()
    countdown()
    pomodoro_window.mainloop()

if __name__ == "__main__":
    main()
