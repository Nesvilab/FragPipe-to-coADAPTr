"""
Author: Carolina Rojas Ramirez
Date: 12/06/2023
Script to add a FPOP mods only column to psm.tsv

"""

import tkinter
from tkinter import filedialog
import pandas as pd
import os
from PyQt5 import QtWidgets
import sys
import re
from itertools import combinations_with_replacement
import io

#set up Tkinter
root = tkinter.Tk()
root.withdraw()

#Makes it possible to select directories which Tkinter apparently does not do easily
CONFIG_FILE = 'config.txt'  # config file for saving last directory for fancy filedialog

def get_data(config_file):
    """
    Load folders of data using custom FileDialog class
    :param config_file: path to the config file with the initial directory for the file chooser
    :return: list of strings of full system folder paths to the folders chosen, updated input_dir
    """
    input_dir = get_last_dir(config_file)

    app = QtWidgets.QApplication(sys.argv)
    ex = FileDialog(input_dir)
    ex.show()
    app.exec_()
    files = ex.selectedFiles()

    new_base_dir = os.path.dirname(files[0])
    save_config(config_file, new_base_dir)
    return files


def get_last_dir(config_file):
    """
    parse the config file for the last directory used, to use as the initial directory when
    opening the file chooser.
    :param config_file: text file with a single directory (full system path) and nothing else
    :return: (string) directory path
    """
    with open(config_file, 'r') as config:
        line = config.readline()
        return line


def save_config(config_file, new_base_dir):
    """
    Update the config file with a new directory name
    :param config_file: file path to update
    :param new_base_dir: information to save in the config file
    :return: void
    """
    with open(config_file, 'w') as config:
        config.write(new_base_dir)



class FileDialog(QtWidgets.QFileDialog):
    """
    File chooser for raw data, created after extensive searching on stack overflow
    """
    def __init__(self, input_dir, *args):
        QtWidgets.QFileDialog.__init__(self, *args)
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.DirectoryOnly)
        self.setDirectory(input_dir)

        self.tree = self.findChild(QtWidgets.QTreeView)
        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

def modstring_processing(assignedmod_str):
    """
    Function to select FPOP mods only
    :param assignedmod_str:str
    :return: str
    """
    FPOP_massoffsetls = [15.9949, 31.9898, 47.9847, 13.9793, -43.0534,
                         -22.0320, -23.0159, -10.0319, 4.9735, -30.0106, -27.9949, -43.9898,
                         -25.0316, -9.0367]
    returnls = []
    # Iterate over proteins
    if isinstance(assignedmod_str, str):

        assignedmod_spl = assignedmod_str.split(",")
        for item in assignedmod_spl:

            for fpopmod in FPOP_massoffsetls:
                if str(fpopmod) in item:
                    returnls.append(item)


    returnstr = ",".join(returnls)

    return returnstr


def psmwithFPOPcolumn(FilePath, psmoverwrite_bool):
    """
    Function to add FPOP only mods column
    :param FilePath: Absolute path to tsv file
    :param file_type: File type (not extension but is it a psm, peptide or protein TSV file)
    :return: it depends
    """

    #Starting analysis
    print(f"~*~*~Reading file = {FilePath}~*~*~")


    #Create dataframe from file
    dataframe_item = pd.read_csv(FilePath, sep='\t')

    #How many lines there are in file
    rows = dataframe_item.shape[0]
    print(f"rows = {rows}")

    modifiedpsms =dataframe_item["Assigned Modifications"]


    FPOPonlycol = []
    # Iteriate over modified PSMs
    for modstring in modifiedpsms:
        # print(modstring)
        newstr = modstring_processing(modstring)
        FPOPonlycol.append(newstr)


    dataframe_item.insert(26, "FPOP Modifications", FPOPonlycol, True)

    outputdir = os.path.dirname(FilePath)

    #If user want to keep a psm file copy without FPOP column
    if psmoverwrite_bool:
        outputfilename = os.path.join(outputdir, "psm.tsv")
    else:
        outputfilename = os.path.join(outputdir, "fpop_psm.tsv")




    dataframe_item.to_csv(outputfilename, sep = "\t", index=False)

    # columns = dataframe_item.columns
    # print(columns)

    # print(f"Priot to error = {file_type}")


def multiexperiment_psm(psmoverwrite = None):
    """
    Function to gather PSMs counts (organized by residue and mass shifts) from all experiments
    :param mode: none, takes aggreagted PSMs files organized by residue and mass shift. Set to "PSMs" to calculate PSMs for each experiment
    :return: void
    """

    # Go thru all the directories outputed by FRAGPIpe for each analaysis
    selected_dirs = get_data(CONFIG_FILE)
    # main_dir = os.path.split(selected_dirs[0])[0]

    #Folder that contains experiments. Folder where FRAGPIPE would store everything.
    for folder in selected_dirs:

        os.chdir(folder)

        print(f"folder = {folder}")
        diritems = [x for x in os.listdir(folder)]
        # print(f"files = {diritems}")


        #For each experiments
        for item in diritems:
            # print(f"item = {item}")

            #Continue if the item is not a folder
            if item.find(".") > -1:
                continue
            else:
                #if the item is a file
                subdiritem = os.path.join(folder,item)

                print(f"subdirectory = {subdiritem}")

                subdirfiles = [x for x in os.listdir(subdiritem)]

                #If calculating residues and mass shift modification from a psm.tsv file

                for file in subdirfiles:
                    if "psm.tsv" == file:
                        # print(f"file = {file}")
                        filepath = os.path.join(subdiritem, file)
                        psmwithFPOPcolumn(filepath, psmoverwrite)

def main():
    """
    Main fcuntion to enable terminal usage
    @return: void
    """

    #Checking Python version
    majorversion = sys.version_info.major
    minorversion = sys.version_info.minor

    if majorversion < 3:
        print("Python version must be at least 3.7")
    elif majorversion == 3 and minorversion < 7:
        print("Python version must be at least 3.7")
    else:
        print("Python version is at least greater than or equal to 3.7")

        # Example adding a second attribute ['.\\fromFragPipe_tocoADAPTr.py', 'True']
        systemarguments = sys.argv

        # If there are two arguments it means and attribute was passed
        if len(systemarguments) == 2:

            # Second argument better be a bool
            overwriteattribute = systemarguments[1]

            if overwriteattribute.lower() == "true":
                # PSM file will be overwritten
                print("PSM file will be overwritten. A FPOP only column will be added, but it will be saved under the same name.")
                multiexperiment_psm(psmoverwrite=True)
            elif overwriteattribute.lower() == "false":
                # PSM file will be overwritten
                print("A copy of the PSM file with the FPOP only column and the name fpop_psm.tsv will be created.")
                multiexperiment_psm(psmoverwrite=False)
            else:
                print("Second attribute must be True or False.")


        # Assume that no second argument equals false
        elif len(systemarguments) == 1:
            print("A copy of the PSM file with the FPOP only column and the name fpop_psm.tsv will be created.")
            multiexperiment_psm()
        else:
            print("There are no system arguments?!")






if __name__ == '__main__':

    main()







