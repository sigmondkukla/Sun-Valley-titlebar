import tkinter as tk
from ctypes import WINFUNCTYPE, c_uint64, windll
from platform import win32_ver
from tkinter import ttk

from data import *


def Titlebar(
    root, main_frame, icon, title_text, minimize, maximize, close, min_width, min_height
):
    # region Docstring
    """Creates a titlebar and basic window functions

    Args:
        root (master): Root window for titlebar
        main_frame (master): Main frame of window
        icon (PhotoImage): Tkinter PhotoImage for icon
        title_text (str): Text to display in titlebar
        minimize (bool): Should a minimize button be created?
        maximize (bool): Should a maximize button be created?
        close (bool): Should a close button be created?
        min_width (int): Minimum width of titlebar
        min_height (int): Minimum height of titlebar
    """
    # endregion

    root.minimized = False  # only to know if root is minimized
    root.maximized = False  # only to know if root is maximized

    # Window manager functions
    def minimize_window():
        """Minimize the window"""
        root.iconify()
        root.minimized = True

    def deminimize(event):
        """Deminimize the window"""
        root.focus()
        if root.minimized == True:
            root.minimized = False

    def maximize_window():
        """Maximize the window"""
        if root.maximized == False:
            expand_button.config(text=" 🗗 ")
            windll.user32.ShowWindow(root.hwnd, SW_MAXIMIZE)
        else:
            expand_button.config(text=" 🗖 ")
            windll.user32.ShowWindow(root.hwnd, SW_NORMAL, 0, 0)

        root.maximized = not root.maximized

    def setup(root):
        """Setup"""

        def WndProc(hwnd, msg, wp, lp):
            """Handle the messages"""
            if msg == WM_NCCALCSIZE and wp:
                lpncsp = NCCALCSIZE_PARAMS.from_address(lp)
                lpncsp.rgrc[0].top -= root.titlebarheight

            return windll.user32.CallWindowProcW(
                *map(c_uint64, (globals()[old], hwnd, msg, wp, lp))
            )

        root.hwnd = windll.user32.GetParent(root.winfo_id())

        old, new = "old", "new"
        prototype = WINFUNCTYPE(c_uint64, c_uint64, c_uint64, c_uint64, c_uint64)

        globals()[old] = None
        globals()[new] = prototype(WndProc)
        globals()[old] = windll.user32.GetWindowLongPtrA(root.hwnd, GWL_WNDPROC)
        windll.user32.SetWindowLongPtrW(root.hwnd, GWL_WNDPROC, globals()[new])

        windll.user32.SetWindowPos(
            root.hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_FRAMECHANGED
        )

    def moving(event):
        """Rewrite the moving of the window"""
        if root.maximized == False:
            windll.user32.ReleaseCapture()
            windll.user32.SendMessageA(root.hwnd, WM_SYSCOMMAND, SC_MOVE + HTCAPTION, 0)

        else:
            expand_button.config(text=" 🗖 ")
            root.maximized = not root.maximized

    def get_window_titlebar_height(root) -> None:
        """Get the correct titlebar hegiht via system version"""
        root.titlebarheight = (
            root.winfo_rooty() - root.winfo_y() - (1 if "11" == win32_ver()[0] else 0)
        )

    # Create a frame for the titlebar
    title_bar = ttk.Frame(root)

    # Pack the title bar window
    title_bar.pack(fill=tk.X)

    # Create the title bar buttons
    if close:
        close_button = ttk.Button(
            title_bar,
            text="  ×  ",
            command=root.destroy,
            style="Close.Titlebar.TButton",
        )
        close_button.pack(side=tk.RIGHT, padx=5, pady=5)
    if maximize:
        expand_button = ttk.Button(
            title_bar, text=" 🗖 ", command=maximize_window, style="Titlebar.TButton"
        )
        expand_button.pack(side=tk.RIGHT, padx=0, pady=5)
    if minimize:
        minimize_button = ttk.Button(
            title_bar, text=" 🗕 ", command=minimize_window, style="Titlebar.TButton"
        )
        minimize_button.pack(side=tk.RIGHT, padx=5, pady=5)

    if icon != None:
        # Create the title bar icon
        title_bar_icon = ttk.Label(title_bar, image=icon)
        title_bar_icon.pack(side=tk.LEFT, padx=(10, 0), fill=tk.Y)

    # Create the title bar title
    title_bar_title = ttk.Label(title_bar, text=title_text)
    title_bar_title.pack(side=tk.LEFT, padx=(10, 0))

    # Bind events for moving the title bar
    title_bar.bind("<B1-Motion>", moving)

    # Set up the window for minimizing functionality
    root.bind("<FocusIn>", deminimize)
    root.iconbitmap("")
    get_window_titlebar_height(root)

    setup(root)


# Menubar class creates a frame for the menubar which is accessed in the Menu class
class Menubar:
    def __init__(self, root):
        self.root = root
        self.menubar_frame = ttk.Frame(root)
        self.menubar_frame.pack(fill=tk.X, pady=(0, 10))


# Adds a menubutton to the menubar frame with the text header
# And allows for the menu to be populated with commands and separators
class Menu:
    def __init__(self, menubar, header):
        self.menu = tk.Menu(menubar.menubar_frame)
        self.menubutton = ttk.Menubutton(
            menubar.menubar_frame, text=header, menu=self.menu, direction="below"
        )
        self.menubutton.pack(side=tk.LEFT, padx=(10, 0))

    def add_command(self, label, command=None):
        """..."""
        if command != None:
            self.menu.add_command(label=label, command=command)
        else:
            self.menu.add_command(label=label)

    def add_separator(self):
        """..."""
        self.menu.add_separator()
