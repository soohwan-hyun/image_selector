import os
import tkinter as tk
from tkinter import Tk, Label, BitmapImage, PhotoImage
from PIL import Image, ImageTk

import gluoncv as gcv
from gluoncv.utils import viz
import matplotlib.pyplot as plt
import shutil
from datetime import datetime


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.dir = '/home/shhyun/drv_c/crawler/'
        self.label_dir = '/home/shhyun/PycharmProjects/image_choice/data/'

        self.filelist = []
        self.label_idx = 1
        self.current_idx = 0

        self.net = gcv.model_zoo.get_model('ssd_512_resnet50_v1_custom', classes=[0], pretrained_base=False)
        self.net.load_parameters('./ssd_512_1_mobilenet_pothole_288_0.params')

        for (path, dir, files) in os.walk(self.dir):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ext == '.bmp':
                    self.filelist.append(path+filename)

        self.filelist.sort()

        self.create_widgets()
        self.bind('<s>', self.save_cmd)
        self.bind('<n>', self.next_cmd)
        self.bind('<p>', self.prev_cmd)

    def create_widgets(self):
        self.save = tk.Button(self)
        self.save["text"] = "Save"
        self.save["command"] = self.save_cmd
        self.save.grid(row=0, column=0)

        self.next = tk.Button(self)
        self.next["text"] = "Next"
        self.next["command"] = self.next_cmd
        self.next.grid(row=0, column=1)

        self.prev = tk.Button(self)
        self.prev["text"] = "Prev"
        self.prev["command"] = self.prev_cmd
        self.prev.grid(row=0, column=2)

        x, image = gcv.data.transforms.presets.ssd.load_test(self.filelist[self.current_idx], 512)
        cid, score, bbox = self.net(x)
        ax = viz.plot_bbox(image, bbox[0], score[0], cid[0], class_names="pot")
        plt.rcParams['figure.figsize'] = (10, 10)
        plt.savefig("test.png")
        plt.close()

        self.img1 = Image.open(self.filelist[self.current_idx])
        print(self.filelist[self.current_idx], self.img1)
        self.render1 = ImageTk.PhotoImage(self.img1)
        self.image1 = Label(self, image=self.render1)
        self.image1.grid(row=1, column=0)

        self.img2 = Image.open("test.png")
        self.render2 = ImageTk.PhotoImage(self.img2)
        self.image2 = Label(self, image=self.render2)
        self.image2.grid(row=1, column=2)

        self.label = Label(self, text="{0:05d}".format(self.current_idx) + "/" + "{0:05d}".format(len(self.filelist)))
        self.label.grid(row=2, column=0)

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.grid(row=0, column=3)

    def save_cmd(self, event=None):
        #self.img.save(self.label_dir + "{0:05d}".format(self.label_idx) + "_" + "{0:05d}".format(self.current_idx) + ".jpg")
        filename = self.label_dir + "{0:05d}".format(self.label_idx) + "_" + "{0:05d}".format(self.current_idx) + "_" \
                   + datetime.today().strftime('%Y-%m-%d') + ".jpg"
        shutil.copy(self.filelist[self.current_idx], filename)
        self.label_idx += 1
        self.current_idx += 1
        self.update_display()
        self.update_label()

    def next_cmd(self, event=None):
        if self.current_idx < len(self.filelist):
            self.current_idx += 1
            self.update_display()
            self.update_label()

    def prev_cmd(self, event=None):
        if self.current_idx > 0:
            self.current_idx -= 1
            self.update_display()
            self.update_label()

    def update_display(self):
        if self.current_idx < len(self.filelist):
            x, image = gcv.data.transforms.presets.ssd.load_test(self.filelist[self.current_idx], 512)
            cid, score, bbox = self.net(x)
            ax = viz.plot_bbox(image, bbox[0], score[0], cid[0], class_names="pot")
            plt.rcParams['figure.figsize'] = (10,10)
            plt.savefig("test.png")
            plt.close()

            self.img1 = Image.open(self.filelist[self.current_idx])
            print(self.filelist[self.current_idx], self.img1)
            self.render1 = ImageTk.PhotoImage(self.img1)
            self.image1.configure(image=self.render1)
            self.image1.image = self.render1
            self.image1.update()

            self.img2 = Image.open("test.png")
            self.render2 = ImageTk.PhotoImage(self.img2)
            self.image2.configure(image=self.render2)
            self.image2.image = self.render2
            self.image2.update()

    def update_label(self):
        self.label.configure(text="{0:05d}".format(self.current_idx) + "/" + "{0:05d}".format(len(self.filelist)))
        self.label.update()

root = tk.Tk()
app = Application(master=root)

app.focus_set()
app.mainloop()
