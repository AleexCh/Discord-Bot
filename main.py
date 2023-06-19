import discord
import os
from keep_alive import keep_alive
from discord.ext import tasks
import time, pytz
from datetime import datetime, timedelta
from pytz import timezone
import operator

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)
#discord bot token is saved as a secrete token in replit.
my_secret = os.environ['TOKEN']

#get the time in epoch and transform to an int to use
my_time = int(time.time())


#"""
#function helper to format an epoch timestamp to a gicen timezone and format
def format_timestamp(timestamp, timezone, format):
  time = datetime.fromtimestamp(timestamp, tz=timezone).strftime(format)
  return time


ops = {'+': operator.add, '-': operator.sub}


#helper function to calculate new times for time command
#using operator module, it does the operation given the string for the operator it receives
def calculate_time(time1, operator, time2):
  new_time = ops[operator](time1, time2)
  return new_time


#updating voice channel name task, it loops every x minutes
@tasks.loop(minutes=15)
async def update_clocks():
  #timezones from pytz module
  CET_tz = timezone('Europe/Amsterdam')
  pacific_tz = timezone('US/Pacific')
  AEST_tz = timezone('Australia/Sydney')
  utc_tz = timezone('UTC')

  #the format of the output date H for Hours, M minutes, %Z tondisplay timezone, %a is abreviated weekdsy     name, %b month and %d the date value
  datetime_format = '%H:%M %Z | %a %b %d'

  #Defining the different clocks timezones we want to manage
  cet_clock = format_timestamp(my_time, CET_tz, datetime_format)

  pacific_clock = format_timestamp(my_time, pacific_tz, datetime_format)

  aest_clock = format_timestamp(my_time, AEST_tz, datetime_format)

  utc_clock = format_timestamp(my_time, utc_tz, datetime_format)

  guild_id = int(os.environ['GUILD_ID'])
  voice_channel_1 = int(os.environ['VOICE_CHANNEL_1_ID'])
  voice_channel_2 = int(os.environ['VOICE_CHANNEL_2_ID'])
  voice_channel_3 = int(os.environ['VOICE_CHANNEL_3_ID'])
  voice_channel_4 = int(os.environ['VOICE_CHANNEL_4_ID'])
  #API call to update each channel with the respective clock time format . For the momment it is hard coded, meaning we need to create the channels before hand and save their ids as secrets in replit
  await client.get_guild(guild_id).get_channel(voice_channel_1).edit(
    name=utc_clock)
  await client.get_guild(guild_id).get_channel(voice_channel_2).edit(
    name=pacific_clock)
  await client.get_guild(guild_id).get_channel(voice_channel_3).edit(
    name=aest_clock)
  await client.get_guild(guild_id).get_channel(voice_channel_4).edit(
    name=cet_clock)

  print("Clocks updated!")


@client.event
async def on_ready():
  update_clocks.start()
  print("logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  #if message is from bot, ignore
  if (message.author == client):
    return

  #respond only if using the prefix ~
  if message.content.startswith('~'):
    #we split the message from the prefix to get the command the user is trying to run
    command = message.content.split(
      '~', 1)[1].lower()  #to make command not case sensitive.
    #command to get ursus times
    if (command == 'ursus'):
      #we want to get the day, month and year from current time
      day = datetime.fromtimestamp(my_time).day
      month = datetime.fromtimestamp(my_time).month
      year = datetime.fromtimestamp(my_time).year

      #get the timestamp for each of ursus timeslots for the day ( +1 to +5) (+18 to +22)
      ursus_start1_epoch = int(datetime(year, month, day, 1, 0, 0).timestamp())
      ursus_end1_epoch = int(datetime(year, month, day, 5, 0, 0).timestamp())
      ursus_start2_epoch = int(
        datetime(year, month, day, 18, 0, 0).timestamp())
      ursus_end2_epoch = int(datetime(year, month, day, 22, 0, 0).timestamp())

      #if my current time is between ursus FIRST run time then
      if (ursus_start1_epoch < my_time < ursus_end1_epoch):
        time_difference = ursus_end1_epoch - my_time
        response = 'Ursus 2x meso is active between <t:' + str(
          ursus_start1_epoch
        ) + ':t> and <t:' + str(ursus_end1_epoch) + ':t> and between <t:' + str(
          ursus_start2_epoch) + ':t> and <t:' + str(
            ursus_end2_epoch
          ) + ':t> \nUrsus 2x meso is currently active, it will end in ' + str(
            timedelta(seconds=time_difference))
        #we will be sending embeds for aesthetic purposes.
        embed = discord.Embed(description=response,
                              colour=discord.Colour.purple())
        await message.channel.send(embed=embed)

      #else if my current time is between SECOND ursus run time
      elif (ursus_start2_epoch < my_time < ursus_end2_epoch):
        time_difference = ursus_end2_epoch - my_time
        response = 'Ursus 2x meso is active between <t:' + str(
          ursus_start1_epoch
        ) + ':t> and <t:' + str(ursus_end1_epoch) + ':t> and between <t:' + str(
          ursus_start2_epoch) + ':t> and <t:' + str(
            ursus_end2_epoch
          ) + ':t> \nUrsus 2x meso is currently active, it will end in ' + str(
            timedelta(seconds=time_difference))
        embed = discord.Embed(description=response,
                              colour=discord.Colour.purple())
        await message.channel.send(embed=embed)

      #if my current time is lower than ursus run time means we are earlier
      elif (ursus_start1_epoch > my_time):
        time_difference = ursus_start1_epoch - my_time
        response = 'Ursus 2x meso is active between <t:' + str(
          ursus_start1_epoch) + ':t> and <t:' + str(
            ursus_end1_epoch) + ':t> and between <t:' + str(
              ursus_start2_epoch) + ':t> and <t:' + str(
                ursus_end2_epoch
              ) + ':t> \nUrsus 2x meso is not active, it will start in ' + str(
                timedelta(seconds=time_difference))
        embed = discord.Embed(description=response,
                              colour=discord.Colour.purple())
        await message.channel.send(embed=embed)

      #if we are past first ursus run time but still lower than the SECOND run time start
      elif (ursus_end1_epoch < my_time < ursus_start2_epoch):
        time_difference = ursus_start2_epoch - my_time
        response = 'Ursus 2x meso is active between <t:' + str(
          ursus_start1_epoch) + ':t> and <t:' + str(
            ursus_end1_epoch) + ':t> and between <t:' + str(
              ursus_start2_epoch) + ':t> and <t:' + str(
                ursus_end2_epoch
              ) + ':t> \nUrsus 2x meso is not active, it will start in ' + str(
                timedelta(seconds=time_difference))
        embed = discord.Embed(description=response,
                              colour=discord.Colour.purple())
        await message.channel.send(embed=embed)

    #command to get server time
    if (command == 'servertime'):
      UTC_time = datetime.fromtimestamp(my_time).strftime('%H:%M %p')
      response = 'The server time right now is: ' + UTC_time + ' \n > Maplestory GMS uses UTC as default server time'
      embed = discord.Embed(description=response,
                            colour=discord.Colour.purple())
      await message.channel.send(embed=embed)

    #command to get the local time compared to server reset time
    if command.startswith('time'):
      splitted_comand = command.split('time')
      #if there is nothing after time
      if not splitted_comand[1]:
        response = 'Your time right now is: <t:' + str(my_time) + ':t>'
        embed = discord.Embed(description=response,
                              colour=discord.Colour.purple())
        await message.channel.send(embed=embed)

      #there is something after time. we want to calculate whats the timestamp in relation to reset time (00:00 UTC). example: If user looks for time +1 it will show their local time when it is 00+1 UTC. If user local time is EST, it will show 9 PM
      else:
        #split by the space and not take it into consideration
        parameter = splitted_comand[1].split(' ')

        #we want to get the day, month and year from current time
        day = datetime.fromtimestamp(my_time).day
        month = datetime.fromtimestamp(my_time).month
        year = datetime.fromtimestamp(my_time).year

        #server reset is at 00:00 UTC
        server_reset_time = int(
          datetime(year, month, day, 0, 0, 0).timestamp())

        #this returns the operator + the number(s) , +1, -1 etc
        op_and_number = parameter[1]
        #this returns only the operator + or -
        operator = op_and_number[0]
        #if lenght is less than 2 is a single digit operation +1 -1, etc
        if len(op_and_number) <= 2:
          new_time = calculate_time(server_reset_time, operator,
                                    int(op_and_number[1]) * 3600)
        #else is a 2 digits operation +10, -10, etc
        elif 2 < len(op_and_number) <= 3:
          new_time = calculate_time(
            server_reset_time, operator,
            int(op_and_number[1] + op_and_number[2]) * 3600)
        #user tried to add or substract a 3 digit hour, error
        else:
          response = " Number range exceeded. Try again with a smaller number"
          embed = discord.Embed(title="Error",
                                description=response,
                                colour=discord.Colour.purple())
          await message.channel.send(embed=embed)
          return

        response = op_and_number + ' is: <t:' + str(new_time) + ':t>'
        embed = discord.Embed(title="Time Converter",
                              description=response,
                              colour=discord.Colour.purple())
        await message.channel.send(embed=embed)

    #command to roll


#this calls the web server which uptimerobot will be calling every x minutes.
keep_alive()
client.run(my_secret)
