import tkinter as tk
# from tkinter import ttk
from tkinter import scrolledtext

import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.widgets import Floodgauge, Meter

import matplotlib.pyplot as plt
import random
from Visual_grid import visuel_grid
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window = ttk.Window(themename='journal')
window.title('KITT GUI')
window.iconbitmap('rc-car.ico')

#window sizes and location
window_width = 800
window_height = 500
display_width = window.winfo_width()
display_height = window.winfo_height()

left = int(display_width / 2 - window_width / 2 )
top = int(display_height / 2 - window_height / 2)

window.geometry(f'{window_width}x{window_height}+{left}+{top}')
window.minsize(400,400)

#window atributes
window.attributes('-topmost',True)

#security event
window.bind('<Escape>', lambda event: window.quit())

#main layout widgets
frame1 = ttk.Frame(window, relief='raised', borderwidth=1)
frame2 = ttk.Frame(window, relief='raised', borderwidth=1)

#main place layout
frame1.place(x = 0, y = 0, relwidth = 0.4, relheight = 1)
frame2.place(relx= 0.4, y = 0, relwidth = 0.6, relheight = 1)


#frame1 layout and place
frame1_1 = ttk.Frame(frame1, relief='raised', borderwidth=1)
frame1_2 = ttk.Frame(frame1, relief='raised', borderwidth=1)
frame1_1.place(x = 0, y = 0, relwidth = 1, relheight = 0.3)
frame1_2.place(x = 0, rely=0.3, relwidth = 1, relheight = 0.7)

#frame2 layout and place
frame2_1 = ttk.Frame(frame2, relief='raised', borderwidth=1)
frame2_2 = ttk.Frame(frame2, relief='raised', borderwidth=1)
frame2_1.place(x = 0, y = 0, relwidth = 1, relheight = 0.3)
frame2_2.place(x= 0, rely=0.3, relwidth = 1, relheight = 0.7)

ttk.Label(frame2_2, background='black').pack(expand=True,fill='both')

#frame1_1 layout and place
frame1_1.columnconfigure(0, weight=1)
frame1_1.columnconfigure(1, weight=1)
frame1_1.rowconfigure(0, weight=1 , uniform='a')
frame1_1.rowconfigure(1, weight=1, uniform='a')
frame1_1.rowconfigure(2, weight=1, uniform='a')
frame1_1.rowconfigure(3, weight=1, uniform='a')
frame1_1.rowconfigure(4, weight=1, uniform='a')

#frame1_1 widgets
label1= ttk.Label(frame1_1,background='green')
label1.grid(row=0,column=0)
label2= ttk.Label(frame1_1,background='black')
label2.grid(row=0,column=1)
label3= ttk.Label(frame1_1,background='blue')
label3.grid(row=1,column=0)
label4= ttk.Label(frame1_1,background='yellow')
label4.grid(row=1,column=1)
label5= ttk.Label(frame1_1,background='purple')
label5.grid(row=2,column=0)
label6= ttk.Label(frame1_1,background='lightblue')
label6.grid(row=2,column=1)
label7= ttk.Label(frame1_1,background='red')
label7.grid(row=3,column=0)
label8= ttk.Label(frame1_1,background='limegreen')
label8.grid(row=3,column=1)
label9= ttk.Label(frame1_1,background='orange')
label9.grid(row=4,column=0)
label10= ttk.Label(frame1_1,background='darkblue')
label10.grid(row=4,column=1)

Comport = ttk.Combobox(frame1_1)
Comport['values'] = ('Comport 1','Comport 2','Comport 3','Comport 4','Comport 5','Comport 6','Comport 7','Comport 8','Comport 9')
Comport.set('Select Comport')  # Set default text
Comport.grid(row=0, column=0, padx=5, pady=2,sticky='w')
#
# Create a KITT_connect switch widget
connect_label = ttk.Label(frame1_1, text="Connect")
connect_label.grid(row=0, column=1, padx=5, pady=2, sticky='w')

KITT_connect = ttk.Checkbutton(
        frame1_1,
        bootstyle="success-round-toggle"
                )
KITT_connect.grid(row=0, column=1, padx=5, pady=2, sticky='e')

# Create a real_or_sim switch widget
real_or_sim_label = ttk.Label(frame1_1, text="Simulation")
real_or_sim_label.grid(row=2, column=1, padx=5, pady=2, sticky='w')
real_or_sim = ttk.Checkbutton(
        frame1_1,
        bootstyle="success-round-toggle"
                )
real_or_sim.grid(row=2, column=1, padx=5, pady=2, sticky='e')
#

radio1 = ttk.Radiobutton(frame1_1, text='Manual mode', value='Manual mode')
radio1.grid(row=1, column=0, padx=10, pady=2,sticky='nesw')
radio2 = ttk.Radiobutton(frame1_1, text='Challenge A', value='Challenge A')
radio2.grid(row=2, column=0, padx=10, pady=2, sticky='nesw')
radio3 = ttk.Radiobutton(frame1_1, text='Challenge B', value='Challenge B')
radio3.grid(row=3, column=0, padx=10, pady=2,sticky='nesw')
radio4 = ttk.Radiobutton(frame1_1, text='Challenge C', value='Challenge C')
radio4.grid(row=4, column=0, padx=10, pady=2,sticky='nesw')




#frame1_2 layout and place
frame1_2.columnconfigure((0,1),weight = 1, uniform='b')
frame1_2.rowconfigure((0,1,2,3), weight= 1,uniform='b')

#frame1_2 widgets
frame1_2_input_data = ttk.Frame(frame1_2, relief='raised', borderwidth=1)
frame1_2_input_data.grid(row = 0,column=0,rowspan=3,columnspan=2,sticky='nesw')
#
frame1_2_input_data_start = ttk.Frame(frame1_2_input_data, relief='raised', borderwidth=1)
frame1_2_input_data_start.place(x = 0, y = 0, relwidth = 1, relheight = 0.18)

frame1_2_input_data_end = ttk.Frame(frame1_2_input_data, relief='raised', borderwidth=1)
frame1_2_input_data_end.place(x = 0, rely = 0.18, relwidth = 1, relheight = 0.18)
#
frame1_2_input_data_waypoint = ttk.Frame(frame1_2_input_data, relief='raised', borderwidth=1)
frame1_2_input_data_waypoint.place(x = 0, rely = 0.36, relwidth = 1, relheight = 0.18)
#
frame1_2_input_data_obstacle = ttk.Frame(frame1_2_input_data, relief='raised', borderwidth=1)
frame1_2_input_data_obstacle.place(x = 0, rely = 0.54, relwidth = 1, relheight = 0.46)
#
frame1_2_input_data_start.columnconfigure((0,1),weight = 1, uniform='c')
frame1_2_input_data_start.rowconfigure((0,1), weight= 1, uniform='d')

frame1_2_input_data_end.columnconfigure((0,1),weight = 1, uniform='c')
frame1_2_input_data_end.rowconfigure((0,1), weight= 1, uniform='d')
#
frame1_2_input_data_waypoint.columnconfigure((0,1),weight = 1, uniform='c')
frame1_2_input_data_waypoint.rowconfigure((0,1), weight= 1, uniform='d')
#
frame1_2_input_data_obstacle.columnconfigure((0,1),weight = 1, uniform='c')
frame1_2_input_data_obstacle.rowconfigure((0,1,2,3,4), weight= 1, uniform='d')
#
starting_point_label = ttk.Label(frame1_2_input_data_start, text = 'Start position',background='lightblue')
starting_point_label.grid(row=0,column=0, padx=10, pady=2,sticky='w')
textbox_starting_x = ttk.Entry(frame1_2_input_data_start,background='blue')
textbox_starting_x.grid(row=1,column=0, padx=1, pady=1)
textbox_starting_y = ttk.Entry(frame1_2_input_data_start,background='blue')
textbox_starting_y.grid(row=1,column=1, padx=1, pady=1)

labeli1= ttk.Label(frame1_2_input_data_start,background='green')
labeli1.grid(row=0,column=0)
labeli2= ttk.Label(frame1_2_input_data_start,background='black')
labeli2.grid(row=0,column=1)
labeli3= ttk.Label(frame1_2_input_data_start,background='blue')
labeli3.grid(row=1,column=0)
labeli4= ttk.Label(frame1_2_input_data_start,background='yellow')
labeli4.grid(row=1,column=1)

end_point_label = ttk.Label(frame1_2_input_data_end, text = 'End position')
end_point_label.grid(row=0,column=0, padx=10, pady=2,sticky='w')
textbox_end_x = ttk.Entry(frame1_2_input_data_end)
textbox_end_x.grid(row=1,column=0, padx=1, pady=1)
textbox_end_y = ttk.Entry(frame1_2_input_data_end)
textbox_end_y.grid(row=1,column=1, padx=1, pady=1)
#
waypoint_label = ttk.Label(frame1_2_input_data_waypoint, text = 'Waypoint')
waypoint_label.grid(row=0,column=0, padx=10, pady=2,sticky='w')
textbox_waypoint_x = ttk.Entry(frame1_2_input_data_waypoint)
textbox_waypoint_x.grid(row=1,column=0, padx=1, pady=1)
textbox_waypoint_y = ttk.Entry(frame1_2_input_data_waypoint)
textbox_waypoint_y.grid(row=1,column=1, padx=1, pady=1)

obstacles_location_label = ttk.Label(frame1_2_input_data_obstacle, text = 'Location Obstacles ')
obstacles_location_label.grid(row=0,column=0, padx=10, pady=2,sticky='w')
textbox_obstacle1_x = ttk.Entry(frame1_2_input_data_obstacle)
textbox_obstacle1_x.grid(row=1,column=0, padx=1, pady=1)
textbox_obstacle1_y = ttk.Entry(frame1_2_input_data_obstacle)
textbox_obstacle1_y.grid(row=1,column=1, padx=1, pady=1)
textbox_obstacle2_x = ttk.Entry(frame1_2_input_data_obstacle)
textbox_obstacle2_x.grid(row=2,column=0, padx=1, pady=1)
textbox_obstacle2_y = ttk.Entry(frame1_2_input_data_obstacle)
textbox_obstacle2_y.grid(row=2,column=1, padx=1, pady=1)
textbox_obstacle3_x = ttk.Entry(frame1_2_input_data_obstacle)
textbox_obstacle3_x.grid(row=3,column=0, padx=1, pady=1)
textbox_obstacle3_y = ttk.Entry(frame1_2_input_data_obstacle)
textbox_obstacle3_y.grid(row=3,column=1, padx=1, pady=1)
textbox_obstacle4_x = ttk.Entry(frame1_2_input_data_obstacle)
textbox_obstacle4_x.grid(row=4,column=0, padx=1, pady=1)
textbox_obstacle4_y = ttk.Entry(frame1_2_input_data_obstacle)
textbox_obstacle4_y.grid(row=4,column=1, padx=1, pady=1)


button_Start_reset = ttk.Button(frame1_2, text = 'Start/reset')
button_Set_Settings = ttk.Button(frame1_2, text = 'Set Settings')
button_Start_reset.grid(row=3,column=0)
button_Set_Settings.grid(row=3,column=1)

timer = ttk.Label(frame1_2, text= "Timer value")
timer.grid(row=4,column=0,columnspan=2,sticky='n')


#frame2_1 layout and place
frame2_1.columnconfigure((0,1),weight = 1, uniform='e')
frame2_1.rowconfigure(0, weight= 2,uniform='f')
frame2_1.rowconfigure(1, weight= 3,uniform='f')


labelw1= ttk.Label(frame2_1,background='green')
labelw1.grid(row=0,column=0,sticky='news')
labelw2= ttk.Label(frame2_1,background='black')
labelw2.grid(row=0,column=1,sticky='news')
labelw3= ttk.Label(frame2_1,background='blue')
labelw3.grid(row=1,column=0,sticky='news')
labelw4= ttk.Label(frame2_1,background='yellow')
labelw4.grid(row=1,column=1,sticky='news')

#frame2_1 widgets

#speed inidicator
speed = ttk.Meter(
    frame2_1,
    amounttotal = 25,
    amountused = 10,
    metertype = 'semi',
    textfont = '-size 12',
    subtext = 'Km/h',
    subtextfont ='-size 6',
    metersize= 75
)
speed.grid(row=0,column=0,sticky='n')

#battery value
battery_value_int = tk.IntVar(value =50)
battery_level = ttk.Floodgauge(
    frame2_1,
    variable = battery_value_int,
    mask = '{}%'
 )
battery_level.grid(row=0,column=1, padx=10, pady=2)

# Create a scrolled_Text widget for displaying output data
message_output_text_field = ScrolledText(frame2_1,autohide=True) #text = 'welcome to KITT, select mode and fill in variables'
message_output_text_field.grid(row=1,column=0,columnspan=2, padx=10, pady=2)


#frame2_2 widgets
# Create a FigureCanvasTkAgg object to display the plot
canvas = FigureCanvasTkAgg(visuel_grid(), master=frame2_2)
canvas.draw()
canvas.get_tk_widget().pack(fill='both')



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Widgets
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#



#
# switch = ctk.CTKSwitch(
#     window,
#     text = 'Connect with KITT',
#     fg_color = ('red','red'),
#     progress_color = ('green','green'))
# switch.pack()
#switch_width
#switch_height








def button():
    pass


# #create widgets
# info_frame = ttk.Frame(master= window)
# entry = ttk.Entry(master= window)
# button = ttk.Button(master = window, text = 'test', command= button)
#
# #radiobutton
# radio1 = ttk.Radiobutton(window, text = 'Manual mode', value= 'Manual mode')
# radio1.pack()
# radio2 = ttk.Radiobutton(window, text = 'Challenge A', value= 'Challenge A')
# radio2.pack()
# radio3 = ttk.Radiobutton(window, text = 'Challenge B', value= 'Challenge B')
# radio3.pack()
# radio4 = ttk.Radiobutton(window, text = 'Challenge C', value= 'Challenge C')
# radio4.pack()
#
#
# info_frame.pack()
# button.pack()
# entry.pack()





#events
# window.bind('<KeyPress-W')
# window.bind('<KeyPress-A')
# window.bind('<KeyPress-D')
# window.bind('<KeyPress-S')

# def update_text():
#     output_data = "This is the output data"
#     text_field.delete("1.0", tk.END)  # Clear the existing text
#     text_field.insert(tk.END, output_data)  # Insert the new output data
#
#
#
#
# # Create a button to trigger the update of the output data
# update_button = tk.Button(window, text="Update", command=update_text)
# update_button.pack()
#
#
#
# #progress bar
# batery_level = ttk.Progressbar(window, variable = 70, maximum= 100)
# batery_level.pack()

#run
window.mainloop()

# class GUI(tk.Tk):
#     def __init__(self):
#         #main set up
#         super().__init__()
#         self.title('KITT GUI')
#         self.minsize(400,400)
#
#         # widgets
#
#         # Create a FigureCanvasTkAgg object to display the plot
#         canvas = FigureCanvasTkAgg(visuel_grid(), master=self)
#         canvas.draw()
#         canvas.get_tk_widget().pack()
#
#         #run
#         self.mainloop()
# GUI()

#window