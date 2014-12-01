Introduction
============

CRONS:
If you need to setup up a CRON for updating a Cache object, this is a 
simple and safe way to achieve this.

I prefer using CronTab on the server since it is editable and doesn't 
require server restart.  Crons in Zope can require you to restart your
server.

Run down on how to do a Once-A-Day cron update:
1. Make a python (Script)
2. Set Proxy Role to allow acceess to a Cache Object (Don't worry).
3. Target your caches.
4. Check the cacheObject.lastUpdate() and compare the day to now().
5. If it is less than today's date run cache updates, otherwise do nothing.
6. Crontab with a wget http://www.domain.com/Plone/cache/pythonScript

Yes it is public but it is okay.  This is a very simple way to update 
a cache once a day. By checking against the last updated day is a simple 
way to prevent someone from a ddos on this update especially if
it is a expensive cache update.


Simple example of a python script:

>>> if context.portal_type != 'LibraryCache':
>>>     return ''
>>> 
>>> request = container.REQUEST
>>> response =  request.response
>>> from DateTime import DateTime
>>> 
>>> last_dt = DateTime(context.lastUpdate())
>>> 
>>> if last_dt.day() < DateTime().day():
>>>     #context.rebuildCache()
>>>     return "Running UPDATE"
>>> 
>>> return "NOT"