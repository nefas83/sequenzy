import os
import sys
import tkinter
from tkinter import filedialog as fd
from tkinter import font
from tkinter import ttk
import customtkinter
import tkinter.messagebox
import re
import collections
from tabulate import tabulate
import pandas as pd

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

customtkinter.set_appearance_mode("dark")       # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")   # Themes: blue (default), dark-blue, green

# Das Muster "[A-Za-z]" passt auf einen einzelnen Buchstaben 
# (entweder groß oder klein geschrieben), 
# "\d{1,3}" passt auf 1 bis 3 aufeinanderfolgende Zahlen, 
# und das Muster "[A-Za-z]" passt auf den abschließenden Buchstaben. 
# Das Muster ist umgeben von runden Klammern, damit es als Ganzes erkannt wird.
pattern = r"([A-Za-z])(\d{1,3})([A-Za-z])"
pattern_name = r'(?<=\>)[^ ]+'

class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()


        # Create the main window
        w = 850                         # width for the Tk root
        h = 700                         # height for the Tk root
        
        # get screen width and height
        ws = self.winfo_screenwidth()   # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.minsize(850,700)

        self.title('Sequenzy')
        
        # configure grid layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=4)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 8, 9), weight=1)
        self.grid_rowconfigure(7, weight=4)


        # Variables
        self.dicSequence            = {}
        self.dictSequence           = {}
        self.sequence_list          = []
        self.sequence               = ''
        self.fileName               = ''
        self.countMutant            = 0
        self.posibleCombinations    = 0
        self.combinations           = set()
        self.orderedMutant          = {}

        # widgets
        # Frame inside the GUI
        self.sidebar_frame = customtkinter.CTkFrame(master=self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")

        self.sequence_label = customtkinter.CTkLabel(master=self.sidebar_frame, text="Load Sequence List", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sequence_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btnLoadSequence = customtkinter.CTkButton(self.sidebar_frame, text="Open", command=self.btn_load_Sequence_event)
        self.btnLoadSequence.grid(row=1, column=0, padx=(20, 20), pady=(20, 10))

        self.logo_label = customtkinter.CTkLabel(master=self.sidebar_frame, text="Load Mutation List", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=2, column=0, padx=20, pady=(20, 10))

        self.btnLoadMutant = customtkinter.CTkButton(self.sidebar_frame, text="Open", command=self.btn_load_Mutation_event)
        self.btnLoadMutant.grid(row=3, column=0, padx=(20, 20), pady=(20, 10))

        self.logo_label = customtkinter.CTkLabel(master=self.sidebar_frame, text="Or Insert Mutation List", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=4, column=0, padx=20, pady=(20, 10))

        self.txtMutation = customtkinter.CTkTextbox(master=self.sidebar_frame)
        self.txtMutation.configure(corner_radius=5,
                                    fg_color="grey81", 
                                    text_color="black")
        self.txtMutation.grid(row=5, rowspan=3, column=0, columnspan=2, padx=20, pady=5, sticky="nsew")

        self.btnCalc = customtkinter.CTkButton(self.sidebar_frame, text="Calculate Possibilities", command=self.btn_calc_event)
        self.btnCalc.grid(row=8, column=0, columnspan=2, padx=(20, 20), pady=(20, 10),sticky="nsew")

        self.btnRun = customtkinter.CTkButton(self.sidebar_frame, text="Generate Combinations", command=self.btn_run_event)
        self.btnRun.configure(state='disabled')
        self.btnRun.grid(row=9, column=0, columnspan=2, padx=(20, 20), pady=(20, 10),sticky="nsew")

        self.txtLog = customtkinter.CTkTextbox(master=self)
        self.txtLog.configure(corner_radius=5,
                              fg_color="grey81", 
                              text_color="black",
                              font=customtkinter.CTkFont(family='Courier',size=20, weight="bold"),
                              state=tkinter.DISABLED)
        self.txtLog.grid(row=0, rowspan=3, column=1, columnspan=6, padx=20, pady=10, sticky="nsew")

        self.txtSequence = customtkinter.CTkTextbox(master=self)
        self.txtSequence.configure(corner_radius=5,
                              fg_color="grey81", 
                              text_color="black",
                              font=customtkinter.CTkFont(family='Courier',size=12, weight="bold"),
                              state=tkinter.DISABLED)
        self.txtSequence.grid(row=3, rowspan=3, column=1, columnspan=6, padx=20, pady=10, sticky="nsew")
        
        self.possibilitiest_label = customtkinter.CTkLabel(master=self, text="number of possibilities: ", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.possibilitiest_label.grid(row=6, column=1,  padx=20, pady=(20, 10))
        self.numMutant_label = customtkinter.CTkLabel(master=self, text="0", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.numMutant_label.grid(row=6, column=2, padx=20, pady=(20, 10))

        self.progress_label = customtkinter.CTkLabel(master=self, text="STATUS", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.progress_label.grid(row=7, column=1, columnspan=6, padx=20, pady=(20, 10))

        self.progressbar = ttk.Progressbar(master=self, orient='horizontal', mode="determinate")
        self.progressbar.grid(row=8, column=1, columnspan=6, padx=20, pady=10, sticky="nsew")
        self.progressbar['value'] = 0

    # Events
# ----------------------------------------------------------------------------
    def btn_load_Mutation_event(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        file = fd.askopenfile(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        
        if file is not None:
            self.txtMutation.delete(0.0, tkinter.END)
            tmpFile = file.readlines()
            for line in tmpFile:
                lineStrip = line.strip()
                self.txtMutation.insert(tkinter.END, lineStrip + '\n')
# ============================================================================
# ============================================================================

# ----------------------------------------------------------------------------
    def btn_load_Sequence_event(self):
        filetypes = (
            ('fasta files', '*.fasta'),
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        file = fd.askopenfile(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        
        if file is not None:
            self.sequence_list = []

            self.progress_label.configure(text='STATUS: Sequence loaded')
            tmpFile = file.readlines()
            for line in tmpFile:
                lineStrip = line.strip()

                #Get Sequence Name
                tmpResult = re.search(pattern_name, line)

                if tmpResult:
                    print(tmpResult.group(0))
                    self.fileName = tmpResult.group(0)
                    tmpLabel = 'STATUS: Sequence Name => ' + self.fileName
                    self.progress_label.configure(text=tmpLabel )

                self.txtSequence.configure(state=tkinter.NORMAL)
                self.txtSequence.insert(tkinter.END, lineStrip + '\n')
                self.txtSequence.configure(state=tkinter.NORMAL)

                if len(lineStrip) > 0:
                    if lineStrip[0] != '>':
                        self.sequence += lineStrip
# ============================================================================
# ============================================================================

# ----------------------------------------------------------------------------
    def btn_calc_event(self):
        self.progressbar['value'] = 0
        self.molReader(self.txtMutation.get(0.0, tkinter.END))
# ============================================================================
# ============================================================================

# ----------------------------------------------------------------------------
#                   "hic sunt dracones" --> Here be dragons
# ----------------------------------------------------------------------------
    def btn_run_event(self):
        legende = {}

        # Set Porgressbar max Value
        self.progressbar['maximum'] = self.posibleCombinations

        for i in range(self.posibleCombinations):
            binary = bin(i)[2:].zfill(len(self.orderedMutant))
            new_string = self.sequence
            changes = []
            
            for j, b in enumerate(binary):
                # name the new file with the name and the actual index
                filename = f"{self.fileName}_{i}.fasta"
                if b == '1':
                    pos = list(self.orderedMutant.keys())[j]
                    aminoAccid = list(self.orderedMutant.values())[j]
                    new_string = new_string[:pos-1] + aminoAccid[1] + new_string[pos:]
                    changes.append(aminoAccid[0] + str(pos) + aminoAccid[1])
                    
            # Write the actual combination to a new file
            legende[i] = changes
            with open(resource_path('output/' + filename), "w") as file:
                print('Write new File: ' + filename)
                file.write('>' + self.fileName + '\n')
                file.write(self.insertLineBreak(new_string, 70))
                if self.progressbar['value'] < self.progressbar['maximum']:
                    self.progressbar['value'] += 1          
        # print(legende)
        self.dict2Excel(legende, self.fileName)
# ============================================================================
# ============================================================================

# ----------------------------------------------------------------------------
#                           Functions
# ----------------------------------------------------------------------------
    def replace(self, s, position, character):
        return s[:position] + character + s[position+1:]
    
    def insertLineBreak(self, s, pos):
        return re.sub("(.{" + str(pos) + "})", "\\1\n", s, 0, re.DOTALL)
    
    def dict2Excel(self, data, name):
        df = pd.DataFrame.from_dict(data=data, orient='index')
        df.to_excel(resource_path('output/legende_' + name + '.xlsx'))
        df.to_csv(resource_path('output/legende_' + name + '.csv'))

    def calcPosibilitys(self,numMutatn):
        self.posibleCombinations = 2**self.countMutant
# ============================================================================
# ============================================================================

# ----------------------------------------------------------------------------
#                   Read the Mutation List
# ----------------------------------------------------------------------------
    def molReader(self, sequence):
        matches = re.findall(pattern, sequence)
        results = {}

        for match in matches:
            results[int(match[1])] = (match[0], match[2])

        # Order the dictionary by the key (Index of the amino accid)
        self.orderedMutant = collections.OrderedDict(sorted(results.items(), key=lambda t: t[0]))
        self.countMutant = len(self.orderedMutant) 
        print(self.countMutant)
        self.calcPosibilitys(self.countMutant)
        print(self.posibleCombinations)
        if self.posibleCombinations < 500:
            self.numMutant_label.configure(text=self.posibleCombinations,  text_color='snow')
            self.btnRun.configure(state='normal')
        else:
            self.numMutant_label.configure(text=self.posibleCombinations, text_color='red')
            self.btnRun.configure(state='disabled')

        # Konvertieren Sie das Dictionary in eine Liste von Listen
        table = []
        for k, v in self.orderedMutant.items():
            table.append([k] + list(v))
            
        # Konvertieren Sie die Tabelle in einen formatierten String
        table_str = tabulate(table, headers=['Pos', 'BASE-Accid', 'TARGET-Accid'], tablefmt='simple_grid', colalign=('center','center','center'))
        self.txtLog.configure(state=tkinter.NORMAL)
        self.txtLog.delete(0.0, tkinter.END)
        self.txtLog.insert(0.0, table_str)
        self.txtLog.configure(state=tkinter.DISABLED)
# ============================================================================
# ============================================================================

# ----------------------------------------------------------------------------
#                           Start of the Program
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    if not os.path.exists(resource_path('output')):
        os.mkdir(resource_path('output'))
#    if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/output'):
#        os.makedirs(os.path.dirname(os.path.realpath(__file__)) + '/output')
    # Run the main event loop
    app = App()
    app.mainloop()
# ============================================================================
# ============================================================================
