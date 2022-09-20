from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """code to run before each test"""
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_home_screen(self):
        """tests that session info and HTML is displayed"""
        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>PLAY BOGGLE</h1>', html)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIn('Score:', html)
            self.assertIn('Seconds Left:', html)

    def test_valid_word(self):
        """test if submitted word is valid"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["R", "N", "U", "R", "R"], 
                                 ["R", "N", "U", "R", "R"], 
                                 ["R", "N", "U", "R", "R"], 
                                 ["R", "N", "U", "R", "R"], 
                                 ["R", "N", "U", "R", "R"]]
            
        res = self.client.get('/check-word?word=run')
        self.assertAlmostEqual(res.json['result'], 'ok')

    def test_invalid_word(self):
        """test if submitted word is invalid"""
        self.client.get('/')
        res = self.client.get('/check-word?word=happy')

        self.assertEqual(res.json['result'], 'not-on-board')

    def test_not_a_word(self):
        """test if submitted word is actually a word"""
        self.client.get('/')
        res = self.client.get('/check-word?word=gggddd')

        self.assertEqual(res.json['result'], 'not-word')

