import tkinter as tk

CAT_RUNNING = "cat_running.gif"

pomodoro_window = tk.Tk()

timer_running_frames = []
i = 0
while True:
    try:
        frame = tk.PhotoImage(file=CAT_RUNNING, format=f"gif -index {i}")
        timer_running_frames.append(frame)
        i += 1
    except tk.TclError:
        break

label = tk.Label(pomodoro_window, bg="black")
label.place(x=0, y=0)

timer_for_work = tk.Label(master=pomodoro_window, text="Starting!")
timer_for_work.pack()

def update(ind=0):
    frame = timer_running_frames[ind]
    label.configure(image=frame)
    ind = (ind + 1) % len(timer_running_frames)
    pomodoro_window.after(100, update, ind)

def window_setup():
    gif = tk.PhotoImage(file=CAT_RUNNING, format="gif -index 0")
    w = gif.width()
    h = gif.height()
    pomodoro_window.title("Pomodoro Timer")
    pomodoro_window.config(bg="black")
    pomodoro_window.geometry(f"{w}x{h}")

def countdown():
    global STUDY_TIME
    STUDY_TIME -=1
    print(STUDY_TIME)
    time.sleep(1)


def main():
    window_setup()
    update()
    countdown()
    #DONT ADD ANYTHING BELOW THIS FUNCTION
    pomodoro_window.mainloop()

if __name__ == "__main__":
    main()
