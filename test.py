import tkinter as tk

class GridDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid Display App")

        self.scrollable_frame = tk.Frame(self.root)
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=10)

        self.email_widgets = []

    def add_grid(self, email_content):
        frame = tk.Frame(self.scrollable_frame)
        frame.grid()

        text_widget = tk.Text(frame, wrap='none', height=5, width=30)
        text_widget.grid()

        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        scrollbar.grid()
        text_widget['yscrollcommand'] = scrollbar.set

        text_widget.insert('1.0', email_content)

        self.email_widgets.insert(0, frame)
        self.update_grid()

    def update_grid(self):
        num_columns = 3  # Change the number of columns as per your requirement
        for i, widget in enumerate(self.email_widgets):
            row = i // num_columns
            col = i % num_columns
            widget.grid(row=row, column=col, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = GridDisplayApp(root)

    # Add grids with content
    app.add_grid("Grid 1: This is the newest grid.")
    app.add_grid("Grid 2: This is another grid.")
    app.add_grid("Grid 3: Yet another grid.")
    app.add_grid("Grid 4: Oldest grid.")

    root.mainloop()
