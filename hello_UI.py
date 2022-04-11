import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "hello_world.ui"


class HelloWorldApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('toplevel', master)
        self.output_label = builder.get_object('output_label', master)



        self.input_text = None
        self.output_text = None
        builder.import_variables(self, ['input_text', 'output_text'])

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def ok_click(self):
        if self.input_text.get().upper() == 'PASS':
            self.output_label['background'] = '#00ff00'
            self.output_text.set(self.input_text.get())
        elif self.input_text.get().upper() == 'FAIL':
            self.output_label['background'] = '#ff0000'
            self.output_text.set(self.input_text.get())
        else:
            self.output_label['background'] = '#ffff00'
            self.output_text.set(self.input_text.get())





if __name__ == '__main__':
    root = tk.Tk()
    app = HelloWorldApp(root)
    app.run()


