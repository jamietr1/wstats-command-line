#!/usr/bin/python 

import gspread
import sys, getopt
from datetime import date, timedelta

# By default, returns yesterday's writing stats
# words, goal, avg, consecutive days, total days

wdate = ''
output = ''
avg_flag = 0
con_days_flag = 0
goal_flag = 0
total_flag = 0
word_flag = 0


try:
	opts, args = getopt.getopt(sys.argv[1:], "acd:ghtw")
except getopt.GetoptError:
	print "wstats.py -a -c -d <date> -g -h -t -w"
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print "wstats.py -a -c -d <date> -g -h -t -w"
		sys.exit()
	elif opt in ('-d'):
		wdate = arg
	elif opt in ('-a'):
		avg_flag = 1
	elif opt in ('-c'):
		con_days_flag = 1
	elif opt in ('-g'):
		goal_flag = 1
	elif opt in ('-t'):
		total_flag = 1
	elif opt in ('-w'):
		word_flag = 1
if not wdate:
	wdate = date.today() - timedelta(days=1)
	wdate = wdate.strftime('%-m/%-d/%Y')

# Login with Google account
gc = gspread.login('jamietoddrubin@gmail.com', 'biwxydcgomnkyfsy')
sh = gc.open_by_key('0AmEvY6JjICyzdFM1aUVCd0hvZmxmT185MGE0R0hrdWc')

worksheet = sh.worksheet('Writing')
cell = worksheet.find(wdate)
dictWriting = worksheet.row_values(cell.row)
col_list = worksheet.col_values(1)

# Set values
totalDays = len(col_list) - 1
words = dictWriting[1]
try:
	goal = dictWriting[3]
except Exception:
	goal = "Unk"
	pass
	
writingDate = dictWriting[0]


# look for days with 0 words
record_sheet = sh.worksheet('Records')
consecutiveDays = record_sheet.acell('D3').value

try:
	mov_avg = int(float(dictWriting[2]))
except Exception:
	mov_avg = "Unk"
	pass

if avg_flag == 0 and con_days_flag == 0 and goal_flag == 0 and total_flag == 0 and word_flag == 0:
	print words, goal, mov_avg, consecutiveDays, totalDays, writingDate
elif word_flag == 1:
	print words
elif goal_flag == 1:
	print goal
elif avg_flag == 1:
	print mov_avg
elif con_days_flag == 1:
	print consecutiveDays
elif total_flag == 1:
	print totalDays

