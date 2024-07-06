import tkinter as tk

def switch_frame(frame):
    frame.tkraise()

def show_frame(frame):
    frame.tkraise()

root = tk.Tk()
root.geometry('500x400')
root.title('Tkinter Hub')

options_frame = tk.Frame(root, bg='#c3c3c3')
options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=100, height=400)

home_frame = tk.Frame(root, bg='white')
menu_frame = tk.Frame(root, bg='white')
contact_frame = tk.Frame(root, bg='white')
about_frame = tk.Frame(root, bg='white')

for frame in (home_frame, menu_frame, contact_frame, about_frame):
    frame.place(x=100, y=0, width=400, height=400)

home_btn = tk.Button(options_frame, text='Home', font=('Bold', 15),
                     fg='#158aff', bd=0, bg='#c3c3c3',
                     command=lambda: show_frame(home_frame))
home_btn.place(x=10, y=50)

menu_btn = tk.Button(options_frame, text='Menu', font=('Bold', 15),
                     fg='#158aff', bd=0, bg='#c3c3c3',
                     command=lambda: show_frame(menu_frame))
menu_btn.place(x=10, y=100)

contact_btn = tk.Button(options_frame, text='Contact', font=('Bold', 15),
                        fg='#158aff', bd=0, bg='#c3c3c3',
                        command=lambda: show_frame(contact_frame))
contact_btn.place(x=10, y=150)

about_btn = tk.Button(options_frame, text='About', font=('Bold', 15),
                      fg='#158aff', bd=0, bg='#c3c3c3',
                      command=lambda: show_frame(about_frame))
about_btn.place(x=10, y=200)

home_lbl = tk.Label(home_frame, text='Home Page', font=('Bold', 30))
home_lbl.pack(expand=True)

menu_lbl = tk.Label(menu_frame, text='Menu Page', font=('Bold', 30))
menu_lbl.pack(expand=True)

contact_lbl = tk.Label(contact_frame, text='Contact Page', font=('Bold', 30))
contact_lbl.pack(expand=True)

about_lbl = tk.Label(about_frame, text='About Page', font=('Bold', 30))
about_lbl.pack(expand=True)

home_frame.tkraise()

root.mainloop()
