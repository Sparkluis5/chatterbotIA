# chatterbotIA

chatterbotIA is a Chatbot developed for the course of Artificial Inteligence.
The Chatbot was developed in order to awnser to several questions related to Calender appointments, where it accepts a format of iCal.
Currently is only focused to the context of the students scheduale of the University of Coimbra - Portugal 2017.

chatterbotIA:
    botandparser.py - Responsible for chatbot initialization and training using chatterbot module and DB creation and population
    calender_adapter.py - Module of chatbot for response generation based on DB information about future and past events
    langtest.py - Additional functions for name and surname recongnition
    database.sqlite3.db - DB for information storage and retrieval
    
Additional Notes:
chatterbotIA was developed on a academic purpose and much of the approaches used are not correct. We didn't performed a good NLP approach and
data processing and SQL DB was probably not necessary. Also there are more powerfull techniques like sentence similarity that we could have
used for better results.

Developed by:
    Luis Duarte
    Diogo Miguel
    
Coimbra 2017
    

