import tkinter as tk
from tkinter import ttk
import sun_valley_titlebar
from ctypes import windll, c_char_p, c_int, byref, sizeof

WINDOW_TITLE = "Titlebar Demo"
WINDOW_MINSIZE = (400, 400)
WINDOW_POSITION = (100, 100) # Make sure to set a decent starting position, otherwise the window will be placed at the top left of the screen

root = tk.Tk()

# Set window parameters
root.minsize(WINDOW_MINSIZE[0], WINDOW_MINSIZE[1])
root.geometry(str(WINDOW_MINSIZE[0]) + "x" + str(WINDOW_MINSIZE[1]) + "+" + str(WINDOW_POSITION[0]) + "+" + str(WINDOW_POSITION[1]))
root.title(WINDOW_TITLE)

# Set the default theme
root.tk.call("source", "sun-valley.tcl")
root.tk.call("set_theme", "light")

# Optional icon for the titlebar
# Must be a gif file and not too large
# because it currently is not automatically resized
icon = tk.PhotoImage(file='feather.gif')

# Change theme function
def change_theme():
    if root.tk.call("ttk::style", "theme", "use") == "sun-valley-dark":
        root.tk.call("set_theme", "light")
    else:
        root.tk.call("set_theme", "dark")


# Create the content frame
big_frame = ttk.Frame(root)

# Create the titlebar
# Parameters: master, big_frame (for resizing), icon, title, minimize button?, maximize button?, close button?, min window size x, min window size y
titlebar = sun_valley_titlebar.Titlebar(root, big_frame, icon, WINDOW_TITLE, True, True, True, WINDOW_MINSIZE[0], WINDOW_MINSIZE[1])

# Create a menubar
menubar = sun_valley_titlebar.Menubar(root)

# Add "File" menu to the menubar
menu = sun_valley_titlebar.Menu(menubar, "File")
menu.add_command("Change theme", change_theme)
menu.add_separator()
menu.add_command("Exit", root.destroy)
# Add "Options" menu to the menubar
options_menu = sun_valley_titlebar.Menu(menubar, "Options")
options_menu.add_command("Option 1")
options_menu.add_command("Option 2")
options_menu.add_command("Option 3")

# Finally pack the big frame so it is below the titlebar and menu
big_frame.pack(fill="both", expand=True)

# Content goes here, with master = big_frame
button = ttk.Button(big_frame, text="Change theme!", command=change_theme)
button.pack()

root.mainloop()
