# -*- coding: utf-8 -*-
from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_random_response
import logging
import urllib
import sys
import sqlite3

# Só corre em Python 3.4
# -------------------------- Chatterbot Domain --------------------------------------------

logging.basicConfig(level=logging.INFO)

bot = ChatBot(
    'Helper',
    response_selection_method=get_random_response,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
	{
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.45,
            'default_response': 'I am sorry, but I do not understand.'
        },
	# o import nao está a ir ao sitio certo
	{
	    'import_path': 'calender_adapter.CalenderLogicAdapter'
	},
	'chatterbot.logic.TimeLogicAdapter',	
    ],
    database='./database.sqlite3'
)

bot.set_trainer(ChatterBotCorpusTrainer)

bot.train(
    "chatterbot.corpus.english.greetings",
    #"chatterbot.corpus.english.conversations",
    #"chatterbot.corpus.english.emotion",
    #"chatterbot.corpus.english.gossip",
    #"chatterbot.corpus.english.humor",
    #"chatterbot.corpus.english.psychology",
    #"chatterbot.corpus.english.trivia",
)


NoneType = type(None)
conn = sqlite3.connect('database.sqlite3.db')
c = conn.cursor()
#------------------------- iCalc Parser Domain ----------------------------------

user = raw_input("Hello Mr/Miss?")
c.execute('SELECT * FROM UsersTable WHERE Name=?', (user,))
loggeduser = c.fetchone()

#print(loggeduser)

if(isinstance(loggeduser, NoneType)):
	c.execute('INSERT INTO UsersTable VALUES (NULL,?)', (user,))
	url = raw_input("Enter iCalender link: ")

	#urllib.request.urlretrieve(url, "test.ics")
	testfile = urllib.URLopener()
	testfile.retrieve(url, 'test.ics')

	summarylist = []
	dstartlist = []
	dtendlist = []
	dtstamplist = []
	descriptionlist = []
	userlist = []
 
	ncontrol = 0

	g = open("test.ics",'rb')
	gcal = Calendar.from_ical(g.read())
	for component in gcal.walk():
		if component.name == "VEVENT":
			#----------------------------Guardar na BD em vez de lista ----------------------------
			print('EVENT PROCESSING')
			summarylist.append(component.get('summary'))	
			print(component.get('summary'))
			dstartlist.append(component.get('dtstart').dt)
			print(component.get('dtstart').dt)
			if(isinstance(component.get('dtend'), NoneType)):
				print("None")
				dtendlist.append("None")
			else:
				dtendlist.append(component.get('dtend').dt)
				print(component.get('dtend').dt)
			dtstamplist.append(component.get('dtstamp').dt)		
			print(component.get('dtstamp').dt)
			descriptionlist.append(component.get('description'))
			print(component.get('description'))
			userlist.append(user)
			print("END EVENT PROCESSING")
			ncontrol += 1
	g.close()
	
	#print(ncontrol)

	infotuple = zip(userlist,summarylist,dstartlist,dtendlist,descriptionlist)	
	c.executemany('INSERT INTO EventsTable VALUES (NULL,?,?,?,?,?)', infotuple)

	#print(infotuple)
	conn.commit()

else:
	print('Hello ' +user) 
# -------------------------- Chatterbot Domain --------------------------------------------
print("WELCOME TO YOUR PERSONAL HELPER PLEASE SAY HI TO HIM")

while True:
    try:
     bot_input = bot.get_response(None)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break




