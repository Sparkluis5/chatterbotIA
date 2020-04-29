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
import sys
import unicodedata

# Available only for Python 3.4 and above
# -------------------------- Chatterbot Domain --------------------------------------------

#Logging for debug purpose
logging.basicConfig(level=logging.DEBUG)

#Chatterbor Bot creation, defining our SQL DB and connection to Logic Adapter script
bot = ChatBot(
    'Helper',
    response_selection_method=get_random_response,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
	{
	    'import_path': 'calender_adapter.CalenderLogicAdapter',
	    'threshold': 0.5
	},
	{
        'import_path': 'chatterbot.logic.LowConfidenceAdapter',
        'threshold': 0.5,
        'default_response': 'I am sorry, but I do not understand.'
    },
	{
        'import_path': 'chatterbot.logic.BestMatch'
    },
	'chatterbot.logic.TimeLogicAdapter',	
    ],
    database='./database.sqlite3'
)


#Training Bot
bot.set_trainer(ChatterBotCorpusTrainer)

bot.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations",
    "chatterbot.corpus.english.emotion",
    "chatterbot.corpus.english.gossip",
    "chatterbot.corpus.english.humor",
    "chatterbot.corpus.english.psychology",
    "chatterbot.corpus.english.trivia",
)

#SQL database connection
NoneType = type(None)
conn = sqlite3.connect('database.sqlite3.db')
c = conn.cursor()

#------------------------- iCalc Parser Domain ----------------------------------
#User recognition input, checks DB for existing user, if not creates a new one
user = raw_input("Hello Mr/Miss?")
c.execute('CREATE TABLE IF NOT EXISTS UsersTable (name,value)')
c.execute('SELECT * FROM UsersTable WHERE Name=?', (user,))
loggeduser = c.fetchone()

#New user needs iCalc link to update DB (Based on University of Coimbra platform Inforestudante calender link
if(isinstance(loggeduser, NoneType)):
	c.execute('INSERT INTO UsersTable VALUES (NULL,?)', (user,))
	url = raw_input("Enter iCalender link: ")

	#urllib.request.urlretrieve(url, "test.ics")
	testfile = urllib.URLopener()
	testfile.retrieve(url, 'test.ics')

	#Aux variables
	summarylist = []
	dstartlist = []
	dtendlist = []
	dtstamplist = []
	descriptionlist = []
	userlist = []
 
	ncontrol = 0

	#Parsing through the calender file for event extraction
	g = open("test.ics",'rb')
	gcal = Calendar.from_ical(g.read())
	for component in gcal.walk():
		if component.name == "VEVENT":
			#----------------------------Guardar na BD em vez de lista ----------------------------
			print('EVENT PROCESSING')
			summarylist.append(component.get('summary'))	
			dstartlist.append(component.get('dtstart').dt)
			if(isinstance(component.get('dtend'), NoneType)):
				dtendlist.append("None")
			else:
				dtendlist.append(component.get('dtend').dt)
			dtstamplist.append(component.get('dtstamp').dt)
			descriptionlist.append(unicodedata.normalize('NFD', component.get('description')).encode('ascii', 'ignore'))#adicionei tornar tudo em ascii
			userlist.append(user)
			print("END EVENT PROCESSING")
			ncontrol += 1
	g.close()
	print("Processing finished")
	
	#print(ncontrol)

	#Data insertion into SQL DB
	infotuple = zip(userlist,summarylist,dstartlist,dtendlist,descriptionlist)	
	c.execute('CREATE TABLE IF NOT EXISTS EventsTable (name,value1,value2,val3,val4,val5)')
	c.executemany('INSERT INTO EventsTable VALUES (NULL,?,?,?,?,?)', infotuple)

	conn.commit()

else:
	print('Hello ' +user) 
# -------------------------- Chatterbot Domain --------------------------------------------
#Bot interaction section
print("WELCOME TO YOUR PERSONAL HELPER PLEASE SAY HI TO HIM")

while True:
    try:
     	bot_input = bot.get_response(None)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break




