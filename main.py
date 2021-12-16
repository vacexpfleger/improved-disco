from tkinter import *
from tkinter import filedialog
import customtkinter
import tkinter as tk
from pygame import mixer

root = Tk()


class Player:
    def __init__(self, window):
        window.geometry("200x200")
        window.title("Přehrávač")

        self.play_restart = tk.StringVar()
        self.pause_resume = tk.StringVar()
        self.play_restart.set("Play")
        self.pause_resume.set("Pause")

        load_button = customtkinter.CTkButton(master=root, text="Load", image="", corner_radius=10, command=self.load)
        load_button.place(x=100, y=40, anchor="center")
        play_button = Button(window, textvariable=self.play_restart, width=10, font=("Arial", 12), command=self.play)
        play_button.place(x=100, y=80, anchor="center")
        load_button = Button(window, textvariable=self.pause_resume, width=10, font=("Arial", 12), command=self.pause)
        load_button.place(x=100, y=120, anchor="center")

        self.music_file = False
        self.playing = False

    def load(self):
        self.music_file = filedialog.askopenfilename()
        print("Loaded: ", self.music_file)
        self.play_restart.set("Play")

    def play(self):
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            mixer.music.play()
            self.playing = False
            self.play_restart.set("Restart")
            self.pause_resume.set("Pause")

    def pause(self):
        if not self.playing:
            mixer.music.pause()
            self.playing = True
            self.pause_resume.set("Resume")
        else:
            mixer.music.unpause()
            self.playing = False
            self.pause_resume.set("Pause")

    def stop(self):
        mixer.music.stop()


Player(root)
root.mainloop()
