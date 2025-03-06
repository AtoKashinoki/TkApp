"""
    Application system tools

This file contains the ApplicationSystem-relate tools used for developing in tkinter.
"""


""" imports """


import os
from CodingTools.os import mkdir

import tkinter

from .AppAttribute import Window
from CodingTools.Config import ConfigManager

from .Page import Application as ApplicationSkeleton, PageSkeleton


"""
    Application
"""


""" Application class """


class Application(ApplicationSkeleton):
    """
        Tkinter Application class

    This class manage widgets and application options.
    """

    """ constants """
    __WIN_CNF_NAME: str = "window.cnf"

    """ Initializer """
    def __init__(
            self,
            _main_page: type[PageSkeleton],
            root: tkinter.Tk = tkinter.Tk(),
            config_dir: str = os.path.join(".", "confs"),
    ):
        """ Initialize tk and values """

        """ Tkinter """
        self.__master = root
        self.__window = Window(self.__master)

        """ config """
        if config_dir == os.path.join(".", "confs"): mkdir(config_dir)
        self.__config_dir = config_dir
        window_cnf = ConfigManager(
            os.path.join(config_dir, self.__WIN_CNF_NAME)
        )
        window_cnf.setattr(self.__window, self.__window.keys())

        """ page """
        self.__current_page_key = "Main"
        self.__pages = {
            self.__current_page_key: _main_page(self.__master, self)
        }

        return

    """ Tkinter """
    __master: tkinter.Tk
    @property
    def master(self) -> tkinter.Tk: return self.__master

    __window: Window
    @property
    def window(self) -> Window: return self.__window

    @property
    def size_tuple(self) -> tuple:
        return tuple(self.__window.geometry.split("x"))
    @property
    def size(self) -> dict[str, int]:
        return {
            key: value
            for key, value in zip(
                ["width", "height"],
                self.size_tuple,
            )
        }

    def mainloop(self) -> int:
        """ Run application """
        self.__page_run()
        self.__master.mainloop()
        self.save_config()
        return 0

    """ config """
    __config_dir: str
    @property
    def config_dir(self) -> str: return self.__config_dir

    def save_config(self) -> None:
        """ Save configs """
        window_cnf = ConfigManager(
            os.path.join(self.config_dir, self.__WIN_CNF_NAME)
        )
        window_cnf.getattr(self.__window, self.__window.keys())
        window_cnf.save()
        return

    """ pages system """
    __current_page_key: str
    @property
    def current_page_key(self) -> str: return self.__current_page_key

    __pages: dict[str, PageSkeleton]
    @property
    def pages(self) -> dict[str, PageSkeleton]: return self.__pages

    def __page_run(self) -> None:
        """ Create and draw page """
        page: PageSkeleton = self.__pages[self.__current_page_key]
        page.__create__()
        page.__draw__()
        return

    def __new_page_run(
            self,
            _new_page_key: str,
            del_pre_page: bool = False,
    ) -> None:
        """ Create and draw new page """
        pre_page_key = self.__current_page_key
        self.__current_page_key = _new_page_key
        pre_page = self.__pages[pre_page_key]
        if del_pre_page: self.del_page(pre_page_key)
        self.__page_run()
        pre_page.place_forget()
        return

    def add_page(
            self,
            _page: type[PageSkeleton],
            key: str = None,
            switch: bool = False,
            del_pre_page: bool = False,
    ) -> None:
        """ Add page in self """
        page_ins = _page(self.__master, self)
        if key is None: key = str(page_ins)
        self.__pages[key] = page_ins
        if switch: self.change_page(key, del_pre_page=del_pre_page)
        return

    def add_pages(self, _pages: list[type[PageSkeleton]] | tuple[type[PageSkeleton]]) -> None:
        """ Add pages in self """
        for page in _pages:
            self.add_page(page)
            continue
        return

    def del_page(self, _page_key: str) -> bool:
        """ Delete page in self """
        if _page_key in self.pages:
            del self.pages[_page_key]
            return True
        return False

    def change_page(
            self,
            _page_key: str,
            del_pre_page: bool = False,
    ) -> bool:
        """
            Change page
        :return: True if page was changed.
        """
        if _page_key in self.pages:
            self.__new_page_run(_page_key, del_pre_page=del_pre_page)
            return True
        return False

    ...
