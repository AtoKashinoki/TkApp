"""
    Widget tools

This file contains the Widget-relate tools used for developing in tk application.
"""


""" imports """


from tkinter import ttk


"""
    Widgets
"""


""" Frame """


class Frame(ttk.Frame):
    """ Frame widget which may contain other widgets and can have a 3D border. """

    def destroy_children(self) -> None:
        """ Destroy all child widgets """
        for child in self.winfo_children():
            child.destroy()
            continue
        return

    ...
