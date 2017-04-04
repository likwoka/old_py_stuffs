import unittest


def run_test():
    '''Temporary unit test.'''
    
    dirpath = r"C:\_share\sandbox\sumsales\Aug_03"

    # Test getting the list of excel files.    
    excelfiles = get_excel_files(dirpath, 'AUG', '03')
    
    if len(excelfiles) != 5:
        print "Error in get_excel_files, result is:", excelfiles

    # Test report path generation.
    reportpath = get_report_path(dirpath, 'AUG', '03')
    
    if reportpath != os.path.join(dirpath, "T_AUG_MONTH_03.xls"):
        print "Error in get_report_path, result is:", reportpath

    # Test extracting data from an Excel file.


    # Test summarizing the data


    # Test writing the summary report    

