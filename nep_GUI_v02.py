#!/usr/bin/env python
import os
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from nep_calculations_v02 import nep_processing
from PIL import ImageTk,Image
import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        '''
        gives weight to the cells in the grid
        '''
        directory = os.path.dirname(os.path.abspath(__file__))+'/'
        rows = 0
        while rows < 50:
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            rows += 1

        '''
        defines and places the notebook widget
        '''
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=0, column=0, columnspan=50, rowspan=49,sticky='nsew')

        '''
        adds tab 1 of the notebook
        '''
        self.frame1 = ttk.Frame(self.notebook, width=600, height=400)
        self.notebook.add(self.frame1, text='Sr')


        '''
        get pictures for buttons and initialized empty variables for remembering path in askdirectory
        '''
        self.last_in_path = ''
        self.last_out_path = ''
        self.pic_button_on = ImageTk.PhotoImage(Image.open(directory+'GUI_images/button_small_on.png'))
        self.pic_button_off = ImageTk.PhotoImage(Image.open(directory+'GUI_images/button_small_off.png'))
        self.pic_button_select_in = ImageTk.PhotoImage(Image.open(directory+'GUI_images/select_input.png'))
        self.pic_button_select_out = ImageTk.PhotoImage(Image.open(directory+'GUI_images/select_output.png'))
        self.pic_button_Go = ImageTk.PhotoImage(Image.open(directory+'GUI_images/button_Go.png'))
        self.pic_button_opz = ImageTk.PhotoImage(Image.open(directory+'GUI_images/button_opz.png'))


        '''
        check which tab is active
        '''
        self.act_tab = ''


        '''
        callback functions
        '''
        def input_fileCallBack():
            self.act_tab = self.notebook.tab(self.notebook.select(), 'text')

            state_opz = OPZ
            state_opz_S = OPZ_S
            print(self.act_tab)
            if self.act_tab == 'Sr':
                self.input_directory.delete(0,'end')
                file = filedialog.askdirectory(initialdir=self.last_in_path)
                active_path = file
                self.last_in_path= file
                self.input_directory.insert(1, active_path + '/')
            elif self.act_tab =='S':
                self.input_directory_S.delete(0, 'end')
                file = filedialog.askdirectory(initialdir=self.last_in_path)
                active_path = file
                self.last_in_path = file
                self.input_directory_S.insert(1, active_path + '/')

        def output_fileCallBack():
            if self.act_tab == 'Sr':
                self.output_directory.delete(0,'end')
                file = filedialog.askdirectory(initialdir=self.last_out_path)
                active_path = file
                self.last_out_path = file
                self.output_directory.insert(1, active_path + '/')
            elif self.act_tab == 'S':
                self.output_directory_S.delete(0, 'end')
                file = filedialog.askdirectory(initialdir=self.last_out_path)
                active_path = file
                self.last_out_path = file
                self.output_directory_S.insert(1, active_path + '/')

        def GoCallBack():
            self.act_tab = self.notebook.tab(self.notebook.select(), 'text')
            if self.act_tab == 'Sr':
                nep_processing(self.input_directory.get(), self.output_directory.get(), last_OPZ.get(), self.act_tab)
                print('kaboom', self.act_tab, last_OPZ.get())
            elif self.act_tab == 'S':
                nep_processing(self.input_directory_S.get(), self.output_directory_S.get(), last_OPZ_S.get(), self.act_tab)
                print('I did sulphur!')
        def toggle_opz():
            self.act_tab = self.notebook.tab(self.notebook.select(), 'text')

            state_opz = OPZ
            state_opz_S = OPZ_S


            if self.act_tab == 'Sr':
                if state_opz.get():
                    last_OPZ['state'] = 'normal'
                    check_opz['image'] = self.pic_button_on
                else:
                    last_OPZ['state'] = 'disabled'
                    check_opz['image'] = self.pic_button_off
            else:
                if state_opz_S.get():
                    last_OPZ_S['state'] = 'normal'
                    check_opz_S['image'] = self.pic_button_on
                else:
                    last_OPZ_S['state'] = 'disabled'
                    check_opz_S['image'] = self.pic_button_off
        def update_graph():
            self.act_tab = self.notebook.tab(self.notebook.select(), 'text')
            if self.act_tab == 'Sr':
                try:
                    self.pic_opz_graph = ImageTk.PhotoImage(Image.open(directory+'GUI_images/opz_graph.png'))
                    lb_graph = tk.Label(f2, image=self.pic_opz_graph, state='disabled')
                    lb_graph.grid(column=0, row=2)
                    lb_graph['state']= 'normal'
                except:
                    None
            elif self.act_tab == 'S':
                try:
                    self.pic_opz_graph_S = ImageTk.PhotoImage(Image.open(directory+'GUI_images/opz_graph_S.png'))
                    lb_graph_S = tk.Label(f4, image=self.pic_opz_graph_S, state='disabled')
                    lb_graph_S.grid(column=0, row=2)
                    lb_graph_S['state']= 'normal'
                except:
                    None

        def active_tab():
            self.act_tab = self.notebook.tab(self.notebook.select(), 'text')
            print(self.act_tab)



        f1 = tk.Frame(self.frame1, width=600, height=400)
        f1.grid(column=0, row=0,sticky='NSEW')

        sep = ttk.Separator(self.frame1)
        sep.grid(column=1, row=5)

        f2 = tk.Frame(self.frame1, width=400, height=400, highlightthickness=5, highlightcolor='black')
        f2.grid(column=5, row=0)

        '''
        building widgets for Sr processing in tab
        '''

        in_search_button = tk.Button(f1, image=self.pic_button_select_in, width=170, command=input_fileCallBack)
        in_search_button.grid(column=0, row=5)

        self.input_directory = tk.Entry(f1, width=50)
        self.input_directory.grid(column=5, row=5)
        self.input_directory.focus()

        out_search_button = tk.Button(f1, text="select output folder", image=self.pic_button_select_out, width=170,
                                   command=output_fileCallBack)
        out_search_button.grid(column=0, row=10)

        self.output_directory = tk.Entry(f1, width=50)
        self.output_directory.grid(column=5, row=10)

        OPZ = tk.BooleanVar()
        OPZ.set(False)

        OPZ_S = tk.BooleanVar()
        OPZ_S.set(False)

        last_OPZ = ttk.Combobox(f1, state='disabled', values=[x for x in range(401)])
        last_OPZ.set('last OPZ file')
        last_OPZ.grid(column=5, row=20,pady=20)

        check_opz = tk.Checkbutton(f1, image=self.pic_button_off, var=OPZ, command=toggle_opz)
        check_opz.grid(column=0, row=20)

        button_opz = tk.Button(f1, image=self.pic_button_opz, command=toggle_opz())
        button_opz.grid(column=0, row=15)

        Go_button = tk.Button(f1, text="Go", image=self.pic_button_Go, fg="blue", width=170, command=GoCallBack)
        Go_button.grid(column=0, row=25)

        #test_button = ttk.Button(f1, text='crazyButton')
        #test_button.grid(column=0, row=30)

        s = ttk.Style()
        s.theme_use('aqua')

        update = tk.Button(f2, text='update', width =40, command = update_graph)
        update.grid(column=0,row=0)


        '''
        adds tab 2 of the notebook
        '''
        self.frame2 = ttk.Frame(self.notebook,width = 600, height=400)
        self.notebook.add(self.frame2, text='S')

        f3 = tk.Frame(self.frame2, width=600, height=400)
        f3.grid(column=0, row=0,sticky='NSEW')

        sep = ttk.Separator(self.frame2)
        sep.grid(column=1, row=5)

        f4 = tk.Frame(self.frame2, width=400, height=400, highlightthickness=5, highlightcolor='black')
        f4.grid(column=5, row=0)

        '''
        building widgets for Sulphur processing in tab
        '''

        in_search_button_S = tk.Button(f3, image=self.pic_button_select_in, width=170, command=input_fileCallBack)
        in_search_button_S.grid(column=0, row=5)

        self.input_directory_S = tk.Entry(f3, width=50)
        self.input_directory_S.grid(column=5, row=5)
        self.input_directory_S.focus()

        out_search_button_S = tk.Button(f3, text="select output folder", image=self.pic_button_select_out, width=170,
                                      command=output_fileCallBack)
        out_search_button_S.grid(column=0, row=10)

        self.output_directory_S = tk.Entry(f3, width=50)
        self.output_directory_S.grid(column=5, row=10)



        last_OPZ_S = ttk.Combobox(f3, state='disabled', values=[x for x in range(201)])
        last_OPZ_S.set('last OPZ file')
        last_OPZ_S.grid(column=5, row=20, pady=20)

        check_opz_S = tk.Checkbutton(f3, image=self.pic_button_off, var=OPZ_S, command=toggle_opz)
        check_opz_S.grid(column=0, row=20)

        button_opz_S = tk.Button(f3, image=self.pic_button_opz, command=toggle_opz())
        button_opz_S.grid(column=0, row=15)

        Go_button_S = tk.Button(f3, text="Go", image=self.pic_button_Go, fg="blue", width=170, command=GoCallBack)
        Go_button_S.grid(column=0, row=25)

        #test_button_S = ttk.Button(f3, text='crazyButton')
        #test_button_S.grid(column=0, row=30)

        s = ttk.Style()
        s.theme_use('aqua')
        update_S = tk.Button(f4, text='update', width=40, command=update_graph)
        update_S.grid(column=0, row=0)

        next_S = tk.Button(f4, text='Next', width=40)
        next_S.grid(column=0, row=1)


        '''
        adds placeholder for opz chart in both tabs
        '''
        self.pic_opz_graph = ImageTk.PhotoImage(Image.open(directory + 'GUI_images/opz_graph_empty.png'))
        lb_graph = tk.Label(f2, image=self.pic_opz_graph, state='disabled')
        lb_graph.grid(column=0, row=2)
        lb_graph['state'] = 'normal'

        self.pic_opz_graph_S = ImageTk.PhotoImage(Image.open(directory + 'GUI_images/opz_graph_empty.png'))
        lb_graph_S = tk.Label(f4, image=self.pic_opz_graph_S, state='disabled')
        lb_graph_S.grid(column=0, row=2)
        lb_graph_S['state'] = 'normal'



if __name__=='__main__':


    root = tk.Tk()
    root.geometry('1400x600')
    root.title('neptune_processing')
    IconFile = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.abspath(__file__)) + '/GUI_images/nep_pro_logo.png'))
    root.tk.call('wm', 'iconphoto', root, IconFile)

    MainApplication(root)
    root.mainloop()

# bug: changes things in the wrong tab writes in entry field ffor S not in Sr
