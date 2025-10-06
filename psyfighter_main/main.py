from customtkinter import *
from chroma_manager import (
    addLongTermMemory,
    updateMemory,
    getTextID,
    deleteMemory,
    retrieveMemory,
)
from llm_interaction import proccessInput, endConversation
from PIL import Image

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


# TODO: remove this and manually add title to each frame
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
            command=lambda: controller.showFrame("ConversationWindow"),
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
        button4 = createButton(parent=self, text="Exit", command=self.quit)

        button1.pack(pady=6)
        button2.pack(pady=6)
        button3.pack(pady=6)
        button4.pack(pady=6)


# ----------------------------------------------------------------------------------------------#
#                                        Edit Memory                                            #
# ----------------------------------------------------------------------------------------------#


class EditMemory(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=appBG)
        self.buttons = []

        label = createLabel(self, "Edit Memory", size=30)
        label.grid(row=0, column=0, pady=20)

        self.controller = controller

        self.scrollFrame = CTkScrollableFrame(
            master=self,
            fg_color=appBG,
        )
        self.scrollFrame.grid(row=1, column=0, sticky="nsew")

        buttonFrame = CTkFrame(master=self, fg_color=appBG, border_width=0)
        buttonFrame.grid(row=2, column=0, pady=20)

        # grid
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)

        # buttons
        refreshButton = createButton(
            parent=buttonFrame, text="Refresh", command=self.loadMemory
        )
        refreshButton.grid(row=0, column=0, padx=5)

        backButton = createButton(
            parent=buttonFrame,
            text="Back",
            command=lambda: self.controller.showFrame("MainMenu"),
        )
        backButton.grid(row=0, column=1, padx=5)

        deleteButton = createButton(
            parent=buttonFrame, text="Delete", command=self.deleteSelectedMemory
        )
        deleteButton.grid(row=0, column=2, padx=5)

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

    def deleteSelectedMemory(self):
        deleteMemory(textID=self.selectedMemory)
        print(f"Deleted memory with ID: {self.selectedMemory}")
        self.loadMemory()

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

        saveButton = createButton(
            parent=buttonFrame, text="Save", command=self.addMemory
        )
        saveButton.grid(row=0, column=1, padx=5)

    def addMemory(self):
        humanInput = self.humanEntry.get()
        aiInput = self.AiEntry.get()
        saveText = ""

        if humanInput != "":
            saveText = f"Human: {humanInput}"
        else:
            saveText = f"Human: "

        if aiInput != "":
            saveText = saveText + f"\nAI: {aiInput}"
        else:
            saveText = saveText = f"\n AI: "

        print(f"Final text to save: \n\n{saveText}")
        addLongTermMemory(text=saveText)


# ----------------------------------------------------------------------------------------------#
#                                        Converastion                                           #
# ----------------------------------------------------------------------------------------------#

# TODO: fix memory management at the end of conversation


class ConversationWindow(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=appBG)

        self.controller = controller

        # back button
        backButton = createButton(
            parent=self, text="Back", command=self.closeConversation
        )
        backButton.pack(padx=(10, 0), pady=(20, 0), anchor="w")

        # title
        label = createLabel(self, "Conversation window", size=30)
        label.pack(pady=(30, 40))

        # chat window
        self.chatFrame = CTkScrollableFrame(master=self, fg_color=appBG)
        self.chatFrame.pack(pady=20, padx=20, expand=True, fill="both")

        # input
        inputFrame = CTkFrame(master=self, fg_color=appBG)
        inputFrame.pack(pady=(0, 20), padx=20, fill="x")

        self.entry = CTkEntry(
            master=inputFrame,
            fg_color=appBG,
            placeholder_text="Enter text...",
            border_color=appHighlight1,
            border_width=2,
            corner_radius=10,
            font=CTkFont(family="Consolas", size=16),
            text_color=appText1,
        )
        self.entry.pack(fill="x", expand=True, side="left", padx=(0, 10))

        sendButton = createButton(
            parent=inputFrame, text="Send", command=self.sendMessage
        )
        sendButton.pack(side="right")

        # avatars
        self.userAvatar = CTkImage(
            dark_image=Image.open("./data/assets/icons8-user-100.png"),
            size=(40, 40),
        )
        self.aiAvatar = CTkImage(
            dark_image=Image.open("./data/assets/icons8-cursor-ai-100.png"),
            size=(40, 40),
        )

    def sendMessage(self):
        print("Sending message...")
        userText = self.entry.get().strip()

        if not userText:
            return

        self.addEntry(sender="USER", text=userText)
        self.entry.delete(first_index=0, last_index="end")

        # AI response
        aiResponse = proccessInput(userInput=userText)
        self.addEntry(sender="AI", text=aiResponse)

    def addEntry(self, sender, text):

        entry = CTkFrame(
            master=self.chatFrame,
            fg_color=appBG,
        )
        wrap_Length = 400  # default wrap lenght
        window_Width = self.winfo_toplevel().winfo_width()

        if window_Width > 200:
            wrap_Length = int(window_Width * 0.6)

        if sender == "USER":
            avatar = CTkLabel(master=entry, text="", image=self.userAvatar)
            avatar.pack(side="right", padx=5, pady=5, anchor="ne")

            textFrameUSER = CTkFrame(
                master=entry,
                fg_color=appBG,
                border_color=appHighlight2,
                border_width=2,
                corner_radius=12,
            )

            message = CTkLabel(
                master=textFrameUSER,
                text=text,
                fg_color=appBG,
                text_color=appText1,
                font=CTkFont(family="Consolas", size=16),
                wraplength=wrap_Length,
                padx=5,
                pady=5,
                anchor="e",
                justify="left",
            )

            message.pack(padx=5, pady=5)
            textFrameUSER.pack(side="right")
            entry.pack(fill="x", pady=10, padx=(0, 10), anchor="e")
        else:
            avatar = CTkLabel(master=entry, text="", image=self.aiAvatar)
            avatar.pack(side="left", padx=5, pady=5, anchor="ne")

            textFrameAI = CTkFrame(
                master=entry,
                fg_color=appBG,
                border_color=appHighlight2,
                border_width=2,
                corner_radius=12,
            )

            message = CTkLabel(
                master=textFrameAI,
                text=text,
                fg_color=appBG,
                text_color=appText1,
                font=CTkFont(family="Consolas", size=16),
                wraplength=wrap_Length,
                padx=5,
                pady=5,
                anchor="w",
                justify="left",
            )
            message.pack(padx=5, pady=5)
            textFrameAI.pack(side="left")
            entry.pack(fill="x", pady=10, padx=10, anchor="w")
        self.chatFrame.update_idletasks()

        try:
            self.chatFrame._parent_canvas.yview_moveto(1.0)
        except E:
            pass

        return

    def closeConversation(self):
        endConversation()
        self.controller.showFrame("MainMenu")


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

        for F in (MainMenu, ConversationWindow, AddMemory, EditMemory, editText):
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
