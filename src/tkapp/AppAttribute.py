"""
    Application attribute systems

This file contains ApplicationAttr-relate systems used for creating application system.
"""


""" imports """


import tkinter

from CodingTools.Inheritance import DataClass
from CodingTools.Descriptor import RunFunc


""" Window attribute class """


class Window(DataClass):
    """ Window attributes """

    """ master """
    __master: tkinter.Tk

    def __init__(self, _master: tkinter.Tk):
        """ Initialize master """
        self.__master = _master

        """ attributes """
        self.title = "Title"
        self.icon = None
        self.geometry = "100x100"
        self.resizable = True, True
        return

    """ Attributes """
    title: str = RunFunc(
        lambda obj, value: getattr(obj.__master, "title")(value)
    )
    icon: str | None = RunFunc(
        lambda obj, value: getattr(obj.__master, "iconbitmap")(default=value)
    )
    geometry: str = RunFunc(
        lambda obj, value: getattr(obj.__master, "geometry")(value)
    )
    resizable: tuple[bool, bool] = RunFunc(
        lambda obj, value: getattr(obj.__master, "resizable")(*value)
    )

    ...


