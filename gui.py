from tkinter import *					
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkinter.filedialog import askdirectory

from do_analysis_for_one_acquisition import do_analysis_for_one_acquisition
from utils import get_PALMTracer_files
from save_as_pdf import save_as_pdf
from get_idx_laser_fov_for_each_well import get_idx_laser_fov_for_each_well

import os


class MyWindow:
    
    def __init__(self, root):
        window = ttk.Notebook(root)
        style = ThemedStyle(root)
        style.theme_use('adapta')

        # Tab 1 : Load files, etc...
        tab1 = ttk.Frame(window)
        window.add(tab1, text ='Files & Informations')
        # Tab 2 : PALMTracer output
        tab2 = ttk.Frame(window)
        window.add(tab2, text ='Localizations Analysis')
        # Tab 3 : PoCA output
        tab3 = ttk.Frame(window)
        window.add(tab3, text ='Clusters Analysis')
        
        window.pack(expand = 1, fill ="both")


        # ------- INFORMATIONS TAB -------
        self.load_data_bool = BooleanVar()
        self.load_data_bool.set(False)
        self.load_data = Button(tab1, text='Select Experiment', command=self.load_molecule_data)
        self.load_data.grid(row=0, column=0, columnspan=7, sticky="WE", pady=3, ipadx=1, padx=5)
        self.repertory_path = None
        self.index = None
        self.files = None
        self.laser = ['561.PT', '561-405.PT']
        
        self.num_fov_text = Label(tab1, text='Number of FOV per well')
        self.num_fov_text.grid(row=1, column=0, sticky='W', padx=5, pady=10)
        self.num_fov = Entry(tab1)
        self.num_fov.grid(row=1, column=1, columnspan=10, sticky="WE", pady=3)
        self.num_fov.insert(0, "1")

        
        
        # ------- LOCALIZATIONS ANALYSIS TAB -------
        self.use_ii_bool = BooleanVar()
        self.use_ii_bool.set(False)
        self.use_ii = Checkbutton(tab2, text='Get Integrated Intensity', variable=self.get_ii)
        self.use_ii.grid(row=0, column=0, sticky='W', padx=10, pady=3)
        
        self.use_cum_loc_number_bool = BooleanVar()
        self.use_cum_loc_number_bool.set(False)
        self.use_cum_loc_number = Checkbutton(tab2, text='Cumulative number of localizations', variable=self.get_cum_loc_number)
        self.use_cum_loc_number.grid(row=1, column=0, sticky='W', padx=10, pady=3)
        
        self.exp_name_text = Label(tab2, text='Name of the Results Repertory')
        self.exp_name_text.grid(row=2, column=0, sticky='W', padx=5, pady=10)
        self.exp_name = Entry(tab2)
        self.exp_name.grid(row=2, column=1, columnspan=10, sticky="WE", pady=3)
        self.exp_name.insert(0, "results_files")
        
        self.run_exp_bool = BooleanVar()
        self.run_exp_bool.set(False)
        self.run_exp = Button(tab2, text='Run Density Measurement', command=self.do_run_exp)
        self.run_exp.grid(row=3, column=0, sticky="WE", pady=3, ipadx=1, padx=5)


    def load_molecule_data(self):
        try:
            self.repertory_path = askdirectory(title="Select your Source directory")
            self.index = [f for f in os.listdir(self.repertory_path+'/') if os.path.isdir(os.path.join(self.repertory_path+'/', f))]
            self.files = get_PALMTracer_files(self.repertory_path)
            print("Done:", "'"+self.repertory_path+"'", 'has been loaded')
        except:
            print("No directory selected")
            
    def get_ii(self):
        None

    def get_cum_loc_number(self):
        None
        
    def do_run_exp(self):
        # Generate list of FOV (FOV1, FOV2, FOV3...depending on the number of FOV)
        input_n_fov = 1
        fov=None
        if input_n_fov != 1 and input_n_fov != 0:
            num_fov = ''.join(map(str, list(range(1,input_n_fov+1))))
            fov = ['FOV'+n_fov for n_fov in num_fov]
        
        for i in self.files:
            if fov != None:
                [idx, lsr, fov] = get_idx_laser_fov_for_each_well(self.index, self.laser, i, fov=fov)
            else:
                [idx, lsr] = get_idx_laser_fov_for_each_well(self.index, self.laser, i)
            cum_loc_per_frame, density_per_frame, avg_density = do_analysis_for_one_acquisition(i)
            save_as_pdf(i, idx, lsr, density_per_frame, cum_loc_per_frame, avg_density, self.exp_name.get())
        print("Analysis Done!")