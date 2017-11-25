# -*- coding: utf-8 -*-
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from datetime import datetime
from dateutil.parser import parse
from pytz import UTC
from nltk.tokenize import sent_tokenize, word_tokenize
import sqlite3
import datetime
import nltk
conn = sqlite3.connect('database.sqlite3.db')
c = conn.cursor()

class CalenderLogicAdapter(LogicAdapter):
	def __init__(self,**kwargs):
		super(CalenderLogicAdapter, self).__init__(**kwargs)

	def can_process(self, statement):
		return True
    		#words = ['what', 'classes', 'today'] #[today,exams,...]
    		#if all(x in statement.text.split() for x in words):
        		#return True
    		#else:
        		#return False

	def process(self, statement): #introduzir logica de trantamento de informação
		#if(exams in statement) -> get_exams()
		fields = ['classes','deliverables','practicals','theoreticals','defense','evaluation','exam']
		temporals = ['today','tomorrow']
		field = []
		temporal = []

		statetokens = word_tokenize(str(statement))
		#taggedtokens = nltk.pos_tag(words)

		for token in statetokens:
			if(token in fields):
				field.append(token)
			if(token in temporals):
				temporal.append(token)
			if(self.is_date(token)):
				dateparse = parse(token)
				temporal.append(token)

		
		print(str(len(field)) +'\n'+ str(len(temporal)))
		if((len(field) > 1) or (len(temporal) > 1)):
			#parse the fie
			print('too big')
		else:
			if('classes' in field):
				if('today' in temporal):
					i = datetime.datetime.now()
					fetchedevents = self.get_specifictime_classes(i)
					statem = 'This are the classes you have today:'+'\n'.join(str(v) for v in fetchedevents)
					response = Statement(statem)
					response.confidence = 1
        				return response
				if('tomorrow' in temporal):
					i = datetime.datetime.now() + datetime.timedelta(days=1)
					fetchedevents = self.get_specifictime_classes(i)
					statem = 'This are the classes you have tomorrow:'+'\n'.join(str(v) for v in fetchedevents)
					response = Statement(statem)
					response.confidence = 1
        				return response
				else:
					dateformated = ''.join(temporal)
					datefind = parse(dateformated)
					fetchedevents = self.get_specifictime_classes(datefind)
					statem = 'This are the classes you have in ' + dateformated + ':'+'\n'.join(str(v) for v in fetchedevents)
					response = Statement(statem)
					response.confidence = 1
        				return response				

			if(field == 'deliverables'):
				fetchedevents = self.get_specific_classes(field,temporal)
			if(field == 'practical'):
				fetchedevents = self.get_specific_classes(field,temporal)
			if(field == 'theoretical'):
				fetchedevents = self.get_specific_classes(field,temporal)
			if(field == 'defense'):
				fetchedevents = self.get_specific_classes(field,temporal)
			if(field == 'evaluation'):
				fetchedevents = self.get_specific_classes(field,temporal)
			if(field == 'exam'): 
				fetchedevents = self.get_specific_classes(field,temporal)


	def get_today_classes(self):
		i = datetime.datetime.now()
		j = datetime.datetime.now() + datetime.timedelta(days=2)
		c.execute('SELECT * FROM EventsTable WHERE StartDate >= date(?) AND StartDate < date(?)', (i,j))
		eventfetch = c.fetchall()

		return eventfetch

	def get_specifictime_classes(self,date):
		i = date
		j = date + datetime.timedelta(days=1)
		c.execute('SELECT * FROM EventsTable WHERE StartDate >= date(?) AND StartDate < date(?)', (i,j))
		eventfetch = c.fetchall()

		return eventfetch


	def get_specific_classes(self, parameter,date):
		if(date == 'today'):
			i = datetime.datetime.now()
		if(date == 'tomorrow'):
			i = datetime.datetime.now() + datetime.timedelta(days=1)
		else:
			i = parse(date)
			
		j = i + datetime.timedelta(days=1)
		c.execute("SELECT * FROM EventsTable WHERE StartDate >= date(?) AND StartDate < date(?) AND Parameter LIKE ?", (i,j,'%'+parameter+'%'))
		eventfetch = c.fetchall()

		return eventfetch

	def is_date(self,string):
    		try: 
        		parse(string)
        		return True
    		except ValueError:
        		return False	

