from customtkinter import *
from chroma_memory_dump import retrieveMemory
from chroma_update_memory import updateMemory, getTextID, deleteMemory

# color scheme
appBG = "#16161a"
appSec = "#72757e"
appTer = "#2cb67d"
appStroke = "#010101"
appText1 = "#fffffe"
appText2 = "#94a1b2"
appHighlight1 = "#7f5af0"  # also for button
appHighlight2 = "#6c4bcf"

# ----------------------------------------------------------------------------------------------#
#                                     Global helper functions                                   #
# ----------------------------------------------------------------------------------------------#


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
        border_color=appHighlight2,
        border_width=0,
        width=width,
        command=command,
    )


# global label template (title)
def createLabel(parent, text="Nothing", size=16):
    return CTkLabel(
        master=parent,
        text=text,
        font=CTkFont(family="Consolas", size=size),
        bg_color=appBG,
        fg_color="transparent",
        text_color=appText1,
    )


# ----------------------------------------------------------------------------------------------#
#                                         Main menu                                             #
# ----------------------------------------------------------------------------------------------#


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
            text="Add Memory",
            command=lambda: controller.showFrame("AddMemory"),
        )
        button3 = createButton(
            parent=self,
            text="Edit Memory",
            command=lambda: controller.showFrame("EditMemory"),
        )

        button1.pack(pady=5)
        button2.pack(pady=5)
        button3.pack(pady=5)


# ----------------------------------------------------------------------------------------------#
#                                        Edit Memory                                            #
# ----------------------------------------------------------------------------------------------#


class EditMemory(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=appBG)
        self.buttons = []

        label = createLabel(self, "Edit Memory", size=30)
        label.pack(pady=20)

        self.controller = controller

        self.scrollFrame = CTkScrollableFrame(
            master=self,
            fg_color=appBG,
        )
        self.scrollFrame.pack(pady=10, expand=True, fill="both")

        self.refresh_btn = createButton(
            parent=self, text="Refresh", command=self.loadMemory
        )
        self.refresh_btn.pack(pady=5)

        self.backButton = createButton(
            parent=self,
            text="Back",
            command=lambda: self.controller.showFrame("MainMenu"),
        )
        self.backButton.pack(pady=10)

        self.deleteButton = createButton(parent=self, text="Delete")
        self.deleteButton.pack(pady=10)

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
            button = textEntry(
                self.scrollFrame,
                text=text_short,
                width=buttonWidth,
            )
            self.buttons.append(button)

            button.bind(
                "<Button-1>",
                lambda event, memoryID=getTextID(x), bttn=button: self.selectMemory(
                    memoryID=memoryID, event=event, button=bttn
                ),
            )

            button.bind(
                "<Double-Button-1>",
                lambda event, fullText=x, memoryID=getTextID(
                    x
                ): self.controller.showFrame(
                    "editText", text=fullText, memoryID=memoryID
                ),
            )

            button.pack(pady=5, anchor="center")

    def selectMemory(self, memoryID, event, button):
        self.selectedMemory = memoryID
        print(f"Selected memory ID:{memoryID}")

        for child in self.scrollFrame.winfo_children():
            child.configure(border_width=0)
        button.configure(border_width=2)

    def onResize(self, event):
        window_width = self.winfo_width()
        buttonWidth = int(window_width * 0.9)
        for child in self.scrollFrame.winfo_children():
            if isinstance(child, CTkButton):
                child.configure(width=buttonWidth)

    def onShow(self):
        self.loadMemory()


class editText(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=appBG)

        self.controller = controller
        self.label = createLabel(parent=self, text="Edit selected memory", size=30)
        self.label.pack(pady=20)

        self.textBox = CTkTextbox(
            master=self,
            height=300,
            fg_color=appBG,
            corner_radius=12,
            border_color=appHighlight1,
            border_width=2,
            font=CTkFont(family="Consolas", size=16),
            text_color=appText1,
            wrap="word",
        )
        self.textBox.pack(pady=10, padx=40, expand=True, fill="both")

        self.saveButton = createButton(
            parent=self, text="Save", command=self.saveMemory
        )
        self.saveButton.pack(pady=20)
        self.backButton = createButton(
            parent=self, text="Back", command=lambda: controller.showFrame("EditMemory")
        )
        self.backButton.pack(pady=5)
        self.bind("<Configure>", self.onResize)

    def onResize(self, event):
        window_width = self.winfo_width()
        new_width = int(window_width * 0.8)
        self.textBox.configure(width=new_width)

    def onShow(self, text=None, memoryID=None):
        # debug
        print(f"Input Text:\n\n{text}")
        print(f"Input Memory ID:\n\n{memoryID}")
        self.memoryID = memoryID

        self.textBox.delete("1.0", "end")
        if text:
            self.textBox.insert("1.0", text=text)

    def saveMemory(self):
        updatedText = self.textBox.get("1.0", "end-1c")
        updateMemory(textID=self.memoryID, newText=updatedText)


# ----------------------------------------------------------------------------------------------#
#                                         Add Memory                                            #
# ----------------------------------------------------------------------------------------------#


class AddMemory(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=appBG)

        label = createLabel(self, "Add Memory", size=30)
        label.pack(pady=30)

        # Human part
        humanFrame = CTkFrame(master=self, fg_color=appBG, border_width=0)
        humanFrame.pack(pady=10, padx=20, fill="x")

        humanLabel = CTkLabel(
            master=humanFrame,
            text="Human:",
            font=CTkFont(family="Consolas", size=20),
            text_color=appText1,
        )
        humanLabel.grid(row=0, column=0, sticky="w", padx=5)

        self.humanEntry = CTkEntry(
            master=humanFrame,
            corner_radius=12,
            border_width=2,
            fg_color=appBG,
            border_color=appHighlight1,
            placeholder_text="enter text...",
            font=CTkFont(family="Consolas", size=16),
        )
        self.humanEntry.grid(row=0, column=1, sticky="ew", padx=5)
        humanFrame.grid_columnconfigure(index=1, weight=1)

        # AI part
        AiFrame = CTkFrame(master=self, fg_color=appBG, border_width=0)
        AiFrame.pack(pady=10, padx=20, fill="x")

        AiLabel = CTkLabel(
            master=AiFrame,
            text="AI:   ",
            font=CTkFont(family="Consolas", size=20),
            text_color=appText1,
        )
        AiLabel.grid(row=0, column=0, sticky="w", padx=5)

        self.AiEntry = CTkEntry(
            master=AiFrame,
            corner_radius=12,
            border_width=2,
            fg_color=appBG,
            border_color=appHighlight1,
            placeholder_text="enter text...",
            font=CTkFont(family="Consolas", size=16),
        )
        self.AiEntry.grid(row=0, column=1, sticky="ew", padx=5)
        AiFrame.grid_columnconfigure(index=1, weight=1)

        buttonFrame = CTkFrame(master=self, fg_color=appBG, border_width=0)
        buttonFrame.pack(pady=30, padx=20)

        backButton = createButton(
            parent=buttonFrame,
            text="Back",
            command=lambda: controller.showFrame("MainMenu"),
        )
        backButton.grid(row=0, column=0, padx=5)

        saveButton = createButton(parent=buttonFrame, text="Save", command=None)
        saveButton.grid(row=0, column=1, padx=5)


# ----------------------------------------------------------------------------------------------#
#                                        Converastion                                           #
# ----------------------------------------------------------------------------------------------#


class BeginConversation(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=appBG)

        label = createLabel(self, "Conversation window", size=30)
        label.pack(pady=40)

        back = createButton(
            parent=self, text="Back", command=lambda: controller.showFrame("MainMenu")
        )
        back.pack()


# ----------------------------------------------------------------------------------------------#
#                                           Main                                                #
# ----------------------------------------------------------------------------------------------#


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

        for F in (MainMenu, BeginConversation, AddMemory, EditMemory, editText):
            pageName = F.__name__
            frame = F(container, self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("MainMenu")

    def showFrame(self, pageName, **kwargs):
        frame = self.frames[pageName]
        frame.tkraise()

        if hasattr(frame, "onShow"):
            frame.onShow(**kwargs)


if __name__ == "__main__":
    set_appearance_mode("dark")
    set_default_color_theme("dark-blue")
    app = App()
    app.mainloop()
