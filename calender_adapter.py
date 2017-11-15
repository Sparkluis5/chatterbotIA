# -*- coding: utf-8 -*-
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from datetime import datetime
from pytz import UTC
import sqlite3
import datetime
import logging
conn = sqlite3.connect('database.sqlite3.db')
c = conn.cursor()

class CalenderLogicAdapter(LogicAdapter):
	def __init__(self,**kwargs):
		self.logger = kwargs.get('logger', logging.getLogger(__name__))
		self.questions = ["what","where","when","who"]
		self.types = ['classes','class', 'delivery','deliveries', 'practical', 'theoretical', 'defenses', 'defense', 'evaluation','evaluations', 'exams', 'exams' ]
		self.frames = ['today', 'tomorrow', "yesterday"]
		super(CalenderLogicAdapter, self).__init__(**kwargs)

	def can_process(self, statement): 
    		if (x in statement.text.split() for x in self.types):
        		return True
    		else:
        		return False

	def process(self, statement): #introduzir logica de trantamento de informação
		ns = statement.text.split()
		ns = [x.lower() for x in ns]

		qa=[]
		ta=[]
		fa=[]
		for q in self.questions:
			if (q in ns):
				qa.append(q)
		for t in self.types:
			if (t in ns):
				ta.append(t)
		for f in self.frames:
			if (f in ns):
				fa.append(f)

		self.logger.info("-------------------------------------~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
		self.logger.info(ns) 
		self.logger.info("-------------------------------------~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
		self.logger.info(qa) 
		self.logger.info("-------------------------------------~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
		self.logger.info(ta) 
		self.logger.info("-------------------------------------~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
		self.logger.info(fa) 
		self.logger.info("-------------------------------------~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 

		if "what" in qa:
			if "class" in ta or "classes" in ta:
				if "today" in fa:
					events = self.make_statement_from_select(self.get_today_classes(),3)
					stm = "Today you have "+events
					response = Statement(stm)
					response.confidence = 1
					return response
		
		
		response = Statement("nothing here")
		response.confidence = 0
		return response





		




	#depth of the information 1=just class      2=  class +time     3 = class +time + soemthign else
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
		#self.logger.info("-------------------------------------~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
		#self.logger.info("hjdkjshdkjh") 
		#self.logger.info("-------------------------------------~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
		return form_string

	def get_today_classes(self):
		i = datetime.datetime.now()
		j = datetime.datetime.now() + datetime.timedelta(days=1)
		c.execute('SELECT * FROM EventsTable WHERE StartDate >= date(?) AND StartDate < date(?)', (i,j))
		eventfetch = c.fetchall()
		return eventfetch

	#def get_specific_classes(self, parameter):	
