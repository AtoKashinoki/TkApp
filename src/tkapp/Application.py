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

from .Page import Application as Attributes, PageSkeleton, call_create, display
from CodingTools.Inheritance import InheritanceSkeleton
from abc import abstractmethod


"""
    Application
"""


""" Application class """


class ApplicationSkeleton(Attributes, InheritanceSkeleton):
    """
        Tkinter Application class

    This class manage widgets and application options.
    """

    """ constants """
    __WIN_CNF_NAME: str = "window.cnf"

    """ Initializer """
    def __init__(
            self,
            root_type: type[tkinter.Tk] = tkinter.Tk,
            use_config: bool = True,
            config_dir: str = os.path.join(".", "confs"),
    ):
        """ Initialize tk and values """

        """ Tkinter """
        self.__root_type = root_type
        self.__master = root_type()
        self.__window = Window(self.__master)
        self.__reboot_flag = False

        """ config """
        self.__use_config = use_config
        self.__config_dir = config_dir
        self.load_config()
        self.save_config()

        """ page """
        self.__current_page_key = "Main"
        self.__pages = {"Main": None}
        self.__init_pages__()

        return

    """ Tkinter """
    __root_type: type[tkinter.Tk] = tkinter.Tk
    @property
    def root_type(self) -> type[tkinter.Tk]: return self.__root_type

    __master: tkinter.Tk
    @property
    def master(self) -> tkinter.Tk: return self.__master

    __window: Window
    @property
    def window(self) -> Window: return self.__window

    __reboot_flag: bool
    @property
    def reboot_flag(self) -> bool: return self.__reboot_flag

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

        """ Reboot """
        if self.reboot_flag:
            self.__reboot_flag = False
            self.load_config()
            self.__master.destroy()
            ApplicationSkeleton.__init__(
                self,
                self.__root_type,
                self.__use_config,
                self.__config_dir,
            )
            self.mainloop()
            ...

        self.save_config()
        return 0

    def reboot(self) -> None:
        """ Restart application """
        self.__master.quit()
        self.__reboot_flag = True
        return

    """ config """
    __use_config: bool
    @property
    def use_config(self) -> bool: return self.__use_config

    __config_dir: str
    @property
    def config_dir(self) -> str: return self.__config_dir

    def load_config(self) -> None:
        """ Load configs """
        if not self.__use_config: return

        if self.__config_dir == os.path.join(".", "confs"): mkdir(self.__config_dir)
        window_cnf = ConfigManager(
            os.path.join(self.__config_dir, self.__WIN_CNF_NAME)
        )
        window_cnf.setattr(self.__window, self.__window.keys())
        return

    def save_config(self) -> None:
        """ Save configs """
        if not self.__use_config: return

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

    __pages: dict[str, PageSkeleton | None]
    @property
    def pages(self) -> dict[str, PageSkeleton]: return self.__pages

    def __page_run(self) -> None:
        """ Create and draw page """
        page = self.__pages[self.__current_page_key]
        if page is None: raise TypeError(
            "Main page is not setting. Execute self.set_main_page function."
        )
        call_create(page)
        display(page)
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

    def set_main_page(
            self,
            _page: type[PageSkeleton],
    ):
        """ Set main page """
        self.__pages[self.__current_page_key] =\
            _page(self.__master, self)
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

    @abstractmethod
    def __init_pages__(self) -> None:
        """ Page initializer """
        return

    ...
