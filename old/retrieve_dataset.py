#!./env/bin/python
import sqlite3
import itertools
import random
import pdb


class Retriever:
    def __init__(self):
        # Setup libraries
        conn = sqlite3.connect('db/matchesV2.db')
        cur = conn.cursor()
        tempConn = sqlite3.connect('db/gamedata.db')
        tempCur = conn.cursor()

        # Define format_input function
        self.champs_len = tempConn.execute('SELECT COUNT(*) FROM champions').fetchone()[0]
        self.champ_bit_pos = dict(tempConn.execute('SELECT champid, rowid-1 FROM champions'))

        # Create test and training sets
        # data_len = cur.execute('SELECT COUNT(*) FROM matches WHERE timestamp > "2016-04-10"').fetchone()[0]
        data_len = cur.execute('SELECT COUNT(*) FROM matches').fetchone()[0]
        # data = cur.execute('SELECT blueWin, b1, b2, b3, b4, b5, r1, r2, r3, r4, r5 FROM matches WHERE timestamp > "2016-04-10" ORDER BY RANDOM()')
        query = cur.execute('SELECT blueWin, b1, b2, b3, b4, b5, r1, r2, r3, r4, r5 FROM matches ORDER BY RANDOM()')
        self.data = [(self.format_input(row[1:]), row[0]) for row in query]

        tempConn.close()
        conn.close()

    def format_input(self, X):
        result = [False] * self.champs_len * 2
        for x in X[0:4]:
            result[self.champ_bit_pos[x]] = True
        for x in X[5:9]:
            result[self.champs_len + self.champ_bit_pos[x]] = True
        # result = result + [True] # Add bias
        return result

    def shuffle(self):
        random.shuffle(self.data)

    def get_data(self, length=None):
        length = len(self.data) if length is None else length
        return self.data[0:length]

    def get_x(self, length=None):
        length = len(self.data) if length is None else length
        return [d[0] for d in data[0:length]]

    def get_y(self, length=None):
        length = len(self.data) if length is None else length
        return [d[1] for d in data[0:length]]

    # TODO: Fix this code to be better as a module
    # # Create summary of (champ_name, team_color, champ_freq_on_team, theta i for champ i)
    # champ_names = list(zip(*tempConn.execute('SELECT name FROM champions ORDER BY rowid')))[0]
    # team_color = ('b') * champs_len + ('r') * champs_len
    # champ_freq_on_team = [0] * champs_len * 2
    # for x in train_x:
    #   champ_freq_on_team = map(sum, zip(x,champ_freq_on_team))
    # champ_freq_on_team = list(champ_freq_on_team)
    # summary = list(zip(champ_names*2, team_color, champ_freq_on_team, clf.coef_[0]))
    # # Sort summary by theta i for champ i
    # summary.sort(key=lambda x: x[3])