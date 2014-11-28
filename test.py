import pyttsx
import sys
#import requests

# proxies = {
#     "http": "http://s0teneau:afr5128mq@proxy.enib.fr",
#     "https": "http://s0teneau:afr5128mq@proxy.enib.fr",
# }

# r = requests.get('http://www.google.fr/', proxies=proxies)
# print r.headers, r.text
# print r

engine = pyttsx.init()


import lib.wikipedia as wikipedia
print "Starting wikipedia Part"
#print wikipedia.summary("Wikipedia")
# Wikipedia is a collaboratively edited, multilingual, free Internet encyclopedia supported by the non-profit Wikimedia Foundation...

#print wikipedia.search("Barack")
# [u'Barak (given name)', u'Barack Obama', u'Barack (brandy)', u'Presidency of Barack Obama', u'Family of Barack Obama', u'First inauguration of Barack Obama', u'Barack Obama presidential campaign, 2008', u'Barack Obama, Sr.', u'Barack Obama citizenship conspiracy theories', u'Presidential transition of Barack Obama']
wikipedia.set_lang("fr")
ny = wikipedia.page("New York")
text = ny.summary
print " READING \n\n" + text

#text ='Philosophy is the study of general and fundamental problems, such as those connected with reality, existence, knowledge, values, reason, mind, and language.Philosophy is distinguished from other ways of addressing such problems by its critical, generally systematic approach and its reliance on rational argument. In more casual speech, by extension, "philosophy" can refer to "the most basic beliefs, concepts, and attitudes of an individual or group"'

rate = engine.getProperty('rate')
print rate
engine.setProperty('rate', rate-75)

def onEnd(name, completed):
	print 'finishing', name, completed
	print engine.getProperty('voice')
	#engine.endLoop()

engine.connect('finished-utterance', onEnd)
voices = engine.getProperty('voices')
for i in range(len(voices)):
	print "number:" + str(i), " - voice : " +  voices[i].id

engine.setProperty('voice', voices[int(sys.argv[1])].id)
engine.say(text,"name")
#engine.say('Yoloyoloyoloyolo',"name")
engine.runAndWait()


#import lib.wikipedia as wikipedia
#print "Starting wikipedia Part"
#print wikipedia.summary("Wikipedia")
# Wikipedia is a collaboratively edited, multilingual, free Internet encyclopedia supported by the non-profit Wikimedia Foundation...

#print wikipedia.search("Barack")
# [u'Barak (given name)', u'Barack Obama', u'Barack (brandy)', u'Presidency of Barack Obama', u'Family of Barack Obama', u'First inauguration of Barack Obama', u'Barack Obama presidential campaign, 2008', u'Barack Obama, Sr.', u'Barack Obama citizenship conspiracy theories', u'Presidential transition of Barack Obama']

#ny = wikipedia.page("New York")
#print ny.summary

#print ny.title
# u'New York'
#print ny.url
# u'http://en.wikipedia.org/wiki/New_York'
#print ny.content
# u'New York is a state in the Northeastern region of the United States. New York is the 27th-most exten'...
#print ny.links[0]
# u'1790 United States Census'

#wikipedia.set_lang("fr")
#wikipedia.summary("Facebook", sentences=1)
