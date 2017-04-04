2004 09 18, Alex Li


This program summarizes the sales report from a directory
of Excel files to produce a summary report.  


The Situation
=============
Each directory represents a month.

Each Excel file contains receipts for a week (7 days).

Each worksheet contains receipts for a day.  The receipts
are listed horizontally.  We will have to take note of 
the worksheet date, since our summary is a monthly report.

Invoice Number = C4, G4, K4, O4, ...etc 

If the Invoice Number is empty, then there is no invoice at
that position.

If the Invoice Number is not empty, then we need to extract:
SUB (subtotal) 		 = D23, H23, L23, ...etc
SER (service charge) = D24
BAR	(bartender tips) = D25
GST					 = D26
PST					 = D27
TOT (total)			 = D28  

Except in January, all other months will have to take a
peek at an Excel file in the previous month, that may
contain their dates and receipts.

Once we get all worksheets, we can summarize them into
a monthly summary report.


Our Steps
=========
Step 1: Given a directory

Step 2: Summarize the files in the directory into our data 
structure.  The list of files are restricted to the filtering 
rule.

*****************************************************************
* THE FILTERING RULE
* ==================
* All excel files in a given directory, except the summary file,
* which has a "_MONTH_" in it, are included in the summarization.
*****************************************************************

Step 3: Get the receipts in the previous month directory.

Step 4: Write out the data structure into a summary file.
Need to generate the summary file name.
If the summary file already exists, rename the existing file
with a ".old" extension.  Any ".old" extension file will be
overwritten.  Finally we save teh summary file.

Step 5: Return any feedback.


Build Instruction
=================
1) Get the python source
2) In the source directory, run:

	python setup.py py2exe

(For help on py2exe, run: python setup.py py2exe --help)

3) All generated files are now located in the directory "dist".
4) Distribute the whole directory to your users.
