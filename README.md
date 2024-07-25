# FragPipe-to-coADAPTr
Standalone script to add FPOP/oxidative modifications column to FragPipe psm tables

Hello!

Fast photochemical oxidation of proteins ([FPOP](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6690683/)) is a powerful technique to determine structural rearrengments of proteins at the single protein and proteome wide level. Since FragPipe 20.1, an FPOP workflow has been included in FragPipe. Since version 21, FPOP workflow has included detailed Mass Offset mode to ensure only searching for FPOP relevann modifications and not any oxidative modification. Now, there is a software available for the downstream analysis (e.g. extendof modification quantitation, graphing) of FPOP data from FragPipe analysis. The new software, [coADAPTr] (https://github.com/LJonesGroup/coADAPTr) has a massive improvement (aaprox. 20x) in analysis time vs manually processing. 

## Using FragPipe output with coADAPTr
In order to make possible fragPipe output analysis with coADAPTr a script that can be run thru terminal is made avaialble in this repository (full integration into FragPipe coming soon). Detailed instrcution follow so any user can run the script (Graphical user Interface is included for FragPipe output folder selection). 

#### 1. Download repository code

