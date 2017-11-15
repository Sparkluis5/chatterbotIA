# -*- coding: utf-8 -*-
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from datetime import datetime
from pytz import UTC
import sqlite3
import datetime
conn = sqlite3.connect('database.sqlite3.db')
c = conn.cursor()

class CalenderLogicAdapter(LogicAdapter):
	def __init__(self,**kwargs):
		super(CalenderLogicAdapter, self).__init__(**kwargs)

	def can_process(self, statement):
    		words = ['what', 'classes', 'today']  # 'deliverables', 'practical', 'theoretical', 'defense', 'evaluation', 'exam', 'registered'  
    		if all(x in statement.text.split() for x in words):
        		return True
    		else:
        		return False

	def process(self, statement): #introduzir logica de trantamento de informação
		fetchedevents = self.get_today_classes()
		statem = 'This are the classes you have today:'+'\n'.join(str(v) for v in fetchedevents)

		response = Statement(statem)
		response.confidence = 1
        	return response

	def get_today_classes(self):
		i = datetime.datetime.now()
		j = datetime.datetime.now() + datetime.timedelta(days=1)
		c.execute('SELECT * FROM EventsTable WHERE StartDate >= date(?) AND StartDate < date(?)', (i,j))
		eventfetch = c.fetchall()

		return eventfetch

	#def get_specific_classes(self, parameter):	
