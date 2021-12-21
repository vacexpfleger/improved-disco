from tkinter import *
from tkinter import filedialog
import tkinter as tk
import customtkinter
from pygame import mixer
from PIL import Image, ImageTk
import os
from mutagen.mp3 import MP3
import time


class App(tk.Tk):

    NAME = "Music Player"
    WIDTH = 700
    HEIGHT = 500
    PATH = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title(App.NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        # image init
        load_image = ImageTk.PhotoImage(Image.open(self.PATH + "/load.png").resize((40, 40)))
        play_image = ImageTk.PhotoImage(Image.open(self.PATH + "/play.png").resize((40, 40)))
        pause_image = ImageTk.PhotoImage(Image.open(self.PATH + "/pause.png").resize((40, 40)))

        # frame init
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, height=App.HEIGHT - 40, corner_radius=10)
        self.frame_left.place(relx=0.32, rely=0.5, anchor=tk.E)

        self.frame_right = customtkinter.CTkFrame(master=self, width=420, height=App.HEIGHT - 40, corner_radius=10)
        self.frame_right.place(relx=0.365, rely=0.5, anchor=tk.W)

        # button init
        self.button_1 = customtkinter.CTkButton(master=self.frame_left, image=load_image, text="", command=self.load,
                                                width=60, height=60, border_width=0, corner_radius=8)
        self.button_1.place(relx=0.5, y=50, anchor=tk.CENTER)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left, image=play_image, text="", command=self.play,
                                                width=60, height=60, border_width=0, corner_radius=8)
        self.button_2.place(relx=0.5, y=120, anchor=tk.CENTER)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left, image=pause_image, text="", command=self.pause,
                                                width=60, height=60, border_width=0, corner_radius=8)
        self.button_3.place(relx=0.5, y=190, anchor=tk.CENTER)

        # progress bar init
        self.status_bar = Label(self.frame_right, text="", bd=1, relief=GROOVE)
        self.status_bar.place(relx=0.5, y=50, anchor=tk.CENTER)

        self.music_file = False
        self.playing = False

    def load(self):
        self.music_file = filedialog.askopenfilename()
        print("Loaded: ", self.music_file)

    def play(self):
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            mixer.music.play()
            self.play_time()
            self.playing = False

    def pause(self):
        if not self.playing:
            mixer.music.pause()
            self.playing = True
        else:
            mixer.music.unpause()
            self.playing = False

    def play_time(self):
        current_time = mixer.music.get_pos() / 1000
        song_duration = time.strftime("%H:%M:%S", time.gmtime(int(MP3(self.music_file).info.length)))
        converted_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
        final_time = converted_time + "/" + song_duration
        self.status_bar.config(text=final_time)
        self.status_bar.after(1000, self.play_time)

    def stop(self):
        mixer.music.stop()

    def startapp(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.startapp()
