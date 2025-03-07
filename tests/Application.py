

from tkinter import ttk
from tkapp.Application import ApplicationSkeleton
from tkapp.Page import PageSkeleton


class Sub(PageSkeleton):

    initial_count: int = 0

    def __setup__(self) -> None:
        Sub.initial_count += 1
        self.name = f"SubPage{Sub.initial_count}"
        return

    def __page_create__(self, app: ApplicationSkeleton) -> None:
        print(app.pages)
        ttk.Button(
            self, text="Return",
            command=lambda : app.add_page(
                Main, "Main", True, True
            )
        ).pack(anchor="nw")
        return

    ...


class Main(PageSkeleton):

    def __setup__(self) -> None:
        self.name = "MainPage"
        return

    def __page_create__(self, app: ApplicationSkeleton) -> None:
        print(app.pages)
        note = ttk.Notebook(self, **self.size)

        frame1 = ttk.Frame(self, **self.size)
        ttk.Label(frame1, text="Main page note1").pack(anchor="nw")
        frame1.pack(anchor="nw")

        frame2 = ttk.Frame(self, **self.size)
        ttk.Button(
            frame2, text="Restart",
            command=lambda : app.reboot()
        ).pack(anchor="nw")
        frame2.pack(anchor="nw")

        frame3 = ttk.Frame(self, **self.size)
        ttk.Button(
            frame3, text="Next page",
            command=lambda: app.add_page(
                Sub, switch=True, del_pre_page=True
            )
        ).pack(anchor="nw")
        frame3.pack(anchor="nw")

        note.add(frame1, text="Main page note1")
        note.add(frame2, text="Main page note2")
        note.add(frame3, text="Main page note3")
        note.pack(anchor="nw")

        return

    ...


class Application(ApplicationSkeleton):

    def __init__(self):
        ApplicationSkeleton.__init__(self)
        return

    def __init_pages__(self) -> None:
        self.set_main_page(Main)
        return

    ...




if __name__ == '__main__':
    Application().mainloop()
    ...
