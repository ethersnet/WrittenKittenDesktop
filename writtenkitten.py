import keyboard
import threading
import rnd_cat
import math

from tkinter import *
from PIL import ImageTk, Image

class KittenCounter:
    def __init__(self):
        self.total_word_count = 0
        self.limit_word_count = 0
        self.kitten_limit = 100
        
        #with Image.open('loading.gif') as im:
        #    self.current_loading_frame = im.n_frames
        #    for i in range(self.current_loading_frame):
        #        im.seek(i)
        #        im.save('assets/loading_{}.png'.format(i))
        
        self.current_loading_frame = 0
        self.loading_frames = 11


    def get_main_blurb(self):
        return "You've written " + str(self.total_word_count) + " words!"

    def get_remains_blurb(self):
        return str(self.kitten_limit - self.limit_word_count) + " words until next kitten."

    def update_count(self):
        self.total_word_count += 1
        self.limit_word_count += 1

        if (self.limit_word_count == self.kitten_limit):
            self.limit_word_count = 0
            return True
        
        return False
    
    def update_kitten_file(self):
        rnd_cat.cat(filename='assets/cat', format='jpg')
    
    def resize_kitten(self, img):
        width, height = img.size

        if (height < width):
            ratio = width / height
            new_height = app_height
            new_width = math.floor(ratio * new_height)
        else:
            ratio = height / width
            new_width = app_width
            new_height = math.floor(ratio * new_width)

        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def get_kitten(self):
        img = Image.open("assets/cat.jpg")
        return self.resize_kitten(img)
        
    
    def get_load_kitten(self):
        img = Image.open("assets/loading_"+str(self.current_loading_frame)+".png")

        self.current_loading_frame += 1

        if self.current_loading_frame > self.loading_frames:
            self.current_loading_frame = 0

        return self.resize_kitten(img)


def space_press():
    while True:
        key_event = keyboard.read_event()
        key = key_event.name
        event = key_event.event_type
        if (key == "space" and event == "up"):
            show_cat = cat_count.update_count()
            main_lbl.config(text=cat_count.get_main_blurb())
            remains_lbl.config(text=cat_count.get_remains_blurb())

            if (show_cat):
                cat_thread = threading.Thread(target=update_cat_image)
                cat_thread.start()
                

def update_cat_image():
    stop = threading.Event()

    load_thread = threading.Thread(target=loading_animation, args=(stop,))
    load_thread.start()

    cat_count.update_kitten_file()

    stop.set()

    tk_img = ImageTk.PhotoImage(cat_count.get_kitten())
    cat_lbl.config(image=tk_img)
    cat_lbl.image = tk_img

def loading_animation(stop):
    while not stop.is_set():
        tk_img = ImageTk.PhotoImage(cat_count.get_load_kitten())
        cat_lbl.configure(image=tk_img)
        cat_lbl.image = tk_img

root = Tk()
app_width = app_height = 500
root.geometry(str(app_width)+"x"+str(app_height))
root.title("Written Kitten App")

cat_count = KittenCounter()

main_lbl = Label(root, text = cat_count.get_main_blurb())
main_lbl.pack()

remains_lbl = Label(root, text = cat_count.get_remains_blurb())
remains_lbl.pack()

tk_img = ImageTk.PhotoImage(cat_count.get_kitten())
cat_lbl = Label(root, image = tk_img)
cat_lbl.image = tk_img
cat_lbl.pack()


thread = threading.Thread(target=space_press, daemon=True)
thread.start()

root.mainloop()