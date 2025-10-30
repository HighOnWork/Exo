import tkinter as tk

CAT_RUNNING = "cat_running.gif"
STUDY_TIME = 15

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

label = tk.Label(master=pomodoro_window, bg="black")
label.place(x=0, y=0)

timer_for_work = tk.Label(master=pomodoro_window, text="Starting!", font=("Arial", 20, "bold"), bg=pomodoro_window["bg"])
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
    if STUDY_TIME > 0:
        STUDY_TIME -= 1
        minutes = STUDY_TIME // 60
        seconds = STUDY_TIME % 60
        new_study_time = f"{minutes}:{seconds}"
        timer_for_work.config(text=new_study_time)
        pomodoro_window.after(1000, countdown)
    else:
        print("DONE")

def main():
    window_setup()
    update()
    countdown()
    #DONT ADD ANYTHING BELOW THIS FUNCTION
    pomodoro_window.mainloop()

if __name__ == "__main__":
    main()
