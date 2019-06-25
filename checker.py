import os
import tkinter as tk
from tkinter import Tk, Label, BitmapImage, PhotoImage
from PIL import Image, ImageTk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.dir = '/home/shhyun/notebooks/crawler2/'
        self.label_dir = '/home/shhyun/PycharmProjects/image_choice/data/'

        self.filelist = []
        self.label_idx = 1
        self.current_idx = 0

        for (path, dir, files) in os.walk(self.dir):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ext == '.bmp':
                    self.filelist.append(path+filename)

        self.create_widgets()
        self.bind('<s>', self.save_cmd)
        self.bind('<n>', self.next_cmd)

    def create_widgets(self):
        self.save = tk.Button(self)
        self.save["text"] = "Save"
        self.save["command"] = self.save_cmd
        self.save.pack(side="top")

        self.next = tk.Button(self)
        self.next["text"] = "Next"
        self.next["command"] = self.next_cmd
        self.next.pack(side="top")

        self.img = Image.open(self.filelist[self.current_idx])
        print(self.filelist[self.current_idx], self.img)
        self.current_idx += 1
        self.render = ImageTk.PhotoImage(self.img)
        self.image = Label(self, image=self.render)
        self.image.pack()

        self.label = Label(self, text="{0:05d}".format(self.current_idx) + "/" + "{0:05d}".format(len(self.filelist)))
        self.label.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def save_cmd(self, event=None):
        self.img.save(self.label_dir + "{0:05d}".format(self.label_idx) + "_" + "{0:05d}".format(self.current_idx) + ".jpg")
        self.label_idx += 1
        self.current_idx += 1
        self.update_display()
        self.update_label()

    def next_cmd(self, event=None):
        self.current_idx += 1
        self.update_display()
        self.update_label()

    def update_display(self):
        if self.current_idx < len(self.filelist):
            self.img = Image.open(self.filelist[self.current_idx])
            print(self.filelist[self.current_idx])

            self.render = ImageTk.PhotoImage(self.img)
            self.image.configure(image=self.render)
            self.image.image = self.render
            self.image.update()

    def update_label(self):
        self.label.configure(text="{0:05d}".format(self.current_idx) + "/" + "{0:05d}".format(len(self.filelist)))
        self.label.update()

root = tk.Tk()
app = Application(master=root)

app.focus_set()
app.mainloop()
