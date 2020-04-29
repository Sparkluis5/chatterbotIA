# -*- coding: utf-8 -*-
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from datetime import datetime
from dateutil.parser import parse
from pytz import UTC
from nltk.tokenize import sent_tokenize, word_tokenize
from nameparser.parser import HumanName
import sqlite3
import datetime
import nltk

#Connection to Database for data retrieval
conn = sqlite3.connect('database.sqlite3.db')
c = conn.cursor()

#Calender Logic Adapter module, responsible for calender events responses
class CalenderLogicAdapter(LogicAdapter):
	def __init__(self,**kwargs):
		super(CalenderLogicAdapter, self).__init__(**kwargs)

	def can_process(self, statement):
		return True

	def process(self, statement):
		#Question process function
		statement = str(statement).lower()
		fields = ['classes','class','deliverables','practicals','theoreticals','defense','evaluation','exame','aula']
		temporals = ['today','tomorrow','next']
		field = []
		temporal = []
		statem = ''

		statetokens = word_tokenize(str(statement))
		names = self.get_human_names(str(statement))
		classes = self.get_classes_names(str(statement))

		#remove capitalizations
		for i in range(len(statetokens)):
			statetokens[i] = statetokens[i].lower()
		#Portuguese converter
		for token in statetokens:
			if(token in fields):
				if (token == 'classes' or token == 'class' or token == 'aula'):
					field.append('Aula')
				else:
					field.append(token)
			if(token in temporals):
				temporal.append(token)
			if(self.is_date(token)):
				dateparse = parse(token)
				temporal.append(token)

		print(field)
		print(temporal)

		if((len(field) == 0) or (len(temporal) == 0))   :
			response = Statement('Sorry didnt understand')
			response.confidence = 0
			return response

		for name in names:
			last_first = HumanName(name).first
			field.append(last_first)

		
		saved=[]
		k=0
		INFORMATIONGIVEN = 1
#-------------------------------------------------MultipleInputs----------------------------------------------------------------------------
		#Section for understanding if there are more than one intention
		#Based on a if else tree based on the detection of intents
		if((len(field) > 1) or (len(temporal) > 1)):
			if(('or' in statetokens) or ('and' in statetokens)):
				for i in range(0,len(field)):
					for j in range(0,len(temporal)):
						temporalsend = ''.join(temporal[j])
						fieldsend = ''.join(field[i])
						statem = statem + self.make_statement_from_select(self.get_specific_classes(fieldsend,temporalsend),INFORMATIONGIVEN)
				statem = 'You have:' + statem
				response = Statement(statem)
				response.confidence = 1
				return response
			elif(('with' in statetokens)):
				for i in range(0,len(field)):
					for j in range(0,len(temporal)):
						temporalsend = ''.join(temporal[j])
						fieldsend = ''.join(field[i])
						help = self.get_specific_classes(fieldsend,temporalsend)
						rets=[]
						if k==0:
							saved = help
							k=k+1
						else:
							for term in help:
								if (term in saved):
									rets.append(term)
				statem = 'You have:' + self.make_statement_from_select(rets,INFORMATIONGIVEN)
				response = Statement(statem)
				response.confidence = 1
				return response
			else:
				if(len(classes) > 0):
					for j in range(0,len(temporal)):
						for i in range(0,len(classes)):
							temporalsend = ''.join(temporal[j])
							fieldsend = ''.join(classes[i])
							fetchedevents = self.get_named_classes(fieldsend,temporalsend)
							statem = statem + self.statement_parsing(fetchedevents)
						
						response = Statement(statem)
						response.confidence = 1
						return response
				else:
					response = Statement('Im not understanding your question very much, please reformulate it')
					response.confidence = 0
					return response
#-------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------Single Inputs, need better modularization----------------------------------------------------
		else:
			#Informal decision tree creation
			if('Aula' in field):
				if('next' in temporal):
					statem = self.make_statement_from_select(self.get_next_classes(),INFORMATIONGIVEN)
					statem = 'Next, you have:' +statem
					response = Statement(statem)
					response.confidence = 1
					return response
				else:
					dateformated = ''.join(temporal)
					datefind = parse(dateformated)
					fetchedevents = self.get_specifictime_classes(datefind)
					statem = self.statement_parsing(fetchedevents)
					response = Statement(statem)
					response.confidence = 1
					return response             

			if('deliverables' in field):
				dateformated = ''.join(temporal)
				fetchedevents = self.get_specific_classes(field,dateformated)
				statem = statem + self.statement_parsing(fetchedevents)
				response = Statement(statem)
				response.confidence = 1
				return response 
			if('practical' in field):
				dateformated = ''.join(temporal)
				fetchedevents = self.get_specific_classes(field,dateformated)
				statem = statem + self.statement_parsing(fetchedevents)
				response = Statement(statem)
				response.confidence = 1
				return response 
			if('theoretical' in field):
				dateformated = ''.join(temporal)
				fetchedevents = self.get_specific_classes(field,dateformated)
				statem = statem + self.statement_parsing(fetchedevents)
				response = Statement(statem)
				response.confidence = 1
				return response 
			if('defense' in field):
				dateformated = ''.join(temporal)
				fetchedevents = self.get_specific_classes(field,dateformated)
				statem = statem + self.statement_parsing(fetchedevents)
				response = Statement(statem)
				response.confidence = 1
				return response 
			if('evaluation' in field):
				dateformated = ''.join(temporal)
				fetchedevents = self.get_specific_classes(field,dateformated)
				statem = statem + self.statement_parsing(fetchedevents)
				response = Statement(statem)
				response.confidence = 1
				return response 
			if('exame' in field): 
				dateformated = ''.join(temporal)
				fetchedevents = self.get_specific_classes(field,dateformated)
				statem = statem + self.statement_parsing(fetchedevents)
				response = Statement(statem)
				response.confidence = 1
				return response 

			response = Statement('Im dont understand very much, please reformulate the question friend')
			response.confidence = 0
			return response 

	#Aux functions for DB retrieval, name is indication of their purpose
	def get_today_classes(self):
		i = datetime.datetime.now()
		j = datetime.datetime.now() + datetime.timedelta(days=1)
		c.execute('SELECT * FROM EventsTable WHERE StartDate >= date(?) AND StartDate < date(?)', (i,j))
		eventfetch = c.fetchall()

		return eventfetch

	def get_next_classes(self):
		i = datetime.datetime.now()
		j = datetime.datetime.now() + datetime.timedelta(days=1)
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
		#print(date)
		dateformated = ''.join(date)
		#print(dateformated)
		parameterformated = ''.join(parameter)
		if(dateformated == 'today'):
			i = datetime.datetime.now()
		else:
			if(dateformated == 'tomorrow'):
				i = datetime.datetime.now() + datetime.timedelta(days=1)
			else:
				i = parse(dateformated)
			
		j = i + datetime.timedelta(days=1)
		c.execute("SELECT * FROM EventsTable WHERE StartDate >= date(?) AND StartDate < date(?) AND Description LIKE (?)", (i,j,'%'+parameterformated+'%'))
		eventfetch = c.fetchall()

		return eventfetch

	def get_named_classes(self, parameter,date):
		#print(date)
		dateformated = ''.join(date)
		#print(dateformated)
		parameterformated = ''.join(parameter)
		if(dateformated == 'today'):
			i = datetime.datetime.now()
		else:
			if(dateformated == 'tomorrow'):
				i = datetime.datetime.now() + datetime.timedelta(days=1)
			else:
				i = parse(dateformated)
			
		j = i + datetime.timedelta(days=1)
		c.execute("SELECT * FROM EventsTable WHERE StartDate >= date(?) AND StartDate < date(?) AND Summary LIKE (?)", (i,j,'%'+parameterformated+'%'))
		eventfetch = c.fetchall()

		return eventfetch

	def is_date(self,string):
			try: 
				parse(string)
				return True
			except ValueError:
				return False

	def get_human_names(self,text):
		tokens = nltk.tokenize.word_tokenize(text)
		pos = nltk.pos_tag(tokens)
		sentt = nltk.ne_chunk(pos, binary = False)
		person_list = []
		person = []
		name = ""
		for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
			for leaf in subtree.leaves():
					person.append(leaf[0])
			if len(person) > 1: #avoid grabbing lone surnames
					for part in person:
						name += part + ' '
					if name[:-1] not in person_list:
						person_list.append(name[:-1])
					name = ''
			person = []

		return (person_list)    

	def get_classes_names(self, text):
		classes_list = []
		sentence = nltk.word_tokenize(text)
		sent = nltk.pos_tag(sentence)
		for s in sent: 
			if(s[1] == 'NNP'):
				classes_list.append(s[0])
		return(classes_list)

	def statement_parsing(self, qresult):
		beg = 'This is what i got:'
		addst = ''
		if(len(qresult) == 0):
			addst = 'I wasnt able to find Anything'
			return addst
			
		for i in range(0,len(qresult)):
			addst = addst + '\n' + qresult[i][2] + '\nStartDate:' + qresult[i][3] + '\nEndDate:' + qresult[i][4] + '\n' + qresult[i][5]

		return beg + addst

	#Answer formulation function
	def make_statement_from_select(self,func,depth):
		fetchedevents = func
		form_string="\n"
		for event in fetchedevents:
			if (depth > 0):
				some = event[2].split(" - ")
				form_string += "\t"+some[0] + " of " + some[1] + " in room " + some[2]
				if (depth > 1):
					h = event[3].split(" ")
					h1 = event[4].split(" ")
					if (h[0]==h1[0]):
						form_string += " on "+h[0]+" from "+h[1].split("+")[0]+" to "+h1[1].split("+")[0]
					else:
						form_string += " starting on "+h[0]+" at "+h[1].split("+")[0] +" and ending on "+h1[0]+" at "+h1[1].split("+")[0]
					if (depth > 2):
						form_string+= "  additional info "
			form_string+= "\n"
		return form_string



