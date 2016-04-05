#!/usr/bin/python 
import unittest
import reader
import json
import datetime

class TestReader(unittest.TestCase):
	def test_parsehashtags(self):
		tweet1 = json.loads('{}')
		self.assertEqual(reader.parsehashtags(tweet1),[])

		tweet2 = json.loads('{"entities":{"hashtags":[{"text":"Pisteare","indices":[9,18]},{"text":"elsientometro","indices":[46,60]}]}}')
		self.assertEqual(reader.parsehashtags(tweet2),['Pisteare','elsientometro'])

	def test_parsetime(self):
		tweet1 = json.loads('{}')
		self.assertEqual(reader.parsetime(tweet1), None)

		tweet2 = json.loads('{"created_at":"Thu Nov 05 05:05:39 +1001 2015"}')
		print reader.parsetime(tweet2)
		self.assertEqual(reader.parsetime(tweet2),datetime.datetime(2015,11,5,15,06,39))

suite = unittest.TestLoader().loadTestsFromTestCase(TestReader)
unittest.TextTestRunner(verbosity=2).run(suite)