import tkinter as tk
from tkinter import scrolledtext
import time

start_time = 0
challenge_completed = False

import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.widgets import Floodgauge, Meter

from visual_grid import visuel_grid
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# def GUI():
# Update combobox state based on selected comport
def update_combobox_state(*args):
    comport = selected_combox_value.get()

    if comport == 'Select Comport':
        KITT_connect.config(state='disabled')
    else:
        KITT_connect.config(state='normal')

def kitt_switch():#still need to add functionalities that check of the kitt is connected
    comport = selected_combox_value.get()

    if comport == 'Select Comport':
        print("Error: Comport not selected")
        return

    state_kitt_switch = KITT_connent_state.get()

    if state_kitt_switch:
        print("Checkbutton is selected")
        Comport.config(state='disabled')
    else:
        print("Checkbutton is not selected")
        Comport.config(state='normal')

    print("Switch state:", state_kitt_switch)
    print(comport)
    return comport
    # comport['state'] = 'disabled'
    # selected_value_combobox = comport.get()


def retrieve_entry_data():
    orientation = textbox_starting_orientation.get()
    starting_x = textbox_starting_x.get()
    starting_y = textbox_starting_y.get()
    end_x = textbox_end_x.get()
    end_y = textbox_end_y.get()
    waypoint_x = textbox_waypoint_x.get()
    waypoint_y = textbox_waypoint_y.get()
    obstacle1_x = textbox_obstacle1_x.get()
    obstacle1_y = textbox_obstacle1_y.get()
    obstacle2_x = textbox_obstacle2_x.get()
    obstacle2_y = textbox_obstacle2_y.get()
    obstacle3_x = textbox_obstacle3_x.get()
    obstacle3_y = textbox_obstacle3_y.get()
    obstacle4_x = textbox_obstacle4_x.get()
    obstacle4_y = textbox_obstacle4_y.get()

    print("Starting Position x,y,teta:", starting_x, starting_y,orientation)
    print("End Position:", end_x, end_y)
    print("Waypoint:", waypoint_x, waypoint_y)
    print("Obstacle 1:", obstacle1_x, obstacle1_y)
    print("Obstacle 2:", obstacle2_x, obstacle2_y)
    print("Obstacle 3:", obstacle3_x, obstacle3_y)
    print("Obstacle 4:", obstacle4_x, obstacle4_y)

    # Call the visuel_grid function with the retrieved data
    # visuel_grid(starting_x, starting_y, orientation, waypoint_x, waypoint_y, end_x, end_y)

    return orientation,starting_x,starting_y,end_x, end_y, waypoint_x,waypoint_y,obstacle1_x, obstacle1_y, obstacle2_x, obstacle2_y, obstacle3_x, obstacle3_y, obstacle4_x, obstacle4_y

def set_button():
    error = False
    # Retrieve the selected radio button value
    selected_mode = selected_radio_value.get()
    if not selected_mode:
        print("No mode selected")
        output_text_var.set("No mode selected")
        message_output_text_field.delete("1.0", tk.END)  # Clear the current text
        message_output_text_field.insert(tk.END, output_text_var.get())  # Update with the new value
        error = True
    else:
        print("Selected value:", selected_mode)
        output_text_var.set(f"Mode {selected_mode} selected")
        message_output_text_field.delete("1.0", tk.END)  # Clear the current text
        message_output_text_field.insert(tk.END, output_text_var.get())  # Update with the new value
        error = False

    state_real_or_sim = real_or_sim_state.get()
    if state_real_or_sim:
        print("Simulation mode")
    else:
        if KITT_connent_state.get() == False:
            print('Connect kitt')
            output_text_var.set(f"Connect KITT for Physical mode")
            message_output_text_field.delete("1.0", tk.END)  # Clear the current text
            message_output_text_field.insert(tk.END, output_text_var.get())  # Update with the new value
            error = True
        print("Physical mode")

    orientation, starting_x, starting_y, end_x, end_y, waypoint_x, waypoint_y, obstacle1_x, obstacle1_y, obstacle2_x, obstacle2_y, obstacle3_x, obstacle3_y, obstacle4_x, obstacle4_y = retrieve_entry_data()

    if error == False:
        all_widgets = [radio1, radio2, radio3, radio4,KITT_connect, real_or_sim,textbox_starting_orientation,
            textbox_starting_x, textbox_starting_y,
            textbox_end_x, textbox_end_y,
            textbox_waypoint_x, textbox_waypoint_y,
            textbox_obstacle1_x, textbox_obstacle1_y,
            textbox_obstacle2_x, textbox_obstacle2_y,
            textbox_obstacle3_x, textbox_obstacle3_y,
            textbox_obstacle4_x, textbox_obstacle4_y,
            starting_point_label, end_point_label, waypoint_label, obstacles_location_label]
        for widget in all_widgets:
            widget.config(state="disabled")

        button_Set_reset.config(text='Reset', command=reset_button)

    # Code to set the settings
    return error, selected_mode,state_real_or_sim,orientation,starting_x,starting_y,end_x, end_y, waypoint_x,waypoint_y,obstacle1_x, obstacle1_y, obstacle2_x, obstacle2_y, obstacle3_x, obstacle3_y, obstacle4_x, obstacle4_y


def start_timer():
    global start_time, challenge_completed
    start_time = time.time()  # Get the current time
    challenge_completed = False
    update_timer()

def reset_timer():
    global start_time, challenge_completed
    start_time = 0
    challenge_completed = False
    timer.config(text="00:00:0")

def update_timer():
    global start_time, challenge_completed
    if challenge_completed:
        return

    current_time = time.time()
    elapsed_time = current_time - start_time

    # Convert elapsed time to minutes, seconds, and tenths of a second
    minutes = int(elapsed_time / 60)
    seconds = int(elapsed_time % 60)
    tenths = int((elapsed_time * 10) % 10)

    # Display the timer in the desired format
    timer.config(text=f"{minutes:02}:{seconds:02}:{tenths}")

    # Update the GUI to refresh the timer display
    window.update()

    # Schedule the next timer update (every 100 milliseconds)
    window.after(100, update_timer)
def start_button(error,select_mode):
    run = True
    if error == False:
        if select_mode != 'Manual mode':
            start_timer()
    return run



def reset_button():
    # Code to reset the settings
    all_widgets = [radio1, radio2, radio3, radio4, KITT_connect, real_or_sim,textbox_starting_orientation,
                   textbox_starting_x, textbox_starting_y,
                   textbox_end_x, textbox_end_y,
                   textbox_waypoint_x, textbox_waypoint_y,
                   textbox_obstacle1_x, textbox_obstacle1_y,
                   textbox_obstacle2_x, textbox_obstacle2_y,
                   textbox_obstacle3_x, textbox_obstacle3_y,
                   textbox_obstacle4_x, textbox_obstacle4_y,
                   starting_point_label, end_point_label, waypoint_label, obstacles_location_label]
    for widget in all_widgets:
        widget.config(state="normal")

    output_text_var.set("Welcome to KITT, select mode and fill in variables!")
    message_output_text_field.delete("1.0", tk.END)  # Clear the current text
    message_output_text_field.insert(tk.END, output_text_var.get())  # Update with the new value

    selected_radio_value.set("")  # Clear the selected value
    reset_timer()

    button_Set_reset.config(text='Set Settings', command=set_button)


window = ttk.Window()#themename='journal'
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
frame1_1 = ttk.Frame(frame1)#, relief='raised', borderwidth=1
frame1_2 = ttk.Frame(frame1)#, relief='raised', borderwidth=1
frame1_1.place(x = 0, y = 0, relwidth = 1, relheight = 0.3)
frame1_2.place(x = 0, rely=0.3, relwidth = 1, relheight = 0.7)

#frame2 layout and place
frame2_1 = ttk.Frame(frame2)#, relief='raised', borderwidth=1
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
# label1= ttk.Label(frame1_1,background='green')
# label1.grid(row=0,column=0)
# label2= ttk.Label(frame1_1,background='black')
# label2.grid(row=0,column=1)
# label3= ttk.Label(frame1_1,background='blue')
# label3.grid(row=1,column=0)
# label4= ttk.Label(frame1_1,background='yellow')
# label4.grid(row=1,column=1)
# label5= ttk.Label(frame1_1,background='purple')
# label5.grid(row=2,column=0)
# label6= ttk.Label(frame1_1,background='lightblue')
# label6.grid(row=2,column=1)
# label7= ttk.Label(frame1_1,background='red')
# label7.grid(row=3,column=0)
# label8= ttk.Label(frame1_1,background='limegreen')
# label8.grid(row=3,column=1)
# label9= ttk.Label(frame1_1,background='orange')
# label9.grid(row=4,column=0)
# label10= ttk.Label(frame1_1,background='darkblue')
# label10.grid(row=4,column=1)

selected_combox_value = tk.StringVar()
Comport = ttk.Combobox(frame1_1,textvariable=selected_combox_value)
Comport['values'] = ('Comport 1','Comport 2','Comport 3','Comport 4','Comport 5','Comport 6','Comport 7','Comport 8','Comport 9')
Comport.set('Select Comport')  # Set default text
Comport.grid(row=0, column=0, padx=5, pady=2,sticky='w')
#
# Create a KITT_connect switch widget
connect_label = ttk.Label(frame1_1, text="Connect")
connect_label.grid(row=0, column=1, padx=5, pady=2, sticky='w')

KITT_connent_state = tk.BooleanVar()
KITT_connect = ttk.Checkbutton(
        frame1_1,
        bootstyle = "success-round-toggle",
        command= kitt_switch,
        variable=KITT_connent_state
                )
# Add callback to update combobox state when the selected value changes
selected_combox_value.trace('w', update_combobox_state)

# Initial state of the combobox
update_combobox_state()
KITT_connect.grid(row=0, column=1, padx=5, pady=2, sticky='e')

# Create a real_or_sim switch widget
real_or_sim_state = tk.BooleanVar()
real_or_sim_label = ttk.Label(frame1_1, text="Simulation")
real_or_sim_label.grid(row=2, column=1, padx=5, pady=2, sticky='w')
real_or_sim = ttk.Checkbutton(
        frame1_1,
        bootstyle = "success-round-toggle",
        variable = real_or_sim_state
                )
real_or_sim.grid(row=2, column=1, padx=5, pady=2, sticky='e')
#

selected_radio_value = tk.StringVar()

radio1 = ttk.Radiobutton(frame1_1, text='Manual mode', value='Manual mode', variable=selected_radio_value)
radio1.grid(row=1, column=0, padx=10, pady=2, sticky='nesw')
radio2 = ttk.Radiobutton(frame1_1, text='Challenge A', value='Challenge A', variable=selected_radio_value)
radio2.grid(row=2, column=0, padx=10, pady=2, sticky='nesw')
radio3 = ttk.Radiobutton(frame1_1, text='Challenge B', value='Challenge B', variable=selected_radio_value)
radio3.grid(row=3, column=0, padx=10, pady=2, sticky='nesw')
radio4 = ttk.Radiobutton(frame1_1, text='Challenge C', value='Challenge C', variable=selected_radio_value)
radio4.grid(row=4, column=0, padx=10, pady=2, sticky='nesw')

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

initial_text = "Orientation"
textbox_starting_orientation = ttk.Entry(frame1_2_input_data_start,background='blue')
textbox_starting_orientation.insert(tk.END, initial_text)
textbox_starting_orientation.grid(row=0,column=1, padx=1, pady=1)

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


button_Start = ttk.Button(frame1_2, text = 'Start',command = start_button)
button_Set_reset = ttk.Button(frame1_2, text = 'Set Settings',command=set_button)
button_Start.grid(row=3,column=0)
button_Set_reset.grid(row=3,column=1)

timer = ttk.Label(frame1_2, text= "Timer 00:00:0")
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
output_text_var = tk.StringVar(value='Welcome to KITT, select mode and fill in variables!')
# Create a Text widget
message_output_text_field = scrolledtext.ScrolledText(frame2_1)

# Insert the value of the StringVar into the ScrolledText widget
message_output_text_field.insert(tk.END, output_text_var.get())
message_output_text_field.grid(row=1,column=0,columnspan=2, padx=10, pady=2)


#frame2_2 widgets
# Create a FigureCanvasTkAgg object to display the plot

canvas = FigureCanvasTkAgg(visuel_grid(),
                           master=frame2_2)
canvas.draw()
canvas.get_tk_widget().pack(side= 'top')


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
    # return

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