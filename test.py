import discord
import os
from keep_alive import keep_alive
from discord.ext import tasks
import time
from datetime import datetime
from pytz import timezone
from PIL import Image
import pytesseract






#function helper to format an epoch timestamp to a gicen timezone and format
def format_timestamp(timestamp, timezone, format):
  time = datetime.fromtimestamp(timestamp, tz=timezone).strftime(format)
  return time


my_time = int(time.time())
#timezones from pytz module
CET_tz = timezone('Europe/Amsterdam')
pacific_tz = timezone('US/Pacific')
central_tz = timezone('US/Central')
AEST_tz = timezone ('Australia/Sydney')
utc_tz = timezone('UTC')
#the format of the output date I instead of H for 12H format, M minutes and p for AM or PM, %a is abreviated weekdsy name, %b month and %d the date value
datetime_format = '%H: %M %Z | %a %b %d'

cet_clock = format_timestamp(my_time, CET_tz, datetime_format)

pacific_clock = format_timestamp(my_time, pacific_tz, datetime_format)


central_clock = format_timestamp(my_time, central_tz, datetime_format)

aest_clock = format_timestamp(my_time, AEST_tz, datetime_format)

utc_clock = format_timestamp(my_time, utc_tz, datetime_format)

#we want to get the day, month and year from current time
day= datetime.fromtimestamp(my_time).day
month= datetime.fromtimestamp(my_time).month
year= datetime.fromtimestamp(my_time).year

#get the timestamp for each of ursus timeslots ( +1 to +5) (+18 to +22)
ursus_start1_epoch=int(datetime(year,month,day,1,0,0).timestamp())
ursus_end1_epoch=int(datetime(year,month,day,5,0,0).timestamp())
ursus_start2_epoch=int(datetime(year,month,day,18,0,0).timestamp())
ursus_end2_epoch=int(datetime(year,month,day,22,0,0).timestamp())



def print_test():

  print(pytesseract.image_to_string('image1.jpg'))
 # print('>>>>')
  #print(ursus_start1_epoch)
  #print(str(month) + '\n')
 # print(datetime.fromtimestamp(my_time).month)
  #print(str(get_date_epoch) + '\n')
  #print(datetime.fromtimestamp(get_date_epoch).strftime(datetime_format)+ '\n')