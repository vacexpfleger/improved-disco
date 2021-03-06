import os
import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import customtkinter
from PIL import Image, ImageTk
from tinytag import TinyTag
from mutagen.mp3 import MP3
from pygame import mixer
from button_init import button

mixer.init()


class App(tk.Tk):

    NAME = "Improved Disco"
    WIDTH = 700
    HEIGHT = 500
    PATH = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        super().__init__()

        self.title(App.NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        # self.minsize(App.WIDTH, App.HEIGHT)
        self.resizable(False, False)
        self.iconphoto(False, tk.PhotoImage(file='music_player.png'))
        self.default_album = ImageTk.PhotoImage(Image.open(self.PATH + "/default.png").resize((150, 150)))

        # frame init
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, height=App.HEIGHT - 40, corner_radius=10)
        self.frame_left.place(relx=0.32, rely=0.5, anchor=tk.E)

        self.frame_right = customtkinter.CTkFrame(master=self, width=420, height=App.HEIGHT - 40, corner_radius=10)
        self.frame_right.place(relx=0.365, rely=0.5, anchor=tk.W)

        # button init
        self.place_buttons()

        # playlist init
        self.playlist = Listbox(self.frame_right, bg="white", fg="black", width=45)
        self.playlist.place(relx=0.5, y=120, anchor=tk.CENTER)

        # status bar init
        self.status_bar = Label(self.frame_right, text="", bd=1, relief=RAISED, padx=5, pady=3)
        self.status_bar.place(relx=0.5, y=215, anchor=tk.CENTER)
        self.status_bar.place_forget()

        # album show init
        self.song_info = Label(self.frame_right, text="", image=self.default_album, compound=TOP)
        self.song_info.place(relx=0.5, y=340, anchor=tk.CENTER)
        self.song_info.place_forget()

        # menu init
        self.player_menu = Menu(self)
        self.config(menu=self.player_menu)

        self.add_song_menu = Menu(self.player_menu)
        self.player_menu.add_cascade(label="File", menu=self.add_song_menu)
        self.add_song_menu.add_command(label="Add", command=self.add_songs)
        self.add_song_menu.add_command(label="Clear", command=self.clear)
        self.add_song_menu.add_separator()
        self.add_song_menu.add_command(label="Exit", command=self.exitapp)

        self.file = None
        self.song = None
        self.update_time = None
        self.playing = False
        self.add_count = 0
        self.songs_list = []

    def place_buttons(self):
        play_image = ImageTk.PhotoImage(Image.open(self.PATH + "/play.png").resize((40, 40)))
        pause_image = ImageTk.PhotoImage(Image.open(self.PATH + "/pause.png").resize((40, 40)))
        stop_image = ImageTk.PhotoImage(Image.open(self.PATH + "/stop.png").resize((40, 40)))
        next_image = ImageTk.PhotoImage(Image.open(self.PATH + "/next.png").resize((40, 40)))
        previous_image = ImageTk.PhotoImage(Image.open(self.PATH + "/previous.png").resize((40, 40)))

        button_1 = button(self.frame_left, play_image, self.play)
        button_1.place(relx=0.5, y=80, anchor=tk.CENTER)
        button_2 = button(self.frame_left, pause_image, self.pause)
        button_2.place(relx=0.5, y=150, anchor=tk.CENTER)
        button_3 = button(self.frame_left, stop_image, self.stop)
        button_3.place(relx=0.5, y=220, anchor=tk.CENTER)
        button_4 = button(self.frame_left, previous_image, self.previous)
        button_4.place(relx=0.5, y=290, anchor=tk.CENTER)
        button_5 = button(self.frame_left, next_image, self.next)
        button_5.place(relx=0.5, y=360, anchor=tk.CENTER)

    def add_songs(self):
        # adds songs to playlist
        songs = filedialog.askopenfilenames(title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
        for song in songs:
            split_songs = list(os.path.split(song))  # splits song path into two separate parts (directory, file)
            self.songs_list.append(split_songs)
            self.playlist.insert(END, split_songs[1])  # adds song name to playlist
        self.add_count += 1
        temp_selection = self.playlist.curselection()
        if self.add_count > 1:
            self.highlight(temp_selection[0])
        else:
            self.highlight(0)

    def play(self):
        # plays a song
        self.song = self.playlist.get(ACTIVE)
        self.song_directory = list(filter(lambda active: active[1] == self.song, self.songs_list))  # looks for directory
        self.file = str(self.song_directory[0][0]) + "/" + str(self.song)  # sticks it back together
        mixer.music.load(self.file)
        mixer.music.play()
        self.play_time()
        self.show_album()

    def play_alt(self, song_number):
        # plays a next song
        try:
            self.song = self.playlist.get(song_number)
            self.song_directory = list(filter(lambda active: active[1] == self.song, self.songs_list))
            self.file = str(self.song_directory[0][0]) + "/" + str(self.song)
            mixer.music.load(self.file)
            mixer.music.play()
            self.play_time()
            self.highlight(song_number)
            self.show_album()
        except IndexError:
            self.show_album()
            self.highlight(0)
            self.stop()

    def pause(self):
        if not self.playing:
            mixer.music.pause()
            self.playing = True
        else:
            mixer.music.unpause()
            self.playing = False

    def play_time(self):
        current_time = mixer.music.get_pos() / 1000
        time_converted = time.strftime("%H:%M:%S", time.gmtime(current_time))
        song_duration = time.strftime("%H:%M:%S", time.gmtime(int(MP3(self.file).info.length)))

        if self.song:
            final_time = f'{self.song}\n{time_converted}/{song_duration}'

            if int(current_time) + 1 == int(MP3(self.file).info.length):  # if the song ends, go to the next one
                time.sleep(1)
                self.next()

        else:
            final_time = f"00:00:00/00:00:00"

        self.status_bar.config(text=final_time)
        self.status_bar.place(relx=0.5, y=215, anchor=tk.CENTER)
        self.update_time = self.status_bar.after(1000, self.play_time)

    def next(self):
        # get an index of the next song
        next_song = self.playlist.curselection()
        next_song = next_song[0] + 1
        self.play_alt(next_song)

    def previous(self):
        # get an index of the previous song
        next_song = self.playlist.curselection()
        next_song = next_song[0] - 1
        self.play_alt(next_song)

    def stop(self):
        mixer.music.stop()

    def highlight(self, selection):
        self.playlist.selection_clear(0, END)
        self.playlist.activate(selection)
        self.playlist.selection_set(selection, last=None)

    def show_album(self):
        global album_name, album_image
        try:
            album_name = TinyTag.get(self.file).album
            album_image = ImageTk.PhotoImage(Image.open(str(self.song_directory[0][0]) + "/cover.jpg").resize((150, 150)))
        except FileNotFoundError:
            album_image = self.default_album
        except IndexError:
            album_name = ""
            album_image = self.default_album
        finally:
            self.song_info.config(text=album_name, image=album_image)
            self.song_info.image = album_image
            self.song_info.place(relx=0.5, y=340, anchor=tk.CENTER)

    def clear(self):
        self.playlist.delete(0, END)
        self.add_count = 0

    def startapp(self):
        self.mainloop()

    def exitapp(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.startapp()
