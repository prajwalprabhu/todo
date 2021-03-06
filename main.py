import tkinter as tk
from json import load, dump
import pickle as pick


class todo():
    def __init__(self):
        self.root = tk.Tk()
        self.load_passwd()

    def passwd_checked(self):
        self.list_todo()
        self.print_todo()
        self.todo_button = tk.Button(text="Add Todo", command=self.add_todo)
        self.todo_dele_button = tk.Button(
            text="Delete Todo", command=self.delete_todo)
        self.todo_button.grid(row=self.row_+1, column=0)
        self.todo_dele_button.grid(row=self.row_+2, column=0)
        self.root.bind("<Control-n>", self.add_todo)
        self.root.bind("<Control-q>", self.close)
        self.root.mainloop()

    def add_todo(self, event: None):
        self.window = tk.Toplevel(self.root)
        tk.Label(self.window, text="Title").pack()
        self.title = tk.Entry(self.window)
        self.title.pack()
        tk.Label(self.window, text="Date").pack()
        self.date = tk.Entry(self.window)
        self.date.pack()
        tk.Label(self.window, text="Comment").pack()
        self.comment = tk.Entry(self.window)
        self.comment.pack()
        tk.Button(self.window, text="Save", command=self.save_todo).pack()

    def save_todo(self):
        data_ = {"title": self.title.get(), "date": self.date.get(),
                 "comment": self.comment.get()}
        self.data.append(data_)
        self.dump_data()
        item = data_
        if self.column_ == 2:
            self.column_ = 0
            self.row_ += 1
        frame = tk.Frame(self.root)
        frame.grid(row=self.row_, column=self.column_)
        self.column_ += 1
        tk.Label(frame, text="Title:"+item["title"]+"\n").pack()
        tk.Label(frame, text="Comment:"+item["comment"]).pack()
        tk.Label(frame, text="Date:"+item["date"]).pack()
        tk.Label(frame, text="--"*20).pack()
        self.frame_list.append(frame)
        self.window.destroy()
        self.todo_button.destroy()
        self.todo_dele_button.destroy()
        self.todo_button = tk.Button(text="Add Todo", command=self.add_todo)
        self.todo_dele_button = tk.Button(
            text="Delete Todo", command=self.delete_todo)
        self.todo_button.grid(row=self.row_+1, column=0)
        self.todo_dele_button.grid(row=self.row_+2, column=0)

    def delete_todo(self):
        def delete():
            item = self.delete_todo_list_box.curselection()[0]
            self.data.pop(item)
            self.dump_data()
            self.delete_todo_list_box.delete(item)
            frame = self.frame_list.pop(item)
            frame.destroy()
            self.refresh()
        self.delete_window = tk.Toplevel(self.root)
        self.delete_todo_list_box = tk.Listbox(self.delete_window)
        self.delete_todo_list_box.pack()
        for item in self.data:
            self.delete_todo_list_box.insert(tk.END, item["title"])

        delete_button = tk.Button(
            self.delete_window, text="Delete", command=delete)
        delete_button.pack()

    def dump_data(self):
        with open("todo.json", "w") as f:
            dump(self.data, f, indent=4)

    def print_todo(self):
        self.row_ = 0
        self.column_ = 0
        self.frame_list = []
        for item in self.data:
            frame = tk.Frame(self.root)
            frame.grid(row=self.row_, column=self.column_)
            tk.Label(frame, text="Title:"+item["title"]+"\n").pack()
            tk.Label(frame, text="Comment:"+item["comment"]).pack()
            tk.Label(frame, text="Date:"+item["date"]).pack()
            tk.Label(frame, text="--"*20).pack()
            self.frame_list.append(frame)
            # row_+=1
            if self.column_ == 1:
                self.column_ = 0
                self.row_ += 1
            else:
                self.column_ += 1

    def list_todo(self):
        try:
            with open("todo.json", "rb") as f:
                self.data = load(f)
        except:
            self.data = [{"title": "", "comment": "", "date": ""}]
            self.dump_data()
            self.list_todo()
        self.number = len(self.data)

    def refresh(self):
        for frame in self.frame_list:
            frame.destroy()
        self.print_todo()

    def load_passwd(self):
        try:
            with open("password.todo", "rb") as f:
                try:
                    self.passwd = pick.load(f)
                    self.check_passwd()
                except Exception as err:
                    self.get_passwd()
        except:
            self.get_passwd()

    def dump_passwd(self):
        with open("password.todo", "wb") as f:
            pick.dump(self.passwd, f)

    def get_passwd(self):
        def get():
            self.passwd = self.passwd_entry.get()
            self.dump_passwd()
            window.destroy()
        window = tk.Toplevel(self.root)
        window.title = "Password"
        tk.Label(window, text="Enter Password").pack()
        self.passwd_entry = tk.Entry(window, show="*")
        self.passwd_entry.pack()
        tk.Button(window, text="Save", command=get).pack()

    def close(self, event: None):
        print("close")
        self.dump_data()
        self.root.destroy()

    def check_passwd(self):
        def check():
            if enterd.get() == self.passwd:
                window.destroy()
                self.passwd_checked()

            else:
                tk.Label(window, text="Wrong Password Try again").pack()
        window = tk.Tk()
        tk.Label(window, text="Enter Password").pack()
        enterd = tk.Entry(window, show="*")
        enterd.pack()
        tk.Button(window, text="Check", command=check).pack()
        window.mainloop()


# todo().cli()
todo()
