"""
    Application page system

This file contains the ApplicationPage-relate tools used for developing in tkapp.
"""


""" imports """


import tkinter
from abc import abstractmethod
from CodingTools.Inheritance import InheritanceSkeleton

from .AppAttribute import Window


"""
    Page system
"""


""" Application dummy """


class Application(InheritanceSkeleton):
    """ Application Skeleton """

    """ properties """
    @property
    def master(self) -> tkinter.Tk: return NotImplemented
    @property
    def window(self) -> Window: return NotImplemented

    @property
    def size_tuple(self) -> tuple: return NotImplemented
    @property
    def size(self) -> dict[str, int]: return NotImplemented

    @property
    def config_dir(self) -> str: return NotImplemented

    @property
    def current_page_key(self) -> str: return NotImplemented
    @property
    def pages(self) -> dict[str, "PageSkeleton"]: return NotImplemented

    """ functions """
    def save_config(self) -> None:
        """ Save configs """
        return

    def add_page(
            self,
            _page: type["PageSkeleton"],
            key: str = None,
            switch: bool = False,
            del_pre_page: bool = False,
    ) -> None:
        """ Add page in self """
        return

    def add_pages(
            self,
            _pages: list[type["PageSkeleton"]] | tuple[type["PageSkeleton"]]
    ) -> None:
        """ Add pages in self """
        return

    def del_page(self, _page_key: str) -> bool:
        """ Delete page in self """
        return NotImplemented

    def change_page(
            self,
            _page_key: str,
            del_pre_page: bool = False,
    ) -> bool:
        """
            Change page
        :return: True if page was changed.
        """
        return NotImplemented

    ...

""" Page class """


class PageSkeleton(tkinter.Frame, InheritanceSkeleton):
    """ Application page system class """

    """ Initializer """
    def __init__(
            self,
            _parent: tkinter.Tk,
            _application: Application,
            size: tuple[int, int] | list[int, int] = None,
    ):
        """ Initialize page systems """

        """ tkinter """
        if size is None:
            size = _application.size_tuple
            ...
        self.__size = size
        tkinter.Frame.__init__(
            self, _parent,
            **self.size,
        )

        """ system values """
        self.__parent = _parent
        self.__application = _application
        self.__name = None

        """ Call setup """
        self.__setup__()
        return

    """ parent """
    __parent: tkinter.Tk
    @property
    def parent(self): return self.__parent

    """ application """
    __application: Application
    @property
    def application(self) -> Application: return self.__application
    @property
    def app(self) -> Application: return self.__application

    """ properties """
    __size: tuple[int, int]
    @property
    def size_tuple(self) -> tuple[int, int]: return self.__size
    @property
    def size(self) -> dict[str, int]:
        return {
            key: value
            for key, value in zip(
                ["width", "height"],
                self.__size,
            )
        }

    """ Called functions """
    @abstractmethod
    def __setup__(self) -> None:
        """ Setup function """
        return

    @abstractmethod
    def __page_create__(self, app: Application) -> None:
        """ Page setup function """
        return

    def __create__(self) -> "PageSkeleton":
        """ Page create function """
        self.__page_create__(self.__application)
        return self

    def __draw__(self) :
        """ Page draw function """
        self.place(x=0, y=0)
        return

    """ page name """
    __name: str | None
    @property
    def name(self) -> str: return self.__name
    @name.setter
    def name(self, _name: str): self.__name = _name

    def __str__(self) -> str:
        """ Return self name """
        if self.__name is None: return f"<Page[{hash(self)}]>"
        return self.__name

    """ debug """
    def __repr__(self) -> str:
        """ print text """
        return f"{self.__name}"

    ...
