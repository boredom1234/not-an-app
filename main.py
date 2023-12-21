import os
import threading
import tkinter as tk
from tkinter import Text, Menu, Scrollbar, filedialog, messagebox, PhotoImage
from dotenv import load_dotenv
import google.generativeai as genai

class Notepad:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Untitled - Notepad")
        self.root.geometry('600x400')

        self.text_area = Text(self.root)
        self.text_area.pack(expand=True, fill='both')

        self.scroll_bar = Scrollbar(self.text_area)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_bar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scroll_bar.set)

        self.setup_menu()

        self.text_area.bind("<Control-Return>", self.handle_question)

    def setup_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_application)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About Notepad", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

    def quit_application(self):
        self.root.destroy()

    def show_about(self):
        messagebox.showinfo("Notepad", "Created by: Microsoft")

    def open_file(self):
        file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[
                                          ("All Files", "*.*"), ("Text Documents", "*.txt")])

        if file == "":
            return

        self.root.title(os.path.basename(file) + " - Notepad")
        with open(file, "r") as f:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.INSERT, f.read())

    def new_file(self):
        self.root.title("Untitled - Notepad")
        self.text_area.delete(1.0, tk.END)

    def save_file(self):
        file = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[
                                            ("All Files", "*.*"), ("Text Documents", "*.txt")])

        if file == "":
            return

        with open(file, "w") as f:
            f.write(self.text_area.get(1.0, tk.END))

        self.root.title(os.path.basename(file) + " - Notepad")

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def handle_question(self, event):
        text = self.text_area.get("1.0", tk.END).strip()
        if text.startswith('-'):
            question = text.lstrip('-').strip()
            
            if question.startswith(">>"):
                context = self.extract_context(question)
                self.continue_conversation(context)
            else:
                self.start_new_conversation(question)

    def extract_context(self, question):
        return question[2:]  # Remove the continuation indicator

    def start_new_conversation(self, question):
        self.text_area.insert(tk.END, "\n...")
        self.conversation_context = []  # Clear previous context
        self.continue_conversation(question)

    def continue_conversation(self, question):
        if self.conversation_context:
            previous_context = " ".join(self.conversation_context)
            question = f"{previous_context} {question}"
        def insert_answer():
            try:
                response = self.generate_text(prompt=question)
                self.text_area.insert(tk.END, f"\nResponse: {response}\n")
                self.conversation_context.append(question)  # Update conversation context
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        threading.Thread(target=insert_answer).start()

    def generate_text(self, prompt):
        try:
            model = genai.GenerativeModel(model_name="gemini-pro")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception("An error occurred during text generation:", e)


def setup_gemini():
    try:
        gemini_api_key = 'YOUR-API-KEY' #Replace with your API Key

        if gemini_api_key is None:
            raise Exception("GEMINI_API_KEY is not set")
        
        genai.configure(api_key=gemini_api_key)
    except Exception as e:
        raise Exception("An error occurred during setup:", e)


def run_notepad():
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        setup_gemini()
        run_notepad()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
