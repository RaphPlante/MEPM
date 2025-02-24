import win32com.client

def xl_xlsfinfo(file_name):
    """
    xl_xlsfinfo
    Description: Finds all the sheets in the Excel file (.xls, .xlsm, .xlsx)
    
    Inputs:
        file_name: File name with path included.
    
    Outputs:
        Sheets_Names: List containing the sheet names along with their indices.
                      Each element in the list is a tuple (index, name).
    
    Author: Pruthvi Raj G
    Version: Version 1.0 - 2011b Compatible
    Date: 11-Feb-2020
    """
    # Create an instance of the Excel Application
    Excel = win32com.client.Dispatch("Excel.Application")
    
    # Open the Excel file
    workbook = Excel.Workbooks.Open(file_name)
    
    # Get the worksheets
    worksheets = workbook.Worksheets
    
    # Initialize a list to store sheet names and indices
    Sheets_Names = []
    
    # Loop through each worksheet
    for i in range(1, worksheets.Count + 1):
        sheet = worksheets.Item(i)
        Sheets_Names.append((i, sheet.Name))
    
    # Close Excel workbook
    workbook.Close()
    
    # Quit Excel Application
    Excel.Quit()
    
    # Release the Excel Application object
    del Excel
    
    return Sheets_Names
