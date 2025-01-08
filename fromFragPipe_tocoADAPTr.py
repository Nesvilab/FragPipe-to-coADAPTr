"""
Author: Carolina Rojas Ramirez
Date: 12/06/2023
Script to add a FPOP mods only column to psm.tsv

"""

import tkinter
from tkinter import filedialog
import pandas as pd
import os
import sys
import re
import numpy as np
from pyteomics import mass

#set up Tkinter
root = tkinter.Tk()
root.withdraw()

def modstring_processing(assignedmod_str):
    """
    Function to select FPOP mods only
    :param assignedmod_str:str
    :return: str
    """
    FPOP_massoffsetls = [15.9949, 31.9898, 47.9847, 13.9793, -43.0534,
                         -22.0320, -23.0159, -10.0319, 4.9735, -30.0106, -27.9949, -43.9898,
                         -25.0316, -9.0367, 67.9874]
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

def modstring_processingDIA(massoffsets_str, unimodict_val):
    """
    Function to select FPOP mods only
    :param assignedmod_str:str
    :return: str
    """
    print(massoffsets_str)

    outls = []

    FPOP_massoffsetls = [15.9949, 31.9898, 47.9847, 13.9793, -43.0534,
                         -22.0320, -23.0159, -10.0319, 4.9735, -30.0106, -27.9949, -43.9898,
                         -25.0316, -9.0367, 67.9874]



    # Including localization
    modregex = re.compile(
        "\([0-9]*.[0-9]*\)|\(Unimod:[0-9]*.[0-9]*\)",
        re.I)
    mod = modregex.finditer(massoffsets_str)
    if mod:
        # If modifications were found iteriate over each one
        truelocationoffset = 0
        for item in mod:
            print(f"moditem = {item}")
            # get modification string
            locations = item.span()

            # Extract modification
            massshift = massoffsets_str[locations[0]:locations[1]]
            # Remove parenthesis
            massoffset = massshift[1:-1]
            # Extract residue after the modification string
            truelocationoffset += abs(locations[0] - locations[1])
            #Handeling n-termcases
            if locations[0] == 0:
                residuestr = massoffsets_str[locations[1]]
                truelocation = 1
            else:
                try:
                    residuestr = massoffsets_str[locations[1]]

                # Mod at the c-term
                except IndexError:
                    residuestr = massoffsets_str[locations[0]-1]
                truelocation = locations[1] + 1 - truelocationoffset




            # print(f"moditem = {massoffset}")
            # For sanity check reconstrcut mass offset string (can simplified later)
            # print(unimodict)

            print(truelocationoffset)

            if "UniMod" in massoffset:
                massoffset_spl = massoffset.split(":")
                massoffset_unimodval = massoffset_spl[1]
                massoffset_val = unimodict_val[int(massoffset_unimodval)]
                if massoffset_val in FPOP_massoffsetls:
                    residuemassoffset = f"{truelocation}{residuestr}({massoffset_val})"
                    outls.append(residuemassoffset)
            else:
                if residuestr != "X":
                    residue_mw = mass.calculate_mass(residuestr) - mass.calculate_mass(formula='H2O')
                else:
                    residue_mw = mass.calculate_mass("K") - mass.calculate_mass(formula='H2O')
                residue_mod = float(massoffset) - residue_mw

                if round(float(residue_mod), 4) in FPOP_massoffsetls:
                    residuemassoffset = f"{truelocation}{residuestr}({round(float(residue_mod), 4)})"
                    outls.append(residuemassoffset)







    outstr = ','.join(outls)

    return outstr


def precursorwithFPOPcolumn(psmoverwrite_bool):
    """
    Function to add FPOP only mods column
    :param FilePath: Absolute path to tsv file
    :param file_type: File type (not extension but is it a psm, peptide or protein TSV file)
    :return: it depends
    """

    #Starting analysis

    FilePath = filedialog.askopenfilename(title="Choose report file")
    print(f"~*~*~Reading file = {FilePath}~*~*~")


    #Create dataframe from file
    dataframe_item = pd.read_csv(FilePath, sep='\t')

    #How many lines there are in file
    rows = dataframe_item.shape[0]
    print(f"rows = {rows}")

    modifiedpsms =dataframe_item["Modified.Sequence"]

    fragpipeinstallfolder = filedialog.askdirectory(title="Choose FragPipe Installation folder")
    unimodfile_path = os.path.join(fragpipeinstallfolder, "tools", "UniModData.tsv")
    unimoddf = pd.read_csv(unimodfile_path, sep="\t")

    # unimod dictionary
    unimodict = {}
    for idx in unimoddf.index:
        monomass = round(unimoddf.loc[idx, "monoMass"], 4)
        unimodid = unimoddf.loc[idx, "id"]

        if np.isnan(unimodid) or unimodid in unimodict.keys():
            continue
        else:
            unimodict[int(unimodid)] = float(monomass)


    FPOPonlycol = []
    # Iteriate over modified PSMs
    for modstring in modifiedpsms:
        # print(modstring)
        newstr = modstring_processingDIA(modstring, unimodict)
        FPOPonlycol.append(newstr)


    dataframe_item.insert(16, "FPOP Modifications", FPOPonlycol, True)

    outputdir = os.path.dirname(FilePath)

    #If user want to keep a psm file copy without FPOP column
    if psmoverwrite_bool:
        outputfilename = os.path.join(outputdir, "report.tsv")
    else:
        outputfilename = os.path.join(outputdir, "report_coADAPTr.tsv")




    dataframe_item.to_csv(outputfilename, sep = "\t", index=False)

    # columns = dataframe_item.columns
    # print(columns)

    # print(f"Priot to error = {file_type}")

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

    folder = filedialog.askdirectory(title = "Choose FragPipe results folder")
    os.chdir(folder)

    print(f"folder = {folder}")
    diritems = [x for x in os.listdir(folder)]
    # print(f"files = {diritems}")

    # For each experiments
    for item in diritems:
        # print(f"item = {item}")

        # Continue if the item is not a folder
        if item.find(".") > -1:
            continue
        else:
            # if the item is a file
            subdiritem = os.path.join(folder, item)

            # print(f"subdirectory = {subdiritem}")

            subdirfiles = [x for x in os.listdir(subdiritem)]

            # If calculating residues and mass shift modification from a psm.tsv file

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

    # main()

    precursorwithFPOPcolumn(False)






