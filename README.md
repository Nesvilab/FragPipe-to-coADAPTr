# FragPipe-to-coADAPTr
Standalone script to add FPOP/oxidative modifications column to FragPipe psm tables

Hello!

Fast photochemical oxidation of proteins ([FPOP](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6690683/)) is a powerful technique to determine structural rearrengments of proteins at the single protein and proteome wide level. Since FragPipe 20.1, [an FPOP workflow has been included in FragPipe](https://pubs.acs.org/doi/full/10.1021/acs.analchem.3c02388). Since version 21, FPOP workflow has included detailed Mass Offset mode to ensure only searching for FPOP relevann modifications and not any oxidative modification. Now, there is a software available for the downstream analysis (e.g. extendof modification quantitation, graphing) of FPOP data from FragPipe analysis. The new software, [coADAPTr](https://github.com/LJonesGroup/coADAPTr) has a massive improvement (aaprox. 20x) in analysis time vs manually processing. 

## Using FragPipe output with coADAPTr
In order to make possible fragPipe output analysis with coADAPTr a script that can be run thru terminal is made avaialble in this repository (full integration into FragPipe coming soon). Detailed instrcution follow so any user can run the script (Graphical user Interface is included for FragPipe output folder selection). 

  1. Download the whole fragPipe-to-coADAPTr repo (to have a local copy of license and README files) or download python file only
  2. In the same folder where fromFragPipe_tocoADAPTr.py is located open a terminal window (In Windows Powershell is recommended)
  3. Run the command: python .\fromFragPipe_tocoADAPTr.py ("python .\fromFragPipe_tocoADAPTr.py False" is also acceptable)
  ##### Note: 
  ##### - This requires a working Python installation (preferable version 3.7 or above).
  ##### - The script will check the Python version is the appropriate one and it will let the user know that it will create a copy of the orginal psm file name "fpop_psm.tsv.
  ##### - To use overwrite mode run the command python .\fromFragPipe_tocoADAPTr.py True. This mode will write overwrite the psm file (the only modification is adding the FPOP only column)
  4. A dialong window will appeared prompting to "Choose FragPipe results folder". Select desired results folder.
  5. Script will start running. FPOP experiments usually have more than one experiment (control -vs- FPOP, no laser control, replicates, etcc..) to determine as close as possible background oxidation and FPOP oxidation. The script will go over each experimental folder and search for psm.tsv file and performed the column addition. If for any reason, the fragPipe results were not separted into experiments and there is only one psm.tsv file with no folder experiment, placed this fil einside a folder, inside the FragPipe folder so it can be properly detected by fromFragPipe_tocoADAPTr.py script.
  6. Check target psm files with new added "FPOP Modifications" column. Now these files can be used by coADAPTr.



