from tkinter import Tk, Label, Button, Frame, StringVar, Entry, TOP, LEFT, X
from main import run_setup, run_loop, save_file
from threading import Thread, Event

class respiration_gui:
    def __init__(self, master):
        # Initialize gui object.
        self.master = master
        master.title("Respiration")
        master.wm_iconbitmap('mouse_face.ico')

        # Set custom size and make non-resizable (for simplicity).
        master.geometry('500x75')
        master.resizable(False, False)
        master.update()

        # Create threads for stop button.
        self.main_thread = None
        self.stop_thread = Event()

        # Create time variable.
        self.start_time = None

        # Variables to hold workbook, arduino, filename.
        self.workbook = None
        self.arduino = None
        self.filename = None

        # Add top label.
        main_text = "BISL Rodent Respiration Tracker v1.0.0. Press Start to begin."
        self.label = Label(master, text=main_text)
        self.label.pack(fill=X, side=TOP)

        # Add input dialog for interval setting.
        self.middle = Frame(master)
        self.middle.pack()
        self.entry_label = Label(master, text='Data collection interval (min):')
        text_var = StringVar()
        self.entry = Entry(master, width=10, textvariable=text_var)
        text_var.set('1') # Default interval time (1 minute).
        self.entry_label.pack(in_=self.middle, side=LEFT)
        self.entry.pack(in_=self.middle, side=LEFT)

        # Add start button.
        self.start_button = Button(master, text="Start", command=self.begin)
        self.start_button.pack()

    def begin(self):
        # call initialization.
        proceed = run_setup(self)
        if proceed:
            # Disable entry
            self.entry['state'] = 'disabled'
            # Clear event to continue.
            self.stop_thread.clear()
            # Create thread to allow interrupt.
            self.main_thread = Thread(target=run_loop,args=(self,))
            self.main_thread.start()

    def update_label(self, new_message):
        # Change text in main label to give progress or instructions.
        self.label['text'] = new_message
        # Update gui to show change.
        self.master.update()

    def update_button(self, new_message, update_func):
        # Update button based on context.
        self.start_button['text'] = new_message
        if update_func:
            # Set command to be interrupt.
            self.start_button['command'] = self.finish
        # Update gui to show change.
        self.master.update()

    def disable_button(self):
        self.start_button['state'] = 'disabled'
        self.master.update()
    
    def enable_button(self):
        self.start_button['state'] = 'normal'
        self.master.update()
    
    def finish(self):
        # Break loop with event.
        self.stop_thread.set()
        self.main_thread.join()
        self.main_thread = None
        # Save file in case there were any updates that got missed.
        save_file(self.workbook, self.filename)
        self.update_label('Finished :)')
        self.entry['state'] = 'normal'
        self.start_button['command'] = self.begin
        self.update_button('Restart', False)

    def return_interval(self):
        # Parse input for interval.
        try:
            return int(self.entry.get())
        except ValueError:
            # Only allow minute intervals for simplicity.
            self.update_label('Invalid Interval Value (Must be an integer).')
    

# Init object.
root = Tk()
my_gui = respiration_gui(root)
root.mainloop()