import tkinter as tk
from tkinter import scrolledtext
import ttkbootstrap as ttk
# from ttkbootstrap.scrolled import ScrolledText

from visual_grid import visuel_grid
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




class GUI(tk.Tk):

    #data


    #     def start_button(self):
    #         print("Start button is pressed")
    #
    #     def set_reset_button(self):
    #         print(radio_var.get())
    #         button_Set_reset_Settings['text'] = 'Reset'
    #         button_Set_reset_Settings['command'] = reset
    #
    #         print("set/reset button is pressed")
    #
    # def reset():
    #     pass
    def __init__(self):
        #main setup GUI
        super().__init__()
        self.title('KITT GUI')
        self.iconbitmap('rc-car.ico')

        # window sizes and location
        window_width = 800
        window_height = 500
        display_width = self.winfo_width()
        display_height = self.winfo_height()

        left = int(display_width / 2 - window_width / 2)
        top = int(display_height / 2 - window_height / 2)

        self.geometry(f'{window_width}x{window_height}+{left}+{top}')
        self.minsize(400, 400)

        # window attributes
        self.attributes('-topmost', True)

        # security event
        self.bind('<Escape>', lambda event: self.quit())

        #data
        self.start_posx = tk.IntVar()
        self.start_posy = tk.IntVar()
        self.end_posx = tk.IntVar()
        self.end_posy = tk.IntVar()
        self.way_posx = tk.IntVar()
        self.way_posy = tk.IntVar()

        self.value_speed = tk.IntVar()
        self.battary_level = tk.InVar()


        #widgets
        self.frame1 = Frame1(self,
                             self.start_posx,
                             self.start_posy,
                             self.end_posx,
                             self.end_posy,
                             self.way_posx,
                             self.way_posy)
        self.frame2 = Frame2(self,
                             self.value_speed,
                             self.battary_level)

        #run
        self.mainloop()

        def kitt_switch(self):
            state = Frame1_1.KITT_connect.value()
            print("Switch state:", state)

            # comport['state'] = 'disabled'
            # selected_value_combobox = comport.get()
            # print(selected_value_combox)

class Frame1(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.place(x = 0, y = 0, relwidth = 0.4, relheight = 1)
        ttk.Frame(self, relief='raised', borderwidth=1)

        # widgets
        self.frame1_1 = Frame1_1(self)
        self.frame1_2 = Frame1_2(self)

class Frame1_1(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=0.3)
        ttk.Frame(self, relief='raised', borderwidth=1)

        self.create_widgets()

    def create_widgets(self):
        #create the widgets
        #comport combox
        comport = ttk.Combobox(self)
        comport['values'] = (
        'Comport 1', 'Comport 2', 'Comport 3', 'Comport 4', 'Comport 5', 'Comport 6', 'Comport 7', 'Comport 8',
        'Comport 9')
        comport.set('Select Comport')  # Set default text


        # Create a KITT_connect switch widget
        connect_label = ttk.Label(self, text="Connect")
        KITT_connect = ttk.Checkbutton(
            self,
            bootstyle="success-round-toggle",
            command = GUI.kitt_switch,
            onvalue = True,
            offvalue= False
        )



        # Create a real_or_sim switch widget
        real_or_sim_label = ttk.Label(self, text="Simulation")
        real_or_sim_label.grid(row=2, column=1, padx=5, pady=2, sticky='w')
        real_or_sim = ttk.Checkbutton(
            self,
            bootstyle="success-round-toggle"
        )

        #create radio buttons
        self.radio_var = tk.StringVar()
        radio1 = ttk.Radiobutton(self, text='Manual mode', value='Manual mode',variable=self.radio_var)
        radio2 = ttk.Radiobutton(self, text='Challenge A', value='Challenge A',variable=self.radio_var)
        radio3 = ttk.Radiobutton(self, text='Challenge B', value='Challenge B',variable=self.radio_var)
        radio4 = ttk.Radiobutton(self, text='Challenge C', value='Challenge C',variable=self.radio_var)

        #place the widgets
        # create the grid
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        # place the widgets
        comport.grid(row=0, column=0, padx=5, pady=2, sticky='w')

        connect_label.grid(row=0, column=1, padx=5, pady=2, sticky='w')
        KITT_connect.grid(row=0, column=1, padx=5, pady=2, sticky='e')

        real_or_sim_label.grid(row=2, column=1, padx=5, pady=2, sticky='w')
        real_or_sim.grid(row=2, column=1, padx=5, pady=2, sticky='e')

        radio1.grid(row=1, column=0, padx=10, pady=2, sticky='nesw')
        radio2.grid(row=2, column=0, padx=10, pady=2, sticky='nesw')
        radio3.grid(row=3, column=0, padx=10, pady=2, sticky='nesw')
        radio4.grid(row=4, column=0, padx=10, pady=2, sticky='nesw')

        # label1 = ttk.Label(self, background='green')
        # label1.grid(row=0, column=0)
        # label2 = ttk.Label(self, background='black')
        # label2.grid(row=0, column=1)
        # label3 = ttk.Label(self, background='blue')
        # label3.grid(row=1, column=0)
        # label4 = ttk.Label(self, background='yellow')
        # label4.grid(row=1, column=1)
        # label5 = ttk.Label(self, background='purple')
        # label5.grid(row=2, column=0)
        # label6 = ttk.Label(self, background='lightblue')
        # label6.grid(row=2, column=1)
        # label7 = ttk.Label(self, background='red')
        # label7.grid(row=3, column=0)
        # label8 = ttk.Label(self, background='limegreen')
        # label8.grid(row=3, column=1)
        # label9 = ttk.Label(self, background='orange')
        # label9.grid(row=4, column=0)
        # label10 = ttk.Label(self, background='darkblue')
        # label10.grid(row=4, column=1)
        return

class Frame1_2(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.place(x = 0, rely=0.3, relwidth = 1, relheight = 0.7)
        ttk.Frame(self, relief='raised', borderwidth=1)

        self.create_widgets()

    def create_widgets(self):
        # frame1_2 layout and place
        self.columnconfigure((0, 1), weight=1, uniform='b')
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='b')

        # frame1_2 widgets
        frame1_2_input_data = ttk.Frame(self)#, relief='raised', borderwidth=1
        frame1_2_input_data.grid(row=0, column=0, rowspan=3, columnspan=2, sticky='nesw')
        #
        frame1_2_input_data_start = ttk.Frame(frame1_2_input_data)#, relief='raised', borderwidth=1
        frame1_2_input_data_start.place(x=0, y=0, relwidth=1, relheight=0.18)

        frame1_2_input_data_end = ttk.Frame(frame1_2_input_data)#, relief='raised', borderwidth=1
        frame1_2_input_data_end.place(x=0, rely=0.18, relwidth=1, relheight=0.18)
        #
        frame1_2_input_data_waypoint = ttk.Frame(frame1_2_input_data)#, relief='raised', borderwidth=1
        frame1_2_input_data_waypoint.place(x=0, rely=0.36, relwidth=1, relheight=0.18)
        #
        frame1_2_input_data_obstacle = ttk.Frame(frame1_2_input_data)#, relief='raised', borderwidth=1
        frame1_2_input_data_obstacle.place(x=0, rely=0.54, relwidth=1, relheight=0.46)
        #
        frame1_2_input_data_start.columnconfigure((0, 1), weight=1, uniform='c')
        frame1_2_input_data_start.rowconfigure((0, 1), weight=1, uniform='d')

        frame1_2_input_data_end.columnconfigure((0, 1), weight=1, uniform='c')
        frame1_2_input_data_end.rowconfigure((0, 1), weight=1, uniform='d')
        #
        frame1_2_input_data_waypoint.columnconfigure((0, 1), weight=1, uniform='c')
        frame1_2_input_data_waypoint.rowconfigure((0, 1), weight=1, uniform='d')
        #
        frame1_2_input_data_obstacle.columnconfigure((0, 1), weight=1, uniform='c')
        frame1_2_input_data_obstacle.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform='d')
        #
        starting_point_label = ttk.Label(frame1_2_input_data_start, text='Start position')
        starting_point_label.grid(row=0, column=0, padx=10, pady=2, sticky='w')
        textbox_starting_x = ttk.Entry(frame1_2_input_data_start)
        textbox_starting_x.grid(row=1, column=0, padx=1, pady=1)
        textbox_starting_y = ttk.Entry(frame1_2_input_data_start)
        textbox_starting_y.grid(row=1, column=1, padx=1, pady=1)

        # labeli1 = ttk.Label(frame1_2_input_data_start, background='green')
        # labeli1.grid(row=0, column=0)
        # labeli2 = ttk.Label(frame1_2_input_data_start, background='black')
        # labeli2.grid(row=0, column=1)
        # labeli3 = ttk.Label(frame1_2_input_data_start, background='blue')
        # labeli3.grid(row=1, column=0)
        # labeli4 = ttk.Label(frame1_2_input_data_start, background='yellow')
        # labeli4.grid(row=1, column=1)

        end_point_label = ttk.Label(frame1_2_input_data_end, text='End position')
        end_point_label.grid(row=0, column=0, padx=10, pady=2, sticky='w')
        textbox_end_x = ttk.Entry(frame1_2_input_data_end)
        textbox_end_x.grid(row=1, column=0, padx=1, pady=1)
        textbox_end_y = ttk.Entry(frame1_2_input_data_end)
        textbox_end_y.grid(row=1, column=1, padx=1, pady=1)
        #
        waypoint_label = ttk.Label(frame1_2_input_data_waypoint, text='Waypoint')
        waypoint_label.grid(row=0, column=0, padx=10, pady=2, sticky='w')
        textbox_waypoint_x = ttk.Entry(frame1_2_input_data_waypoint)
        textbox_waypoint_x.grid(row=1, column=0, padx=1, pady=1)
        textbox_waypoint_y = ttk.Entry(frame1_2_input_data_waypoint)
        textbox_waypoint_y.grid(row=1, column=1, padx=1, pady=1)

        obstacles_location_label = ttk.Label(frame1_2_input_data_obstacle, text='Location Obstacles ')
        obstacles_location_label.grid(row=0, column=0, padx=10, pady=2, sticky='w')
        textbox_obstacle1_x = ttk.Entry(frame1_2_input_data_obstacle)
        textbox_obstacle1_x.grid(row=1, column=0, padx=1, pady=1)
        textbox_obstacle1_y = ttk.Entry(frame1_2_input_data_obstacle)
        textbox_obstacle1_y.grid(row=1, column=1, padx=1, pady=1)
        textbox_obstacle2_x = ttk.Entry(frame1_2_input_data_obstacle)
        textbox_obstacle2_x.grid(row=2, column=0, padx=1, pady=1)
        textbox_obstacle2_y = ttk.Entry(frame1_2_input_data_obstacle)
        textbox_obstacle2_y.grid(row=2, column=1, padx=1, pady=1)
        textbox_obstacle3_x = ttk.Entry(frame1_2_input_data_obstacle)
        textbox_obstacle3_x.grid(row=3, column=0, padx=1, pady=1)
        textbox_obstacle3_y = ttk.Entry(frame1_2_input_data_obstacle)
        textbox_obstacle3_y.grid(row=3, column=1, padx=1, pady=1)
        textbox_obstacle4_x = ttk.Entry(frame1_2_input_data_obstacle)
        textbox_obstacle4_x.grid(row=4, column=0, padx=1, pady=1)
        textbox_obstacle4_y = ttk.Entry(frame1_2_input_data_obstacle)
        textbox_obstacle4_y.grid(row=4, column=1, padx=1, pady=1)

        button_Start = ttk.Button(self, text='Start',width=20)#,command=start_button
        button_Set_reset_Settings = ttk.Button(self, text='Set Settings',width=20)#,command=set_reset_button
        button_Start.grid(row=3, column=0)
        button_Set_reset_Settings.grid(row=3, column=1)

        timer = ttk.Label(self, text="Timer value")
        timer.grid(row=4, column=0, columnspan=2, sticky='n')



class Frame2(ttk.Frame):
    def __init__(self,parent):
        #main setup GUI
        super().__init__(parent)
        self.place(relx=0.4, y=0, relwidth=0.6, relheight=1)
        ttk.Frame(self, relief='raised', borderwidth=1)

        # widgets
        self.frame2_1 = Frame2_1(self)
        self.frame2_2 = Frame2_2(self)

class Frame2_1(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # frame2 layout and place
        self.place(x=0, y=0, relwidth=1, relheight=0.3)
        ttk.Frame(self, relief='raised', borderwidth=1)

        self.create_widgets()

    def create_widgets(self):
        # frame2_1 layout and place
        self.columnconfigure((0, 1), weight=1, uniform='e')
        self.rowconfigure(0, weight=2, uniform='f')
        self.rowconfigure(1, weight=3, uniform='f')

        # labelw1 = ttk.Label(self, background='green')
        # labelw1.grid(row=0, column=0, sticky='news')
        # labelw2 = ttk.Label(self, background='black')
        # labelw2.grid(row=0, column=1, sticky='news')
        # labelw3 = ttk.Label(self, background='blue')
        # labelw3.grid(row=1, column=0, sticky='news')
        # labelw4 = ttk.Label(self, background='yellow')
        # labelw4.grid(row=1, column=1, sticky='news')

        # frame2_1 widgets

        # speed indicator
        speed = ttk.Meter(
            self,
            amounttotal=25,
            amountused=10,
            metertype='semi',
            textfont='-size 12',
            subtext='Km/h',
            subtextfont='-size 6',
            metersize=75
        )
        speed.grid(row=0, column=0, sticky='n')

        # battery value
        battery_value_int = tk.IntVar(value=69)
        battery_level = ttk.Floodgauge(
            self,
            variable=battery_value_int,
            mask='{}%'
        )
        battery_level.grid(row=0, column=1, padx=10, pady=2)

        # Create a scrolled_Text widget for displaying output data
        output_text_var = tk.StringVar(value = 'Welcome to KITT, select mode and fill in variables!')
        # Create a Text widget
        message_output_text_field = scrolledtext.ScrolledText(self)

        # Set the initial value of the StringVar
        output_text_var.set("Welcome to KITT, select mode and fill in variables!")

        # Insert the value of the StringVar into the ScrolledText widget
        message_output_text_field.insert(tk.END, output_text_var.get())
        # message_output_text_field = ScrolledText(self,
        #                                          autohide=True,
        #                                          state = 'disabled',
        #                                          text='welcome to KITT, select mode and fill in variables'
        #                                          )  #
        message_output_text_field.grid(row=1, column=0, columnspan=2, padx=10, pady=2)


class Frame2_2(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, rely=0.3, relwidth=1, relheight=0.7)
        ttk.Frame(self, relief='raised', borderwidth=1)

        self.create_widgets()

    def create_widgets(self):
        # frame2_2 widgets
        # Create a FigureCanvasTkAgg object to display the plot
        canvas = FigureCanvasTkAgg(visuel_grid(), master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top')


GUI()
