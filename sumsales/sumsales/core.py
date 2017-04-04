'''
The core business logic.  Both GUI and CommandLine will call this
module.
'''


import os, sys, glob, fnmatch
from win32com.client import Dispatch


#----------------------------------------------------------------------------
# Program constants.

# Monthly report's title, visible when printing out the report.
# Sub in month, year.
REPORT_TITLE = "T-DOT's %s 20%s Sales"

# Filenames satisfied this pattern are to be
# considered an Excel file that we want to
# summarize.
# Sub in month, year.
EXCEL_FILE_FILTER = 'T_%s*_*_%s.xls' 


# Filenames satisfied this pattern are to be
# considered an Excel file with receipts 
# spanning 2 months, such as the last few
# days of a month and the first few days
# of the next month.  There should be only
# at max 1 such file in a directory (which
# represents a month).
# Sub in prev_month, month, year.
MIX_MONTH_EXCEL_FILE_FILTER = 'T_%s*_%s*_%s.xls' 


# If we found any file that satisfies either
# patterns, then it means we don't have to
# search for receipts in the previous month's
# directory.
# Sub in month, year.
FIRST_OF_MONTH_FILENAMES = ['T_%s1_*_%s.xls', 'T_%s01_*_%s.xls']


# The name of the summary report.
# Sub in month, year.
SUMMARY_FILENAME = 'T_%s_MONTH_%s.xls'


# The OLD summary report extension.
# We rename any existing summary report with
# this extension so that we can create a new
# summary report without losing old data.
OLD_EXT = '.old'


# The month sequence, we use this to determine
# the previous/next month...etc.
MONTH = ['JAN', 'FEB', 'MAR', 'APR',
         'MAY', 'JUN', 'JUL', 'AUG',
         'SEP', 'OCT', 'NOV', 'DEC']


# We are generating the sequence of columns,
# up to a total of 104 (26 * 4) columns, ex:
# A, B, C, ... AA, AB, ... BA, BB, ... CA, CB ... CZ.
def generate_columns():
    import string
    
    result = []
    for alphabet in string.ascii_uppercase:
        result.append(alphabet)

    for alphabet in string.ascii_uppercase:
        result.append("A" + alphabet)

    for alphabet in string.ascii_uppercase:
        result.append("B" + alphabet)

    for alphabet in string.ascii_uppercase:
        result.append("C" + alphabet)

    return result


# The worksheet column sequence.
COLUMNS = generate_columns()


# The global Excel Application object
app = None


#----------------------------------------------------------------------------
# Data Model.  No business logic attached. (Not so OO, but clean layers)

class Receipt:
    '''
    A receipt lives in a Worksheet.
    '''
    def __init__(self, invoice_id):
        self.invoice_id = invoice_id
        self.sub = 0
        self.ser = 0
        self.bar = 0
        self.gst = 0
        self.pst = 0
        self.tot = 0

    def __cmp__(self, other):
        '''
        An internal compare method.  We are comparing
        the invoice_id as text.
        '''
        self_id = self.invoice_id.upper()
        other_id = getattr(y, 'invoice_id').upper()

        # There should be no case where they would be equal,
        # since every invoice has an unique invoice id!
        if self_id < other_id:
            return -1
        else:
            return 1

        
class Worksheet(list):
    '''
    A Worksheet lives in a Workbook.  It also
    contains many receipts of the same day.
    '''
    def __init__(self, name):
        self.name = name
        list.__init__(self)


class Workbook(list):
    '''
    A Workbook contains some worksheets, each represents
    a day.  A Workbook can be considered a weekly
    collection of receipts.
    '''
    def __init__(self, name):
        list.__init__(self)
        

#----------------------------------------------------------------------------
# The business logic.


class DirectoryNotFoundError(Exception):
    def __init__(self, path):
        self.msg = "Directory <%s> not found." % path


def get_excel_files(path, month, year):
    '''
    Return a list of Excel files according to the filtering rule,
    in ascending date order.

    path - a string of the path to the directory we are summarizing.    
    '''

    result = []     # The result to return.
    comparator = [] # A list used to sort the result. 
    
    tmplist = glob.glob(os.path.join(path,
        EXCEL_FILE_FILTER % (month, year)))

    # The starting position of the date in the filename.
    start =len('T_%s' % month)


    for fullpath in tmplist:
        
        filename = os.path.split(fullpath)[1]

        if not fnmatch.fnmatch(filename,
            SUMMARY_FILENAME % (month, year)):
            # This is not a summary report, it should be 
            # a weekly report that we want to summarize.
            # So we add it to the list here.  Before we do
            # so, we need to sort their sequence first.
    
            try:
                date = int(filename[start:start+2])
            except ValueError:
                date = int(filename[start])

            if len(result) == 0:
                # This is the first element, so we just
                # insert it at the beginning.
                result.append(fullpath)
                comparator.append(date)
            else:
                # Need to loop through the comparator
                # to determine the insert position
                i = 0
                while date > comparator[i]:
                    i = i + 1

                    # We are at the end of the comparator,
                    # so let's break the loop and insert
                    # it to the end of the result.
                    if i == len(comparator):
                        break;
                    
                result.insert(i, fullpath) 
                comparator.insert(i, date) 
                    
    return result


def get_month_year(path):
    '''
    Return a tuple of (month, year) that we are summarizing.
    Both values are string type.

    path - a string of the path to the directory we are summarizing.
           We want this because the last directory would be named as
           MMM_YY, ex: AUG_03.
    '''
    notused, secondhalf = os.path.split(os.path.abspath(path))
    return secondhalf.upper().split('_') 
    

def get_report_path(path, month, year):
    '''
    Return a string of the monthly report full path.

    path - a string of the path to the directory we are summarizing.
    month - a string of month in MMM format.
    year - a string of year in YY format.
    '''
    return os.path.join(path, SUMMARY_FILENAME % (month, year))


def rename_any_existing_report(path):
    '''
    Rename any existing summary report with the OLD_EXT
    extension.
    
    path - a string of fullpath to the summary report.
    '''
    # If the report already exists, we rename the existing
    # report with an OLD_EXT extension.
    # If it does not exist, we don't do anything, just exit
    # this function.
    if os.path.exists(path):

        # The name of the old file.
        oldfile = path + OLD_EXT

        try:
            # If the old file already exists, we just overwrite it.
            # On Windows, os.rename() would fail if old file already
            # exists, therefore we have to os.remove() it first.
            if os.path.exists(oldfile):
                os.remove(oldfile)

            os.rename(path, oldfile)

            print >> sys.stdout, \
                "Renamed existing report with .old extension"
            
        except OSError:
            print >> sys.stderr, \
                "Error!  The summary file cannot be saved. " \
                "May be you have it opened in the Excel program? " \
                "In that case, close that file first.  If you " \
                "do not have it opened, then it looks like that " \
                "file is owned by someone else and you cannot " \
                "modify it.  In that case ask the owner to run " \
                "this program."

            
    
def sum(path):
    '''
    Start the summarization process by reading each excel file
    and write the result to a summary Excel file.
    '''
    path = os.path.abspath(path)
    
    month, year = get_month_year(path)
    excelfiles = get_excel_files(path, month, year)
    reportpath = get_report_path(path, month, year)

    workbooks = []
    global app

    try:
        app = Dispatch('Excel.Application')
        
        for excelfile in excelfiles:
            workbook = sum_a_workbook(excelfile, month)
            workbooks.append(workbook)

        # Initialize the variable.        
        found_first_of_month = False

        for filename in FIRST_OF_MONTH_FILENAMES:        
            if glob.glob(os.path.join(path,filename % (month, year))) != []:
                # We found the first of month file!  No need to
                # look into the previous month's directory.
                found_first_of_month = True
                break;

        if not found_first_of_month:
            workbook = sum_receipts_in_previous_month(path, month, year)
             
            if workbook is not None and len(workbook) > 0:
                # This workbook is not empty, we found some receipts
                # so let's add them to the beginning.
                workbooks.insert(0, workbook)


        report = MonthlyReport(month, year, app)
        report.create(workbooks)

        # We rename it at this last stage.  Why?  Because we don't
        # want to rename anything if our report cannot be
        # generated successfully.
        rename_any_existing_report(reportpath)

        report.write(reportpath)

        print >> sys.stdout, "Summary file is written to", reportpath
        print >> sys.stdout, 'Done.'        

    finally:
        # Delete the reference.  Remember that the app object
        # is actually a COM Server, which means that there is
        # only 1 instance for the whole machine at runtime.
        # If you call app.Quit(), it will actually close
        # all Excel instances, even those that are opened
        # by the user.
        del app


def sum_a_workbook(excelfile, month):
    '''
    Summarize an Excel.Workbook and return
    a Workbook instance.

    excelfile - a string of path to the Excel file.
    '''
    myWorkbook = Workbook(excelfile)
    global app    

    try:
        print >> sys.stdout, "Read", excelfile
        workbook = app.Workbooks.Open(excelfile)

        sheets = workbook.Sheets    
        for sheet in sheets:
            name = sheet.Name.strip()
            if name.startswith(month) or \
               name.endswith(month):
                # This worksheet belongs to this month,
                # we will collect all receipts on it.
                # There are 2 cases Mar13 or 13Mar
                myWorkbook.append(sum_a_worksheet(sheet))

    finally:
        # False means don't save changes.  We are opening
        # the excel files for read only.
        workbook.Close(False)
    
    return myWorkbook    


def sum_a_worksheet(sheet):
    '''
    Summarize an Excel.Worksheet in a workbook and
    return a Worksheet instance.

    sheet - an Excel.Worksheet instance.
    '''
    myWorksheet = Worksheet(sheet.Name)

    # A worksheet will contains many receipt for
    # that day, we create them in this loop.
    # Receipt looping rules   
    for col in COLUMNS[2::4]:
        
        invoice_cell = col + '4'        
        invoice_id = sheet.Range(invoice_cell).Value

        if invoice_id is not None and invoice_id.strip(): 
            # There is a receipt. The Id is not None and not empty space.

            # This is the column for the amounts,
            # which is the next column
            col2 = COLUMNS[COLUMNS.index(col)+1]

            r = Receipt(invoice_id)
            rows = range(23, 29)
            properties = ('sub',
                          'ser',
                          'bar',
                          'gst',
                          'pst',
                          'tot')
            
            for property, row in zip(properties, rows):
                setattr(r, property, sheet.Range(col2 + str(row)).Value2)
                          
            myWorksheet.append(r)

    return myWorksheet


def sum_receipts_in_previous_month(oldpath, month, year):
    '''
    Return a Workbook that contains the receipts of
    this month but are stored in the excel file of
    the previous month's directory.

    oldpath - a string of path to the current month's directory.
    month - a string of current month.
    year - a string of current year.
    '''
    # Create the path to the previous month's folder.
    prev_month = MONTH[MONTH.index(month)-1]

    if month == 'JAN':
        # if it is JAN, then previous month is DEC,
        # which is in last year.  So we have to
        # roll back a year as well.
        year = str(int(year) - 1).zfill(2)
        
    newpath = os.path.join(
        os.path.split(os.path.abspath(oldpath))[0],
        '%s_%s' % (prev_month, year))

    if not os.path.isdir(newpath):
        raise DirectoryNotFoundError(newpath)

    # Find the excel file that should contain the worksheets
    # that we want.  Note that there should only be one.
    excelfiles = get_excel_files(newpath, prev_month, year)
    newfile = None
    for excelfile in excelfiles:
        
        if fnmatch.fnmatch(os.path.split(excelfile)[1],
            MIX_MONTH_EXCEL_FILE_FILTER % (prev_month, month, year)):
            newfile = excelfile
            break;
    
    # Summarize the workbook
    if newfile is not None:
        return sum_a_workbook(os.path.join(newpath, newfile), month)
    return None
    

class MonthlyReport:
    
    def __init__(self, month, year, excel_app_obj):
        self.month = month
        self.year = year
        self.app = excel_app_obj

        # Private members.        
        self._sheetObj = None
        self._wbObj = None



    def _cell(self, row, col):
        '''
        Return an Excel.Range object representing this cell.
        
        row - a int representing the row.
        col - a character (A, B, C...) representing the column.       
        '''
        return self._sheetObj.Range(col + str(row))



    def _cells(self, row1, col1, row2, col2):
        '''
        Return an Excel.Range object representing the rectangle
        of cells.
        
        row1, row2 - an int representing the row.
        col1, col2 - a character (A, B, C...) representing the column.
        '''
        return self._sheetObj.Range(col1 + str(row1) + ':'
                                     + col2 + str(row2))



    def _fill_row_labels(self, row_index):
        '''
        Fill in the row labels.
        row_index - an int, the starting row index.
        '''
        col = 'A'
        rows = range(row_index, row_index + 7)
        labels = ('SUB TOTAL',
                  '10% SERVICE',
                  'BAR TAX 2%',
                  'GST',
                  'PST',
                  'TOTAL')

        for row, label in zip(rows, labels):
            self._cell(row, col).Value = label



    def _fill_row_totals(self, row_index):
        '''
        Fill in the row totals.
        row_index - an int, the starting row index.
        '''
        col = 'N'
        rows = range(row_index, row_index + 6)

        for row in rows:   
            self._cell(row, col).Formula = '=sum(B%s:M%s)' % (row, row)
            self._cell(row, col).Style = 'currency'



    def _fill_date_range(self, row_index, end_col='M'):
        '''
        Fill in the date range for this row of receipts.
        row_index - an int, the starting row index.
        '''
        startdate = int(self._cell(row_index, 'B').Value[4:6])
        enddate = int(self._cell(row_index, end_col).Value[4:6])
        range = '%s %s-%s' % (self.month, startdate, enddate) 
        self._cell(row_index, 'A').Value = range       



    def _format_rows(self, row_index):
        '''
        Format the rows.
        row_index - an int, the starting row index.
        '''      
        self._cells(row_index, '', row_index, '').Font.Bold = True
        self._cells(row_index, '', row_index, '').Font.Underline = True

        # Underline the values above the totals.
        self._cells(row_index+5, 'A', row_index+5, 'M').Font.Underline = True

        # Align the invoice numbers; -4108 means align center        
        self._cells(row_index, 'B', row_index, 'N').HorizontalAlignment = -4108



    def _fill_monthly_totals(self, row_index):
        '''
        Fill in the monthly totals for the montly report.
        row_index - an int, the starting row index.
        '''       
        self._cells(row_index, '', row_index, '').Font.Bold = True
        self._cells(row_index, '', row_index, '').Font.Underline = True

        labels = ('SUB',
                  '10% FEE',
                  'BAR 2%',
                  'GST 7%',
                  'PST 8%',
                  'TOTAL')
        columns1 = COLUMNS[COLUMNS.index('B'):COLUMNS.index('M'):2]
        
        self._cell(row_index, 'A').Value = 'MONTH TOTAL:'

        for col, label in zip(columns1, labels):
            self._cell(row_index, col).Value = label
            self._cell(row_index, col).HorizontalAlignment = -4108


        # Starts at C(3), jump 2, ends after M (which is N(14))
        columns2 = COLUMNS[COLUMNS.index('C'):COLUMNS.index('N'):2]

        for col, i in zip(columns2, range(8, 2, -1)):            
            formula = '=%s' % '+'.join(
                ['N%s' % n for n in range(row_index-i, 0, -8)])
            self._cell(row_index, col).Formula = formula
            self._cell(row_index, col).Style = 'currency'
            self._cell(row_index, col).Font.Underline = False



    def create(self, workbooks):
        '''
        Create the report by summing over the receipts and writing
        to a new Excel file.  Note that the excel file is not saved
        after the writing.  Call write() to save it.

        workbooks - a list of Workbook instance.        
        '''
        try:
            self._wbObj = self.app.Workbooks.Add()
            self._sheetObj = self._wbObj.ActiveSheet

            # We starts at column B; 0 means A here, but
            # it will be incremented in the loop.
            col_index = 0

            # We stops at column M.       
            col_end_index = COLUMNS.index('M')

            row_index = 1 # we starts at row 1
            self._fill_row_labels(row_index+1)
                
            for workbook in workbooks:
                for worksheet in workbook:
                    for receipt in worksheet:
                        
                        if col_index < col_end_index:              
                            # Move to next column of the summary for
                            # the next receipt.
                            col_index = col_index + 1 
                        else:
                            # Calculate row totals.
                            self._fill_row_totals(row_index+1)
                            
                            # Fill date range for this row of receipts.
                            self._fill_date_range(row_index)

                            # Format the rows (underline, bold...etc)
                            self._format_rows(row_index)
                
                            # We have reached column M, let's move back
                            # to the start (column B) and move to the
                            # next set of rows.             
                            col_index = 1
                            row_index = row_index + 8

                            # Fill row labels.
                            self._fill_row_labels(row_index+1)

                        col = COLUMNS[col_index]
                        
                        # +7 because it stops before row+7
                        rows = range(row_index, row_index + 7)
                        amounts = (receipt.invoice_id,
                                   receipt.sub,
                                   receipt.ser,
                                   receipt.bar,
                                   receipt.gst,
                                   receipt.pst,
                                   receipt.tot)
                        
                        for row, amount in zip(rows, amounts):
                            self._cell(row, col).Value = amount

                            if row != row_index:
                                # The current row is not the first row,
                                # which means it is an amount (not the
                                # invoice_id), therefore we sum it and
                                # set it to currency style.
                                #self._set_cell(row, col, 'NumberFormat',
                                #'Currency')
                                self._cell(row, col).Style = 'currency'


            # For the last rows of receipts, we do these.
            self._fill_row_totals(row_index+1)

            # col comes from the last receipt we worked on.
            self._fill_date_range(row_index, end_col=col) 
            self._format_rows(row_index)
                        
            # Fill the monthly totals.
            self._fill_monthly_totals(row_index+9)

            # Final formatting bits.
            self._cell(1, 'N').Value = 'WEEK TOTAL'
            self._sheetObj.Cells.Font.Name = 'Arial'
            self._sheetObj.Cells.Font.Size = 8
            self._sheetObj.Cells.ColumnWidth = 8
            
            self._cells('', 'N', '', 'N').ColumnWidth = 9.13
            self._cells('', 'A', '', 'A').ColumnWidth = 12.29
            self._cells('', 'A', '', 'A').Font.Bold = True
            self._cells('', 'A', '', 'A').Font.Underline = True
            

            # Page setup for printing.
            # Set the left and right margin to 0.5 inches.
            self._sheetObj.PageSetup.LeftMargin = \
                                self.app.InchesToPoints(0.5)
            self._sheetObj.PageSetup.RightMargin = \
                                self.app.InchesToPoints(0.5)
            # 1 is Portrait, 2 is Landscape
            self._sheetObj.PageSetup.Orientation = 2 
            self._sheetObj.PageSetup.CenterHeader = \
                                REPORT_TITLE % (self.month, self.year)
            self._sheetObj.PageSetup.CenterFooter = "&F"

        except:
            self._wbObj.Close(False)
            raise



    def write(self, path):
        '''
        Write out the report to a Excel file.

        path - a string of the path to the excel file.
        '''
        try:
            self._wbObj.SaveAs(path)
        finally:
            # False here means not saving any changes.  Note that
            # if everything is ok up to this point, any changes
            # would have already been saved.
            self._wbObj.Close(False)

