########################################
# LICENSE - GNU GPLv3
########################################
#
#    Aerofoil Utility, a toolset for aerofoil curve generation and analysis.
#    Copyright (C) 2023 Richard Davis
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/.


########################################
# IMPORTS
########################################

from math import sin
from math import cos
from math import tan
from math import radians

import numpy as np

import pandas as pd

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import webbrowser


########################################
# DEFINE FUNCTIONS
########################################

def callback(event):
    webbrowser.open_new(event.widget.cget("text"))

def sind(deg):
    deg = sin(radians(deg))
    return deg

def cosd(deg):
    deg = cos(radians(deg))
    return deg

def tand(deg):
    deg = tan(radians(deg))
    return deg

def read_dat_file(file_path=".\\UIUC_Selig_Database"):
    selig_aerofoil_header = ''
    selig_aerofoil_matrix = []
    with open(file_path, 'r') as file:
        selig_aerofoil_header = file.readline().strip()
        for line in file:
            values = [float(value) for value in line.split()]
            selig_aerofoil_matrix.append(values)
    selig_aerofoil_matrix = np.insert(selig_aerofoil_matrix, 1, 0, axis=1)
    exports_text_label_1_0.configure(text=selig_aerofoil_header)
    return selig_aerofoil_header, selig_aerofoil_matrix

def import_button_click():
    global file_path
    file_path = filedialog.askopenfilename(initialdir=".\\UIUC_Selig_Database", title="Select a dat file", filetypes=(("dat files", "*.dat"), ("all files", "*.*")))
    if file_path:
        curve_update()

def update_plot(curve):
    ax.clear()
    plot_x=curve[:,0]
    plot_y=curve[:,1]
    plot_z=curve[:,2]
    ax.plot(plot_x,plot_y,plot_z)
    ax.set_aspect('equal')
    axisscale = 2
    ax.set_xlim(xmin=(np.min(plot_x)-(axisscale*(np.max(plot_x)-np.min(plot_x)))),xmax=(np.max(plot_x)+(axisscale*(np.max(plot_x)-np.min(plot_x)))))
    ax.set_ylim(ymin=(np.min(plot_y)-(axisscale*(np.max(plot_y)-np.min(plot_y)))),ymax=(np.max(plot_y)+(axisscale*(np.max(plot_y)-np.min(plot_y)))))
    ax.set_zlim(zmin=(np.min(plot_z)-(axisscale*(np.max(plot_z)-np.min(plot_z)))),zmax=(np.max(plot_z)+(axisscale*(np.max(plot_z)-np.min(plot_z)))))
    plotcanvas.draw()

def update_matrix_output(curve):
    matrix_display.delete(1.0, tk.END)
    for row in curve:
        formatted_row = [f"{value:.5f}" for value in row]
        row_text = " ".join(formatted_row) + "\n"
        matrix_display.insert(tk.END, row_text)

def export_matrix(matrix):
    filetypes=[("text file", "*.txt"), ("Excel file", "*.xls"),("CSV file", "*.csv"),("dat files", "*.dat"), ("all files", "*.*")]
    filename = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=".txt")
    if filename:
        if filename.endswith(".txt"):
            np.savetxt(filename, matrix, delimiter='\t')
        elif filename.endswith(".csv"):
            np.savetxt(filename, matrix, delimiter=',')
        elif filename.endswith(".dat"):
            np.savetxt(filename, matrix, delimiter='\t')    
        elif filename.endswith(".xls"):
            df = pd.DataFrame(matrix)
            df.to_excel(filename, index=False)    

def curve_chord_fun(curve, chord):
    curve *= chord
    return curve

def curve_stretch_fun(curve, sx, sz):
    curve[:,0] *= sx
    curve[:,2] *= sz
    return curve

def curve_rotate_fun(curve, alpha, beta, gamma):
    Rz=np.array([[cosd(beta),-sind(beta),0],[sind(beta),cosd(beta),0],[0,0,1]])
    Ry=np.array([[cosd(alpha),0,sind(alpha)],[0,1,0],[-sind(alpha),0,cosd(alpha)]])
    Rx=np.array([[1,0,0],[0,cosd(gamma),-sind(gamma)],[0,sind(gamma),cosd(gamma)]])
    curve = np.matmul(curve, Rz)
    curve = np.matmul(curve, Ry)
    curve = np.matmul(curve, Rx)
    return curve

def curve_translate_fun(curve, dx, dy, dz):
    curve[:,0] += dx
    curve[:,1] += dy
    curve[:,2] += dz
    return curve

def curve_generation_fun(curve, chord, dx, dy, dz, alpha, beta, gamma, sx, sz):
    curve_chord = curve_chord_fun(curve, chord)
    curve_stretch = curve_stretch_fun(curve_chord, sx, sz)
    curve_rotate = curve_rotate_fun(curve_stretch, alpha, beta, gamma)
    curve_translate = curve_translate_fun(curve_rotate, dx, dy, dz)
    return curve_translate

def curve_update():
    global curve_translate
    curve_translate = []
    selig_aerofoil_header, selig_aerofoil_matrix = read_dat_file(file_path)
    curve_translate = curve_generation_fun(selig_aerofoil_matrix,float(inputs_entry_3_1.get()),float(inputs_entry_5_1.get()),float(inputs_entry_6_1.get()),float(inputs_entry_7_1.get()),float(inputs_entry_10_1.get()),float(inputs_entry_11_1.get()),float(inputs_entry_9_1.get()),float(inputs_entry_13_1.get()),float(inputs_entry_14_1.get()))
    update_plot(curve_translate)
    update_matrix_output(curve_translate)

def update_button_click(event):
    curve_update()

def export_button_click(event):
    export_matrix(curve_translate)


########################################
# CREATE WINDOW
########################################

root = tk.Tk()
root.geometry('1280x720')
root.title('Aerofoil Utility')

# Create the tab control (notebook)
tabControl = ttk.Notebook(root)
tabControl.grid(sticky='NESW')  # Fill the window

tabs = []


########################################
# TAB 0 - INFORMATION
########################################

tab0 = ttk.Frame(tabControl)
tabControl.add(tab0, text='Information')
tabs.append(tab0)

    # Configure the grid in the tab to give all extra space to the Canvas widget
tab0.grid_rowconfigure(0, weight=1)
tab0.grid_columnconfigure(0, weight=1)

    # Add a Canvas widget to the tab
canvas0 = tk.Canvas(tab0)
canvas0.grid(row=0, column=0, sticky='NESW')

    # Add vertical Scrollbar to the canvas
y_scroll0 = ttk.Scrollbar(tab0, orient='vertical', command=canvas0.yview)
y_scroll0.grid(row=0, column=1, sticky='NS')
canvas0['yscrollcommand'] = y_scroll0.set

    # Add horizontal Scrollbar to the canvas
x_scroll0 = ttk.Scrollbar(tab0, orient='horizontal', command=canvas0.xview)
x_scroll0.grid(row=1, column=0, sticky='EW')
canvas0['xscrollcommand'] = x_scroll0.set

    # Create a Frame within the Canvas
inner_frame0 = ttk.Frame(canvas0)
canvas0.create_window((0, 0), window=inner_frame0, anchor='nw')

########################################
# TAB 0 - GRID SIZINGS

inner_frame0.columnconfigure(0, minsize=410)
inner_frame0.columnconfigure(1, minsize=410)
inner_frame0.columnconfigure(2, minsize=410)

########################################
# TAB 0 - CONTENT, Add widgets to the inner_frame0 as needed

# Title
info_text_label_0_0 = tk.Label(inner_frame0, fg="#1f2224", text="AEROFOIL UTILITY", font=("Courier", 14, "bold"))
info_text_label_0_0.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

# Description
info_text_label_1_0 = tk.Label(inner_frame0, fg="#1f2224", text="A toolset for aerofoil curve generation and analysis.", font=("Courier", 10))
info_text_label_1_0.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

# GitHub Link
info_text_label_2_0 = tk.Label(inner_frame0, fg="#1f2224", text=r"https://github.com/davisrj/aerofoil_utility", cursor="hand2", font=("Courier", 10))
info_text_label_2_0.grid(row=2, column=0, columnspan=3, padx=5, pady=25)

# Richard Credit
info_text_label_3_0 = tk.Label(inner_frame0, fg="#1f2224", text="Created by Richard Davis, MSc\nCopyright 2023 Richard Davis GNU GPLv3\nRelease 1.0\nSupport me!", font=("Courier", 10))
info_text_label_3_0.grid(row=3, column=0, padx=5, pady=5)

info_text_label_4_0 = tk.Label(inner_frame0, fg="#1f2224", text=r"https://ko-fi.com/davisrj", cursor="hand2", font=("Courier", 10))
info_text_label_4_0.grid(row=4, column=0, padx=5, pady=5)
info_text_label_4_0.bind("<Button-1>", callback)

# Smith Credit
info_text_label_5_0 = tk.Label(inner_frame0, fg="#1f2224", text="With thanks to Ben Smith", font=("Courier", 10))
info_text_label_5_0.grid(row=5, column=0, padx=5, pady=5)

info_text_label_6_0 = tk.Label(inner_frame0, fg="#1f2224", text=r"https://github.com/benhicklingsmith", cursor="hand2", font=("Courier", 10))
info_text_label_6_0.grid(row=6, column=0, padx=5, pady=5)
info_text_label_6_0.bind("<Button-1>", callback)

# Selig Credit
info_text_label_3_1 = tk.Label(inner_frame0, fg="#1f2224", text="Aerofoil data provided with permission by:\nMichael Selig, Ph.d., Professor Emeritus\nUniversity of Illinois at Urbana-Champaign\nDept of Aerospace Engineering", font=("Courier", 10))
info_text_label_3_1.grid(row=3, column=1, padx=5, pady=5)

info_text_label_4_1 = tk.Label(inner_frame0, fg="#1f2224", text=r"https://m-selig.ae.illinois.edu/ads.html", cursor="hand2", font=("Courier", 10))
info_text_label_4_1.grid(row=4, column=1, padx=5, pady=5)
info_text_label_4_1.bind("<Button-1>", callback)

# Credit
info_text_label_5_1 = tk.Label(inner_frame0, fg="#1f2224", text="Utilising OpenCASCADE", font=("Courier", 10))
info_text_label_5_1.grid(row=5, column=1, padx=5, pady=5)

info_text_label_6_1 = tk.Label(inner_frame0, fg="#1f2224", text=r"https://www.opencascade.com/", cursor="hand2", font=("Courier", 10))
info_text_label_6_1.grid(row=6, column=1, padx=5, pady=5)
info_text_label_6_1.bind("<Button-1>", callback)

# Evans Credit
info_text_label_3_2 = tk.Label(inner_frame0, fg="#1f2224", text="FLITE2D provided with permission by:\nBen Evans, Ph.d., Professor\nSwansea University\nDept of Aerospace Engineering", font=("Courier", 10))
info_text_label_3_2.grid(row=3, column=2, padx=5, pady=5)

info_text_label_4_2 = tk.Label(inner_frame0, fg="#1f2224", text=r"https://github.com/DrBenEvans", cursor="hand2", font=("Courier", 10))
info_text_label_4_2.grid(row=4, column=2, padx=5, pady=5)
info_text_label_4_2.bind("<Button-1>", callback)

# GMSH Credit
info_text_label_5_2 = tk.Label(inner_frame0, fg="#1f2224", text="Utilising gmsh", font=("Courier", 10))
info_text_label_5_2.grid(row=5, column=2, padx=5, pady=5)

info_text_label_6_2 = tk.Label(inner_frame0, fg="#1f2224", text=r"https://gmsh.info/", cursor="hand2", font=("Courier", 10))
info_text_label_6_2.grid(row=6, column=2, padx=5, pady=5)
info_text_label_6_2.bind("<Button-1>", callback)

    # Update canvas's scroll region as inner_frame changes
def update_scrollregion0(event):
    canvas0.configure(scrollregion=canvas0.bbox('all')) 

canvas0.bind('<Configure>', update_scrollregion0)


########################################
# TAB 1 - AEROFOIL CURVES
########################################

tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Aerofoil Curves')
tabs.append(tab1)

    # Configure the grid in the tab to give all extra space to the Canvas widget
tab1.grid_rowconfigure(0, weight=1)
tab1.grid_columnconfigure(0, weight=1)

    # Add a Canvas widget to the tab
canvas1 = tk.Canvas(tab1)
canvas1.grid(row=0, column=0, sticky='NESW')

    # Add vertical Scrollbar to the canvas
y_scroll1 = ttk.Scrollbar(tab1, orient='vertical', command=canvas1.yview)
y_scroll1.grid(row=0, column=1, sticky='NS')
canvas1['yscrollcommand'] = y_scroll1.set

    # Add horizontal Scrollbar to the canvas
x_scroll1 = ttk.Scrollbar(tab1, orient='horizontal', command=canvas1.xview)
x_scroll1.grid(row=1, column=0, sticky='EW')
canvas1['xscrollcommand'] = x_scroll1.set

    # Create a Frame within the Canvas
inner_frame1 = ttk.Frame(canvas1)
canvas1.create_window((0, 0), window=inner_frame1, anchor='nw')

########################################
# TAB 1 - GRID SIZINGS

inner_frame1.columnconfigure(0, minsize=50)

########################################
# TAB 1 - CONTENT, Add widgets to the inner_frame1 as needed

# Import Button
inputs_button_0_0 = tk.Button(inner_frame1, text="Import Selig Formatted Aerofoil .dat File", command=import_button_click)
inputs_button_0_0.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

# Curve Name
exports_text_label_1_0 = tk.Label(inner_frame1, fg="#1f2224", text="", font=("Courier", 12, "bold"))
exports_text_label_1_0.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="NESW")

# Chord Length
inputs_text_label_2_0 = tk.Label(inner_frame1, fg="#1f2224", text="Chord Length", font=("Courier", 12, "bold"))
inputs_text_label_2_0.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

inputs_text_label_3_0 = tk.Label(inner_frame1, fg="#1f2224", text="Chord Length", font=("Courier", 10))
inputs_text_label_3_0.grid(row=3, column=0, padx=5, pady=5, sticky="w")

inputs_entry_3_1 = tk.Entry(inner_frame1, fg="#1f2224")
inputs_entry_3_1.insert(0, "1")
inputs_entry_3_1.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Translation
inputs_text_label_4_0 = tk.Label(inner_frame1, fg="#1f2224", text="Translation", font=("Courier", 12, "bold"))
inputs_text_label_4_0.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

inputs_text_label_5_0 = tk.Label(inner_frame1, fg="#1f2224", text="X axis, Roll", font=("Courier", 10))
inputs_text_label_5_0.grid(row=5, column=0, padx=5, pady=5, sticky="w")

inputs_entry_5_1 = tk.Entry(inner_frame1, fg="#1f2224")
inputs_entry_5_1.insert(0, "0")
inputs_entry_5_1.grid(row=5, column=1, padx=5, pady=5, sticky="w")

inputs_text_label_6_0 = tk.Label(inner_frame1, fg="#1f2224", text="Y axis, Pitch", font=("Courier", 10))
inputs_text_label_6_0.grid(row=6, column=0, padx=5, pady=5, sticky="w")

inputs_entry_6_1 = tk.Entry(inner_frame1, fg="#1f2224")
inputs_entry_6_1.insert(0, "0")
inputs_entry_6_1.grid(row=6, column=1, padx=5, pady=5, sticky="w")

inputs_text_label_7_0 = tk.Label(inner_frame1, fg="#1f2224", text="Z axis, Yaw", font=("Courier", 10))
inputs_text_label_7_0.grid(row=7, column=0, padx=5, pady=5, sticky="w")

inputs_entry_7_1 = tk.Entry(inner_frame1, fg="#1f2224")
inputs_entry_7_1.insert(0, "0")
inputs_entry_7_1.grid(row=7, column=1, padx=5, pady=5, sticky="w")

# Rotation
inputs_text_label_8_0 = tk.Label(inner_frame1, fg="#1f2224", text="Rotation", font=("Courier", 12, "bold"))
inputs_text_label_8_0.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="w")

inputs_text_label_9_0 = tk.Label(inner_frame1, fg="#1f2224", text="X axis, Roll, γ", font=("Courier", 10))
inputs_text_label_9_0.grid(row=9, column=0, padx=5, pady=5, sticky="w")

inputs_entry_9_1 = tk.Entry(inner_frame1, fg="#1f2224")
inputs_entry_9_1.insert(0, "0")
inputs_entry_9_1.grid(row=9, column=1, padx=5, pady=5, sticky="w")

inputs_text_label_10_0 = tk.Label(inner_frame1, fg="#1f2224", text="Y axis, Pitch, α", font=("Courier", 10))
inputs_text_label_10_0.grid(row=10, column=0, padx=5, pady=5, sticky="w")

inputs_entry_10_1 = tk.Entry(inner_frame1, fg="#1f2224")
inputs_entry_10_1.insert(0, "0")
inputs_entry_10_1.grid(row=10, column=1, padx=5, pady=5, sticky="w")

inputs_text_label_11_0 = tk.Label(inner_frame1, fg="#1f2224", text="Z axis, Yaw, β", font=("Courier", 10))
inputs_text_label_11_0.grid(row=11, column=0, padx=5, pady=5, sticky="w")

inputs_entry_11_1 = tk.Entry(inner_frame1, fg="#1f2224")
inputs_entry_11_1.insert(0, "0")
inputs_entry_11_1.grid(row=11, column=1, padx=5, pady=5, sticky="w")

# Stretch
inputs_text_label_12_0 = tk.Label(inner_frame1, fg="#1f2224", text="Stretch", font=("Courier", 12, "bold"))
inputs_text_label_12_0.grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky="w")

inputs_text_label_13_0 = tk.Label(inner_frame1, fg="#1f2224", text="Stretch in local x axis", font=("Courier", 10))
inputs_text_label_13_0.grid(row=13, column=0, padx=5, pady=5, sticky="w")

inputs_entry_13_1 = tk.Entry(inner_frame1, fg="#1f2224")
inputs_entry_13_1.insert(0, "1")
inputs_entry_13_1.grid(row=13, column=1, padx=5, pady=5, sticky="w")

inputs_text_label_14_0 = tk.Label(inner_frame1, fg="#1f2224", text="Stretch in local z axis", font=("Courier", 10))
inputs_text_label_14_0.grid(row=14, column=0, padx=5, pady=5, sticky="w")

inputs_entry_14_1 = tk.Entry(inner_frame1, fg="#1f2224")
inputs_entry_14_1.insert(0, "1")
inputs_entry_14_1.grid(row=14, column=1, padx=5, pady=5, sticky="w")

# Update
update_button_15_0 = tk.Button(inner_frame1, text="Update")
update_button_15_0.grid(row=15, column=0, columnspan=2, padx=5, pady=5)
update_button_15_0.bind("<Button-1>", update_button_click)

# Axes
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot(0,0,0)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
#ax.set_box_aspect([1, 1, 1])
ax.set_aspect('equal') 
plotcanvas = FigureCanvasTkAgg(fig, master=inner_frame1)
plotcanvas.get_tk_widget().grid(row=0,column=2,rowspan=16,columnspan=3)

# Matrix
matrix_display = tk.Text(inner_frame1, height=28, width=30)
matrix_display.grid(row=0, column=5, rowspan=15, columnspan=3, padx=5, pady=5, sticky="n")

# Export
exports_button_15_5 = tk.Button(inner_frame1, text="Export")
exports_button_15_5.grid(row=15, column=5, columnspan=3, padx=5, pady=5)
exports_button_15_5.bind("<Button-1>", export_button_click)


    # Update canvas's scroll region as inner_frame changes
def update_scrollregion1(event):
    canvas1.configure(scrollregion=canvas1.bbox('all'))

canvas1.bind('<Configure>', update_scrollregion1)


########################################
# CLOSE LOOP
########################################

    # Configure the root grid to distribute space between widgets
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
