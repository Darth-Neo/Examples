import xlrd

def getXLSText(fileXLS):
    text_runs = []
    workbook = xlrd.open_workbook(fileXLS)

    sheet = "Specific Requirements"
    worksheet = workbook.sheet_by_name(sheet)

    CellTypes = ["Empty", "Text", "Number", "Date", "Boolean", "Error", "Blank"]

    for worksheet_name in workbook.sheet_names():
        worksheet = workbook.sheet_by_name(worksheet_name)
        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1
        curr_row = -1

        while curr_row < num_rows:
            curr_row += 1
            row = worksheet.row(curr_row)
            print 'Row:', curr_row
            curr_cell = -1
            while curr_cell < num_cells:
                curr_cell += 1
                # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                
                cell_type = worksheet.cell_type(curr_row, curr_cell)
                cell_value = worksheet.cell_value(curr_row, curr_cell)
                if cell_type == 1:
                    text_runs += cell_value
                    print '  ', cell_value

    return text_runs

if __name__ == "__main__":
    fileXLS = "C:\\Users\\morrj140\\Dev\\GitRepository\\DirCrawler\\PMS_Use CaseList_RequirementList V2.xlsx"
    getXLSText(fileXLS)
