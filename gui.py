from tkinter import *					
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
from tkinter.filedialog import askdirectory

from utils import get_PALMTracer_files, get_poca_files, get_csv_poca_frame_files, get_csv_poca_intensity_files, get_csv_poca_sigma_files
from save_loc_as_pdf import save_loc_as_pdf
from do_analysis_for_one_acquisition import do_analysis_for_one_acquisition
from get_idx_laser_fov_for_each_well import get_idx_laser_fov_for_each_well
from do_cumulative_number_clusters import do_cumulative_number_clusters
from do_photophysics_parameters_plotting import do_photophysics_parameters_plotting
from do_heatmap_photophysics_parameters import do_heatmap_photophysics_parameters
from do_heatmap_one_photophysics_parameter import do_heatmap_one_photophysics_parameter
from do_photophysics_number_super_supra_clusters import do_photophysics_number_super_supra_clusters
from do_96heatmap_one_photophysics_parameter import do_96heatmap_one_photophysics_parameter

import os
import statistics

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
        window.add(tab2, text ='Single Well Analysis')
        # Tab 3 : PoCA output
        tab3 = ttk.Frame(window)
        window.add(tab3, text ='8-Well Plate Analysis')
        # Tab 4 : Super/Supra-Blinkers
        tab4 = ttk.Frame(window)
        window.add(tab4, text ='NOT WORKING(SuperBlinkers)')
        window.pack(expand = 1, fill ="both")
        # Tab 4 : Super/Supra-Blinkers
        tab5 = ttk.Frame(window)
        window.add(tab5, text ='96-Well Plate Analysis')
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
        
        self.isPT_bool = BooleanVar()
        self.isPT_bool.set(True)
        self.isPT = Checkbutton(tab1, text='PALMTracer experiment (After Loading)', variable=self.isPT_bool, bg='#FAFBFC')
        self.isPT.grid(row=1, column=0, sticky='W', padx=10, pady=3)
        
        self.exp_name_text = Label(tab1, text='Name for Results Repertory', bg='#FAFBFC')
        self.exp_name_text.grid(row=2, column=0, sticky='W', padx=5, pady=10)
        self.exp_name = Entry(tab1)
        self.exp_name.grid(row=2, column=1, columnspan=10, sticky="WE", pady=3)
        self.exp_name.insert(0, "results_files_loc")
        
        # Select statistic to use for heatmaps
        self.stats_choice = Label(tab1, text = "Statistical value used for heatmaps", bg='#FAFBFC')
        self.stats_choice.grid(row=3, column=0, sticky="W", pady=3, ipadx=1, padx=5)
        self.list_stats_choice = ["Median", "Mean"]
        self.widget_stats_choice = ttk.Combobox(tab1, values=self.list_stats_choice, state="readonly")
        self.widget_stats_choice.grid(row=4, column=0, sticky="W", pady=3, ipadx=1, padx=5)
        self.widget_stats_choice.current(0)
        self.choice_stats = 'median'
        self.method_choice_stats = statistics.median
        
        # Select if we want boxplot or histogram
        self.hist_box = Label(tab1, text = "Distribution Representation", bg='#FAFBFC')
        self.hist_box.grid(row=5, column=0, sticky="W", pady=3, ipadx=1, padx=5)
        self.list_hist_box = ["density histogram", "boxplot"]
        self.widget_hist_box = ttk.Combobox(tab1, values=self.list_hist_box, state="readonly")
        self.widget_hist_box.grid(row=6, column=0, sticky="W", pady=3, ipadx=1, padx=5)
        self.widget_hist_box.current(0)
        self.hist_box_choice = 'density histogram'
        self.use_boxplot = True

                
        # ------- LOCALIZATIONS ANALYSIS TAB -------
        self.run_exp_bool = BooleanVar()
        self.run_exp_bool.set(False)
        self.run_exp = Button(tab2, text='Run Density Measurement', command=self.do_run_loc_exp)
        self.run_exp.grid(row=0, column=0, sticky="WE", pady=3, ipadx=1, padx=5)
        
        self.run_exp_bool = BooleanVar()
        self.run_exp_bool.set(False)
        self.run_exp = Button(tab2, text='Get Cumulative Number of Clusters', command=self.do_run_cum_num_clus)
        self.run_exp.grid(row=1, column=0, sticky="WE", pady=3, ipadx=1, padx=5)

        self.run_exp_bool = BooleanVar()
        self.run_exp_bool.set(False)
        self.run_exp = Button(tab2, text='Get Photophysics Plots', command=self.do_photophysics_analysis)
        self.run_exp.grid(row=2, column=0, sticky="WE", pady=3, ipadx=1, padx=5)
        self.poca_files = None
        self.csv_intensity_files = None
        self.csv_frame_files = None
        self.csv_sigma_files = None      
        
          
        # ------- CLUSTERS ANALYSIS TAB -------
        self.get_experiment_heatmap_bool = BooleanVar()
        self.get_experiment_heatmap_bool.set(False)
        self.get_experiment_heatmap = Button(tab3, text='Get Experiment Heatmap', command=self.do_heatmap_whole_exp)
        self.get_experiment_heatmap.grid(row=0, column=0, sticky="WE", pady=3, ipadx=1, padx=5)

        self.get_one_heatmap_bool = BooleanVar()
        self.get_one_heatmap_bool.set(False)
        self.get_one_heatmap = Button(tab3, text='Get Photophysics Parameter Heatmap', command=self.do_one_heatmap)
        self.get_one_heatmap.grid(row=1, column=0, sticky="WE", pady=3, ipadx=1, padx=5)
        
        self.index_we_want = []
        self.phot_parameters = ['ON times', 'OFF times', "Intensity_loc", 'total ON',
                                'blinks', 'intensity', '# seq ON', '# seq OFF', 'Loc_Precision']

        self.options = ["Length ON times", "Length OFF times", "Intensity per Loc.", "Total ON time",
                "Num. Blinks", "Intensity per Clus.", "Num. ON time", "Num. OFF time", "Loc. Precision"]

        self.checkbox_vars = []
        self.checkboxs = list()
        for i in range(0,4):
            var = IntVar()
            self.checkbox_vars.append(var)
            checkbox = Checkbutton(tab3, text=self.options[i], variable=var, bg='#FAFBFC')
            checkbox.grid(row=i+2, column=0, sticky='W')
            self.checkboxs.append(checkbox)
        for i in range(4,8):
            var = IntVar()
            self.checkbox_vars.append(var)
            checkbox = Checkbutton(tab3, text=self.options[i], variable=var, bg='#FAFBFC')
            checkbox.grid(row=i-2, column=1, sticky='W')
            self.checkboxs.append(checkbox)
        # Loc precision
        var = IntVar()
        self.checkbox_vars.append(var)
        checkbox = Checkbutton(tab3, text=self.options[8], variable=var, bg='#FAFBFC')
        checkbox.grid(row=7, column=0, sticky='W')
        self.checkboxs.append(checkbox)
        
        self.check_everything = Button(tab3, text='Check Everything', command=self.select_all, bg='#FAFBFC')
        self.check_everything.grid(row=8, column=0, sticky='W')
        
        self.drop_one_event_bool = BooleanVar()
        self.drop_one_event_bool.set(False)
        self.drop_one_event_check = Checkbutton(tab3, text='Drop Single Event', variable=self.drop_one_event_bool, bg='#FAFBFC')
        self.drop_one_event_check.grid(row=9, column=0, sticky='W')
        
        self.drop_beads_bool = BooleanVar()
        self.drop_beads_bool.set(False)
        self.drop_beads_bool_check = Checkbutton(tab3, text='Remove Beads', variable=self.drop_beads_bool, bg='#FAFBFC')
        self.drop_beads_bool_check.grid(row=9, column=1, sticky='W')
        
        
        
        # ------- SUPERBLINKERS ET SUPRABLINKERS TAB -------
        self.var = StringVar()
        self.superblinkers = Radiobutton(tab4, text='Superblinkers', variable=self.var, value='1', bg='#FAFBFC')
        self.superblinkers.grid(row=0, column=0, sticky='W', padx=10, pady=3)
        self.sm_cluster = Radiobutton(tab4, text='Single Molecule Cluster', variable=self.var, value='2', bg='#FAFBFC')
        self.sm_cluster.grid(row=0, column=1, sticky='W', padx=10, pady=3)
                
        self.run_exp_super_bool = BooleanVar()
        self.run_exp_super_bool.set(False)
        self.run_exp_super = Button(tab4, text='Get Specific Photophysics Plots', command=self.do_photophysics_analysis_super_supra)
        self.run_exp_super.grid(row=1, column=0, sticky="WE", pady=3, ipadx=1, padx=5)
    
        self.get_experiment_heatmap_super_bool = BooleanVar()
        self.get_experiment_heatmap_super_bool.set(False)
        self.get_experiment_heatmap_super = Button(tab4, text='Get Experiment Heatmap', command=self.do_heatmap_whole_exp)
        self.get_experiment_heatmap_super.grid(row=2, column=0, sticky="WE", pady=3, ipadx=1, padx=5)

        self.get_one_heatmap_super_bool = BooleanVar()
        self.get_one_heatmap_super_bool.set(False)
        self.get_one_heatmap_super = Button(tab4, text='Get Photophysics Parameter Heatmap', command=self.do_one_heatmap)
        self.get_one_heatmap_super.grid(row=3, column=0, sticky="WE", pady=3, ipadx=1, padx=5)
        
        self.index_we_want_super = []
        self.phot_parameters_super = ['ON times', 'OFF times', "Intensity_loc", 'total ON',
                                'blinks', 'intensity', '# seq ON', '# seq OFF', 'Loc_Precision']

        self.options_super = ["Length ON times", "Length OFF times", "Intensity per Loc.", "Total ON time",
                "Num. Blinks", "Intensity per Clus.", "Num. ON time", "Num. OFF time", "Loc. Precision"]

        self.checkbox_vars_super = []
        self.checkboxs_super = list()
        for i in range(0,4):
            var = IntVar()
            self.checkbox_vars_super.append(var)
            checkbox = Checkbutton(tab4, text=self.options_super[i], variable=var, bg='#FAFBFC')
            checkbox.grid(row=i+4, column=0, sticky='W')
            self.checkboxs_super.append(checkbox)
        for i in range(4,8):
            var = IntVar()
            self.checkbox_vars_super.append(var)
            checkbox = Checkbutton(tab4, text=self.options_super[i], variable=var, bg='#FAFBFC')
            checkbox.grid(row=i, column=1, sticky='W')
            self.checkboxs_super.append(checkbox)
        # Loc precision
        var = IntVar()
        self.checkbox_vars_super.append(var)
        checkbox = Checkbutton(tab4, text=self.options[8], variable=var, bg='#FAFBFC')
        checkbox.grid(row=9, column=0, sticky='W')
        self.checkboxs_super.append(checkbox)
        
        self.check_everything_super = Button(tab4, text='Check Everything', command=self.select_all_super, bg='#FAFBFC')
        self.check_everything_super.grid(row=10, column=0, sticky='W')
   


        # ------- 96-WELL PLATE ANALYSIS TAB -------
        self.get_experiment_96heatmap_bool = BooleanVar()
        self.get_experiment_96heatmap_bool.set(False)
        self.get_experiment_96heatmap = Button(tab5, text='Get Experiment Heatmap', command=self.do_heatmap_whole_exp)
        self.get_experiment_96heatmap.grid(row=0, column=0, sticky="WE", pady=3, ipadx=1, padx=5)

        self.get_one_96heatmap_bool = BooleanVar()
        self.get_one_96heatmap_bool.set(False)
        self.get_one_96heatmap = Button(tab5, text='Get Photophysics Parameter Heatmap', command=self.do_one_96heatmap)
        self.get_one_96heatmap.grid(row=1, column=0, sticky="WE", pady=3, ipadx=1, padx=5)
        
        self.index_we_want = []
        self.phot_parameters = ['ON times', 'OFF times', "Intensity_loc", 'total ON',
                                'blinks', 'intensity', '# seq ON', '# seq OFF', 'Loc_Precision']

        self.options = ["Length ON times", "Length OFF times", "Intensity per Loc.", "Total ON time",
                "Num. Blinks", "Intensity per Clus.", "Num. ON time", "Num. OFF time", "Loc. Precision"]

        self.checkbox_vars96 = []
        self.checkboxs96 = list()
        for i in range(0,4):
            var = IntVar()
            self.checkbox_vars96.append(var)
            checkbox = Checkbutton(tab5, text=self.options[i], variable=var, bg='#FAFBFC')
            checkbox.grid(row=i+2, column=0, sticky='W')
            self.checkboxs96.append(checkbox)
        for i in range(4,8):
            var = IntVar()
            self.checkbox_vars96.append(var)
            checkbox = Checkbutton(tab5, text=self.options[i], variable=var, bg='#FAFBFC')
            checkbox.grid(row=i-2, column=1, sticky='W')
            self.checkboxs96.append(checkbox)
        # Loc precision
        var = IntVar()
        self.checkbox_vars96.append(var)
        checkbox = Checkbutton(tab5, text=self.options[8], variable=var, bg='#FAFBFC')
        checkbox.grid(row=7, column=0, sticky='W')
        self.checkboxs96.append(checkbox)
        
        self.check_everything96 = Button(tab5, text='Check Everything', command=self.select_all96, bg='#FAFBFC')
        self.check_everything96.grid(row=8, column=0, sticky='W')
        
        self.drop_one_event_bool = BooleanVar()
        self.drop_one_event_bool.set(False)
        self.drop_one_event_check = Checkbutton(tab5, text='Drop Single Event', variable=self.drop_one_event_bool, bg='#FAFBFC')
        self.drop_one_event_check.grid(row=9, column=0, sticky='W')
        
        self.drop_beads_bool = BooleanVar()
        self.drop_beads_bool.set(False)
        self.drop_beads_bool_check = Checkbutton(tab5, text='Remove Beads', variable=self.drop_beads_bool, bg='#FAFBFC')
        self.drop_beads_bool_check.grid(row=9, column=1, sticky='W')



   
    def load_molecule_data(self):
        """
        Load PALMTracer files (ending with locPALMTracer.txt), PoCA files (cleaned PT and csv files)
        """        
        try:
            self.repertory_path = askdirectory(title="Select your Source directory")
            self.index = [f for f in os.listdir(self.repertory_path+'/') if os.path.isdir(os.path.join(self.repertory_path+'/', f))]
            self.files = get_PALMTracer_files(self.repertory_path)
            self.poca_files = get_poca_files(self.repertory_path)
            self.csv_intensity_files = get_csv_poca_intensity_files(self.repertory_path)
            self.csv_frame_files = get_csv_poca_frame_files(self.repertory_path)
            self.csv_sigma_files = get_csv_poca_sigma_files(self.repertory_path)
            self.isPT_bool.set(True)
            print("Done:", "'"+self.repertory_path+"'", 'has been loaded')
        except:
            print("No directory selected")


    def do_run_loc_exp(self):
        """
        Run the localization data analysis and plot the density through time
        """        
        for i in self.files:
            if self.isPT_bool.get() == False:
                self.laser = self.index
            # Get laser and well name
            [idx, lsr] = get_idx_laser_fov_for_each_well(self.index, self.laser, i)
            # Get data about localisation, density...
            cum_loc_per_frame, density_per_frame, avg_density = do_analysis_for_one_acquisition(i)
            # Plot and saving plots
            save_loc_as_pdf(i, idx, lsr, density_per_frame, cum_loc_per_frame, avg_density, self.exp_name.get())
        print("Analysis Done!")
        
                
    def do_run_cum_num_clus(self):
        do_cumulative_number_clusters(self.poca_files, self.exp_name.get(), self.isPT_bool.get(), 
                                      drop_one_event=self.drop_one_event_bool.get(),
                                      drop_beads=self.drop_beads_bool.get())
        print("Cumulative Clusters Analysis Done!")
    
    
    def do_photophysics_analysis(self):
        self.select_stats_method_visu()
        do_photophysics_parameters_plotting(self.poca_files, self.csv_frame_files, self.csv_intensity_files, self.csv_sigma_files, 
                                            self.exp_name.get(), self.isPT_bool.get(), drop_one_event=self.drop_one_event_bool.get(),
                                            boxplot=self.use_boxplot, drop_beads=self.drop_beads_bool.get())
        print("Cluster Photophysics Plotting Done!")

        
    def do_heatmap_whole_exp(self):
        self.select_stats_method_heatmap()
        do_heatmap_photophysics_parameters(self.exp_name.get(), self.poca_files, self.csv_frame_files, self.csv_intensity_files, 
                                           self.csv_sigma_files, self.isPT_bool.get(), stats=self.method_choice_stats, 
                                           drop_one_event=self.drop_one_event_bool.get(), drop_beads=self.drop_beads_bool.get())
        print("Heatmap for the Whole Experiment Done!")

        
    def do_one_heatmap(self):
        self.select_stats_method_heatmap()
        self.checkbox_values = [option for option, var in zip(range(0, 9), self.checkbox_vars) if var.get()]
        self.index_we_want = [self.phot_parameters[i] for i in self.checkbox_values]
        do_heatmap_one_photophysics_parameter(self.exp_name.get(), self.index_we_want, self.poca_files, self.csv_frame_files, 
                                              self.csv_intensity_files, self.csv_sigma_files,self.isPT_bool.get(), 
                                              stats=self.method_choice_stats, drop_one_event=self.drop_one_event_bool.get(),
                                              drop_beads=self.drop_beads_bool.get())
        print("Heatmap(s) for Selected Parameters Done!")
        
    def do_one_96heatmap(self):
        self.select_stats_method_heatmap()
        self.checkbox_values = [option for option, var in zip(range(0, 9), self.checkbox_vars96) if var.get()]
        self.index_we_want = [self.phot_parameters[i] for i in self.checkbox_values]
        do_96heatmap_one_photophysics_parameter(self.exp_name.get(), self.index_we_want, self.poca_files, self.csv_frame_files, 
                                              self.csv_intensity_files, self.csv_sigma_files,self.isPT_bool.get(), 
                                              stats=self.method_choice_stats, drop_one_event=self.drop_one_event_bool.get(),
                                              drop_beads=self.drop_beads_bool.get())
        print("Heatmap(s) for Selected Parameters Done!")


    def select_all(self):
        for i in self.checkboxs:
            i.invoke()
            
    def select_all96(self):
        for i in self.checkboxs:
            i.invoke()

    def select_all_super(self):
        for i in self.checkboxs_super:
            i.invoke()
                    
    def select_stats_method_heatmap(self):
        # Obtenir l'élément sélectionné
        self.choice_stats = self.widget_stats_choice.get()
        if self.choice_stats == 'Mean':
            self.method_choice_stats = statistics.mean
        else:
            self.method_choice_stats = statistics.median


    def select_stats_method_visu(self):
        self.hist_box_choice = self.widget_hist_box.get()
        if self.hist_box_choice == 'boxplot':
            self.use_boxplot = True
        else:
            self.use_boxplot = False



    def do_photophysics_analysis_super_supra(self):
        self.select_stats_method_visu()
        method = self.var.get()
        if method == str(1):
            one_event = False
            superblinkers = True
        elif method == str(2):
            one_event = True
            superblinkers = False
        do_photophysics_number_super_supra_clusters(self.poca_files, self.csv_frame_files, self.csv_intensity_files, self.csv_sigma_files, 
                                            self.exp_name.get(), self.isPT_bool.get(),boxplot=self.use_boxplot, use_one_event=one_event, 
                                            use_super_blinkers=superblinkers)
        if one_event == True:
            print("Single Molecule Cluster Photophysics Plotting Done!")
        else:
            print("Superblinkers Photophysics Plotting Done!")
