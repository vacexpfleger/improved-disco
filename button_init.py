import customtkinter


def button(master, image, command):
    return customtkinter.CTkButton(master=master, image=image, text="", command=command, width=60, height=60,
                                   border_width=0, corner_radius=20)