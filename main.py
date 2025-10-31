import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import io

RESET = False
CAT_RUNNING = "cat_running.gif"
CAT_STOPPED = "cat_resting.gif"
STUDY_TIME = 15

pomodoro_window = tk.Tk()
Flag = True


def load_gif_frames(gif_path):
    """
    Loads all frames from a GIF using Pillow and returns a list of PhotoImage objects.
    This correctly handles optimized GIFs.
    """
    frames = []
    try:
        with Image.open(gif_path) as pil_image:
            # Iterate over each frame in the GIF
            for frame in ImageSequence.Iterator(pil_image):
                # Create a PhotoImage object for each frame.
                # We must keep a reference to this object, so we append it to our list.
                # frame.copy() is important to ensure we have a distinct image for each frame.
                photo_frame = ImageTk.PhotoImage(frame.copy())
                frames.append(photo_frame)
    except FileNotFoundError:
        print(f"Error: GIF file not found at {gif_path}")
        # Create a placeholder frame if file is missing
        placeholder_img = Image.new('RGB', (200, 200), color='grey')
        img_byte_arr = io.BytesIO()
        placeholder_img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        frames.append(tk.PhotoImage(data=img_byte_arr))
    except Exception as e:
        print(f"Error loading GIF {gif_path}: {e}")
        return []

    return frames


# --- Updated Frame Loading ---
# Use the new Pillow-based function to load frames
print(f"Loading {CAT_RUNNING}...")
timer_running_frames = load_gif_frames(CAT_RUNNING)
print(f"Loading {CAT_STOPPED}...")
timer_stopped_frames = load_gif_frames(CAT_STOPPED)
# --- End of Update ---

if not timer_running_frames or not timer_stopped_frames:
    print("Error: Could not load one or both GIF files. Exiting.")
    pomodoro_window.destroy()
    if not timer_running_frames:
        timer_running_frames = load_gif_frames("nonexistent_placeholder_1.gif")
    if not timer_stopped_frames:
        timer_stopped_frames = load_gif_frames("nonexistent_placeholder_2.gif")

if timer_running_frames:
    gif = timer_running_frames[0]
    w, h = gif.width(), gif.height()
else:
    w, h = 200, 200

canvas = tk.Canvas(pomodoro_window, width=w, height=h, highlightthickness=0)
canvas.pack()


image_item = canvas.create_image(0, 0, anchor="nw", image=timer_running_frames[0] if timer_running_frames else None)
text_item = canvas.create_text(
    w // 2, h // 2 - 50,
    text="Starting!",
    font=("Arial", 20, "bold"),
    fill="white"
)


def running_update(ind=0):
    global RESET
    global Flag

    current_frames = timer_running_frames if Flag else timer_stopped_frames

    if not current_frames:
        return

    if RESET:
        ind = 0
        RESET = False

    frame = current_frames[ind]
    ind = (ind + 1) % len(current_frames)

    canvas.itemconfig(image_item, image=frame)
    pomodoro_window.after(100, running_update, ind)


def countdown():
    global RESET
    global Flag
    global STUDY_TIME

    STUDY_TIME -= 1
    minutes = STUDY_TIME // 60
    seconds = STUDY_TIME % 60
    # Format seconds to always have two digits (e.g., 1:05)
    new_study_time = f"{minutes}:{seconds:02d}"

    canvas.itemconfig(text_item, text=new_study_time)

    if STUDY_TIME <= 0:
        RESET = True
        Flag = not Flag
        if Flag:

            STUDY_TIME = 15
            print("Time for a study session!")
        else:

            STUDY_TIME = 5
            print("Time for a break!")

    pomodoro_window.after(1000, countdown)


def window_setup():
    pomodoro_window.title("Pomodoro Timer")
    pomodoro_window.config(bg="black")

    pomodoro_window.geometry(f"{w}x{h}")


def main():
    window_setup()

    if timer_running_frames and timer_stopped_frames:
        running_update()
        countdown()
        pomodoro_window.mainloop()
    else:
        print("Could not start app: essential GIF files are missing.")

        canvas.itemconfig(text_item, text=f"Error: Missing GIF files.\n{CAT_RUNNING}\n{CAT_STOPPED}", fill="red",
                          font=("Arial", 12, "bold"))
        pomodoro_window.mainloop()


if __name__ == "__main__":
    main()
