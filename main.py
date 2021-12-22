from tkinter import *
from tkinter import filedialog
import tkinter as tk
import customtkinter
from pygame import mixer
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
import os
import time

mixer.init()


class App(tk.Tk):

    NAME = "Music Player"
    WIDTH = 700
    HEIGHT = 500
    PATH = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        super().__init__()

        self.title(App.NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        # image init
        play_image = ImageTk.PhotoImage(Image.open(self.PATH + "/play.png").resize((40, 40)))
        pause_image = ImageTk.PhotoImage(Image.open(self.PATH + "/pause.png").resize((40, 40)))
        stop_image = ImageTk.PhotoImage(Image.open(self.PATH + "/stop.png").resize((40, 40)))

        # frame init
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, height=App.HEIGHT - 40, corner_radius=10)
        self.frame_left.place(relx=0.32, rely=0.5, anchor=tk.E)

        self.frame_right = customtkinter.CTkFrame(master=self, width=420, height=App.HEIGHT - 40, corner_radius=10)
        self.frame_right.place(relx=0.365, rely=0.5, anchor=tk.W)

        # button init
        self.button_1 = customtkinter.CTkButton(master=self.frame_left, image=play_image, text="", command=self.play,
                                                width=60, height=60, border_width=0, corner_radius=8)
        self.button_1.place(relx=0.5, y=120, anchor=tk.CENTER)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left, image=pause_image, text="", command=self.pause,
                                                width=60, height=60, border_width=0, corner_radius=8)
        self.button_2.place(relx=0.5, y=190, anchor=tk.CENTER)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left, image=stop_image, text="", command=self.stop,
                                                width=60, height=60, border_width=0, corner_radius=8)
        self.button_3.place(relx=0.5, y=260, anchor=tk.CENTER)

        # playlist init
        self.playlist = Listbox(self.frame_right, bg="black", fg="white", width=50)
        self.playlist.place(relx=0.5, y=100, anchor=tk.CENTER)

        # menu init
        self.player_menu = Menu(self)
        self.config(menu=self.player_menu)

        self.add_song_menu = Menu(self.player_menu)
        self.player_menu.add_cascade(label="Add Songs", menu=self.add_song_menu)
        self.add_song_menu.add_command(label="Add One Song", command=self.add_song)

        self.music_file = None
        self.playing = False

    def add_song(self):
        song = filedialog.askopenfilename(title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
        self.playlist.insert(END, os.path.basename(song))

    def load(self):
        self.music_file = filedialog.askopenfilename()
        print("Loaded: ", self.music_file)

    def play(self):
        self.music_file = self.playlist.get(ACTIVE)
        mixer.music.load(self.music_file)
        mixer.music.play()
        self.status_bar = Label(self.frame_right, text="", bd=1, relief=GROOVE)
        self.status_bar.place(relx=0.5, y=205, anchor=tk.CENTER)
        self.play_time()

    def pause(self):
        if not self.playing:
            mixer.music.pause()
            self.playing = True
        else:
            mixer.music.unpause()
            self.playing = False

    def play_time(self):
        global time_update
        current_time = mixer.music.get_pos() / 1000
        song_duration = time.strftime("%H:%M:%S", time.gmtime(int(MP3(self.music_file).info.length)))
        converted_time = time.strftime("%H:%M:%S", time.gmtime(current_time))
        final_time = f'{converted_time}/{song_duration}'
        self.status_bar.config(text=final_time)
        time_update = self.status_bar.after(1000, self.play_time)

    def stop(self):
        mixer.music.stop()
        self.status_bar.config(text=f'00:00:00/00:00:00')
        self.status_bar.after_cancel(time_update)

    def startapp(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.startapp()
