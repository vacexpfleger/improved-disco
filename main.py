import tkinter
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

        # image init
        play_image = ImageTk.PhotoImage(Image.open(self.PATH + "/play.png").resize((40, 40)))
        pause_image = ImageTk.PhotoImage(Image.open(self.PATH + "/pause.png").resize((40, 40)))
        stop_image = ImageTk.PhotoImage(Image.open(self.PATH + "/stop.png").resize((40, 40)))
        next_image = ImageTk.PhotoImage(Image.open(self.PATH + "/next.png").resize((40, 40)))
        previous_image = ImageTk.PhotoImage(Image.open(self.PATH + "/previous.png").resize((40, 40)))

        # frame init
        self.frame_left = customtkinter.CTkFrame(master=self, width=200, height=App.HEIGHT - 40, corner_radius=10)
        self.frame_left.place(relx=0.32, rely=0.5, anchor=tk.E)

        self.frame_right = customtkinter.CTkFrame(master=self, width=420, height=App.HEIGHT - 40, corner_radius=10)
        self.frame_right.place(relx=0.365, rely=0.5, anchor=tk.W)

        # button init
        self.button_1 = customtkinter.CTkButton(master=self.frame_left, image=play_image, text="", command=self.play,
                                                width=60, height=60, border_width=0, corner_radius=20)
        self.button_1.place(relx=0.5, y=80, anchor=tk.CENTER)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left, image=pause_image, text="", command=self.pause,
                                                width=60, height=60, border_width=0, corner_radius=20)
        self.button_2.place(relx=0.5, y=150, anchor=tk.CENTER)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left, image=stop_image, text="", command=self.stop,
                                                width=60, height=60, border_width=0, corner_radius=20)
        self.button_3.place(relx=0.5, y=220, anchor=tk.CENTER)

        self.button_4 = customtkinter.CTkButton(master=self.frame_left, image=previous_image, text="",
                                                command=self.previous, width=60, height=60, border_width=0,
                                                corner_radius=20)
        self.button_4.place(relx=0.5, y=290, anchor=tk.CENTER)

        self.button_5 = customtkinter.CTkButton(master=self.frame_left, image=next_image, text="",
                                                command=self.next, width=60, height=60, border_width=0,
                                                corner_radius=20)
        self.button_5.place(relx=0.5, y=360, anchor=tk.CENTER)

        # playlist init
        self.playlist = Listbox(self.frame_right, bg="white", fg="black", width=45)
        self.playlist.place(relx=0.5, y=120, anchor=tk.CENTER)

        # status bar init
        self.status_bar = Label(self.frame_right, text="", bd=1, relief=RAISED, padx=5, pady=3)
        self.status_bar.place(relx=0.5, y=215, anchor=tk.CENTER)
        self.status_bar.place_forget()

        # menu init
        self.player_menu = Menu(self)
        self.config(menu=self.player_menu)

        self.add_song_menu = Menu(self.player_menu)
        self.player_menu.add_cascade(label="File", menu=self.add_song_menu)
        self.add_song_menu.add_command(label="Add", command=self.add_songs)
        self.add_song_menu.add_command(label="Clear", command=self.clear)
        self.add_song_menu.add_separator()
        self.add_song_menu.add_command(label="Exit", command=quit)

        self.file = None
        self.song = None
        self.update_time = None
        self.song_info = None
        self.playing = False
        self.add_count = 0
        self.songs_list = []

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
        self.song = self.playlist.get(song_number)
        self.song_directory = list(filter(lambda active: active[1] == self.song, self.songs_list))
        self.file = str(self.song_directory[0][0]) + "/" + str(self.song)
        mixer.music.load(self.file)
        mixer.music.play()
        self.play_time()
        self.highlight(song_number)
        self.show_album()

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
            mixer.music.stop()
            final_time = f'End of playlist.'
            self.highlight(0)

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
        self.status_bar.after_cancel(self.update_time)
        self.status_bar.config(text=f'00:00:00/00:00:00')

    def highlight(self, selection):
        self.playlist.selection_clear(0, END)
        self.playlist.activate(selection)
        self.playlist.selection_set(selection, last=None)

    def show_album(self):
        try:
            album_image = ImageTk.PhotoImage(Image.open(str(self.song_directory[0][0]) + "/cover.jpg").resize((150, 150)))
            print("Album cover je dostupný.")
        except IOError:
            print(f"Album cover není dostupný.")
            if self.song_info.winfo_exists() == 1:
                self.song_info.place_forget()
        else:
            self.song_info = Label(self.frame_right, image=album_image)
            self.song_info.image = album_image
            self.song_info.place(relx=0.5, y=320, anchor=tk.CENTER)

        album_image = None

    def clear(self):
        self.playlist.delete(0, END)

    def startapp(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.startapp()
