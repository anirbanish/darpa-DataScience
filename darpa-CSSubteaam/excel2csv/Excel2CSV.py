#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd
import csv
import sys

def Excel2CSV(excel_filename, sheet_name, csv_filename):
	try:
		excel_workbook = xlrd.open_workbook(excel_filename)
	except Exception:
		print("Could not open Excel file")
		sys.exit()

	try:
		excel_worksheet = excel_workbook.sheet_by_name(sheet_name)
	except Exception:
		print("Could not open " + sheet_name + " in Excel file")
		sys.exit()

	new_csvfile = open(csv_filename, 'wb')
	wr = csv.writer(new_csvfile, quoting=csv.QUOTE_ALL)

	for row_n in xrange(excel_worksheet.nrows):
		wr.writerow(list(x.encode('utf-8') if type(x) == type(u'') 
			else x for x in excel_worksheet.row_values(row_n)))
	new_csvfile.close()



if __name__ == "__main__":

	if len(sys.argv) != 3:
		print("Usage: python Excel2CSV.py <Excel_filename.xls> <CSV_filename.csv>")
		print("       python Excel2CSV.py <Excel_filename.xlsx> <CSV_filename.csv>")
		sys.exit()

	if ((sys.argv[1][-4:].lower() != ".xls") and (sys.argv[1][-5:].lower() != ".xlsx")):
		print("Excel filename must end with either \".xls\" or \".xlsx\"")
		sys.exit()

	if sys.argv[2][-4:].lower() != ".csv":
		print("CSV Filename must end with \".csv\"")
		sys.exit()

	sheetname = "Sheet1"
	if(sys.argv[1][-4:].lower() == ".xls"):
		sheetname = "Sheet 1"

	Excel2CSV( sys.argv[1], sheetname, sys.argv[2] )
	print("Process complete.")
