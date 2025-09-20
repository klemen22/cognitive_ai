from customtkinter import *
from chroma_memory_dump import retrieveMemory
from chroma_update_memory import updateMemory, getTextID, deleteMemory, addMemory

# color scheme
appBG = "#16161a"
appSec = "#72757e"
appTer = "#2cb67d"
appStroke = "#010101"
appText1 = "#fffffe"
appText2 = "#94a1b2"
appHighlight1 = "#7f5af0"  # also for button
appHighlight2 = "#6c4bcf"


# global button style
def createButton(parent, text, command=None):
    return CTkButton(
        master=parent,
        text=text,
        corner_radius=16,
        text_color=appText1,
        font=CTkFont(family="Consolas", size=16),
        fg_color="transparent",
        border_color=appHighlight1,
        hover_color=appHighlight2,
        border_width=1.5,
        command=command,
    )


# global text entry
def textEntry(parent, text, width, command=None):
    if len(text) > 120:
        text = text[:120] + "..."
    return CTkButton(
        master=parent,
        text=text,
        corner_radius=12,
        text_color=appText1,
        anchor="center",
        font=CTkFont(family="Consolas", size=16),
        fg_color="transparent",
        hover_color=appHighlight2,
        border_width=0,
        width=width,
        command=command,
    )


# global label template
def createLabel(parent, text="Nothing", size=16):
    return CTkLabel(
        master=parent,
        text=text,
        font=CTkFont(family="Consolas", size=size),
        bg_color=appBG,
        fg_color="transparent",
        text_color=appText1,
    )


class MainMenu(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=appBG)

        label = createLabel(self, "Agent Interface", size=40)
        label.pack(pady=40)

        button1 = createButton(
            parent=self,
            text="Begin Conversation",
            command=lambda: controller.showFrame("BeginConversation"),
        )

        button2 = createButton(
            parent=self,
            text="Edit Memory",
            command=lambda: controller.showFrame("EditMemory"),
        )
        button3 = createButton(
            parent=self,
            text="Add Memory",
            command=lambda: controller.showFrame("AddMemory"),
        )

        button1.pack(pady=5)
        button2.pack(pady=5)
        button3.pack(pady=5)


class EditMemory(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=appBG)

        label = createLabel(self, "Edit Memory", size=30)
        label.pack(pady=20)

        self.scrollFrame = CTkScrollableFrame(
            master=self,
            fg_color=appBG,
        )
        self.scrollFrame.pack(pady=10, expand=True, fill="both")

        self.refresh_btn = createButton(
            parent=self, text="Refresh", command=self.loadMemory
        )
        self.refresh_btn.pack(pady=5)

        self.back_btn = createButton(
            parent=self, text="Back", command=lambda: controller.showFrame("MainMenu")
        )
        self.back_btn.pack(pady=10)

        self.bind("<Configure>", self.onResize)
        self.loadMemory()

    def loadMemory(self):
        for x in self.scrollFrame.winfo_children():
            x.destroy()

        memories = retrieveMemory()
        window_width = self.winfo_toplevel().winfo_width()
        buttonWidth = int(window_width * 0.9)

        for i, x in enumerate(memories):
            text_short = x if len(x) <= 120 else x[:120] + "..."
            button = textEntry(self.scrollFrame, text=text_short, width=buttonWidth)
            button.pack(pady=5, anchor="center")

    def onResize(self, event):
        window_width = self.winfo_width()
        buttonWidth = int(window_width * 0.9)
        for child in self.scrollFrame.winfo_children():
            if isinstance(child, CTkButton):
                child.configure(width=buttonWidth)

    def onShow(self):
        self.loadMemory()

    def editSelected():
        print()


class AddMemory(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=appBG)

        label = createLabel(self, "Add Memory", size=30)
        label.pack(pady=40)

        back = createButton(
            parent=self, text="Back", command=lambda: controller.showFrame("MainMenu")
        )
        back.pack()


class BeginConversation(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=appBG)

        label = createLabel(self, "Conversation window", size=30)
        label.pack(pady=40)

        back = createButton(
            parent=self, text="Back", command=lambda: controller.showFrame("MainMenu")
        )
        back.pack()


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("")
        self.geometry("1200x800")

        container = CTkFrame(self, fg_color=appBG)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainMenu, BeginConversation, AddMemory, EditMemory):
            pageName = F.__name__
            frame = F(container, self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("MainMenu")

    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

        if hasattr(frame, "onShow"):
            frame.onShow()


if __name__ == "__main__":
    set_appearance_mode("dark")
    set_default_color_theme("dark-blue")
    app = App()
    app.mainloop()
