#!/usr/bin/python 
import unittest 
import analyzer
import datetime
from collections import deque
import copy

class TestAnalyzer(unittest.TestCase):
	def test_refaddvertex(self):
		vref1 = {'hello':1}
		vertices1 = ['hello','world','Troy']
		analyzer.refaddvertex(vref1,vertices1)
		self.assertEqual(vref1,{'hello':3,'world':2, 'Troy':2})

		vref2 = {'world':1}
		vertices2=['hello']
		analyzer.refaddvertex(vref2,vertices2)
		self.assertEqual(vref2,{'world':1})

	def test_refdeletevertex(self):
		vref1 = {'hello':3, 'world':4}
		vertices1 = ['babe']
		analyzer.refdeletevertex(vref1,vertices1)
		self.assertEqual(vref1,{'hello':3,'world':4})

		vref2 = {'hello':1, 'world':4, 'Dayum': 2}
		vertices2 = ['hello','world']
		analyzer.refdeletevertex(vref2,vertices2)
		self.assertEqual(vref2,{'world':3, 'Dayum':2})

	def test_outoftime(self):
		t = datetime.datetime.min
		Q = deque()
		Q.append((datetime.datetime(2008, 11, 22, 19, 53, 42),['hello','world']))
		Q.append((datetime.datetime(2008, 11, 22, 19, 57, 42),['hello','thanks','Rudi']))
		self.assertTrue(analyzer.outoftime(Q,t))

		t = datetime.datetime.max
		self.assertFalse(analyzer.outoftime(Q,t))

	def test_old(self):
		t = datetime.datetime(2008, 11, 22, 19, 57, 40)
		Q = deque()
		Q.append((datetime.datetime(2008, 11, 22, 19, 57, 42),['hello','thanks','Rudi']))
		self.assertFalse(analyzer.old(Q,t))

		t = datetime.datetime(2008, 11, 22, 19, 50, 55)
		Q = deque()		
		Q.append((datetime.datetime(2008, 11, 22, 19, 53, 42),['hello','world']))
		Q.append((datetime.datetime(2008, 11, 22, 19, 57, 42),['hello','thanks','Rudi']))
		self.assertTrue(analyzer.old(Q,t))

	def test_fixoutoftime(self):
		Q1 = deque()
		Q1.append((datetime.datetime(2008, 11, 22, 19, 53, 42),['hello','world']))
		vref1 = {'hello':1,'world':1}

		t1 = datetime.datetime(2008, 11, 22, 19, 50, 55)
		vertices1 = ['hello','Rudi','skip']

		P1 = deque()
		P1.append((datetime.datetime(2008, 11, 22, 19, 53, 42),['hello','world']))
		P1.appendleft((t1,vertices1))

		analyzer.fixoutoftime(Q1,t1,vertices1,vref1)
		self.assertEqual(Q1,P1)
		self.assertEqual(vref1,{'hello':3, 'world':1, 'Rudi':2, 'skip':2})
		

		Q2 = deque()
		Q2.append((datetime.datetime(2008, 11, 22, 19, 53, 42),['hello','world']))
		Q2.append((datetime.datetime(2008, 11, 22, 19, 53, 48),['rawr','world']))
		vref2 = {'hello':1,'world':1}

		t2 = datetime.datetime(2008, 11, 22, 19, 53, 47)
		vertices2 = ['hello','Rudi','skip']

		analyzer.fixoutoftime(Q2,t2,vertices2,vref2)
		P2 = deque()
		P2.append((datetime.datetime(2008, 11, 22, 19, 53, 42),['hello','world']))
		P2.append((t2,vertices2))
		P2.append((datetime.datetime(2008, 11, 22, 19, 53, 48),['rawr','world']))
		self.assertEqual(Q2,P2)

	def test_refresh(self):
		Q1 = deque()
		Q1.append((datetime.datetime(2008, 11, 22, 19, 57, 42),['hello','thanks','Rudi']))
		vref1 = {'hello':2, 'thanks':2, 'Rudi':2}
		t1 = datetime.datetime(2008, 11, 22, 19, 57, 43)
		vertices1 = ['bla','hello']

		analyzer.refresh(Q1,t1,vertices1,vref1)
		P1 = deque()
		P1.append((datetime.datetime(2008, 11, 22, 19, 57, 42),['hello','thanks','Rudi']))
		P1.append((t1,vertices1))
		self.assertEqual(Q1,P1)
		self.assertEqual(vref1,{'hello':3, 'thanks':2, 'Rudi':2, 'bla':1})

		Q2 = deque()
		Q2.append((datetime.datetime(2008, 11, 22, 19, 57, 42),['hello','thanks','Rudi']))
		vref2 = {'hello':2, 'thanks':2, 'Rudi':2}
		t2 = datetime.datetime(2008, 11, 22, 19, 58, 43)
		vertices2 = ['bla','hello']
		
		analyzer.refresh(Q2,t2,vertices2,vref2)
		P2 = deque()
		P2.append((t2,vertices2))
		self.assertEqual(Q2,P2)
		self.assertEqual(vref2,{'bla':1,'hello':1})

	def test_calc_avg(self):
		vref = {}
		self.assertEqual(analyzer.calc_avg(vref),'0.00')

		vref = {'hello':3, 'world':2}
		self.assertEqual(analyzer.calc_avg(vref), '2.50')

suite = unittest.TestLoader().loadTestsFromTestCase(TestAnalyzer)
unittest.TextTestRunner(verbosity=2).run(suite)