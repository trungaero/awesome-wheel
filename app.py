import tkinter as tk
from flask import Flask, request, render_template
import os, sys

global session
global words


app = Flask(__name__, template_folder='templates', static_folder='static')


def read_word_list():
    global words
    with open('list_of_words.txt', 'r') as f:
        words = [tuple(s.split(';')) for s in f.readlines()]
    print(words)


def reset_game():
    global session
    global words
    session = Session(words[0])
    words.pop(0)


class Session:
    IS_REVEALED = 1
    NOT_REVEALED = 0
    MAX_NUM_ATTEMPTS = 99999

    def __init__(self, str):
        self.letters = [s.upper() for s in str[0].strip().replace(' ', '')]
        self.description = str[1]
        self.idx_reveal = [0 for _ in range(len(self.letters))]
        self.idx_last_reveals = self.idx_reveal.copy()
        self.cnt_failed_attempt = 0
        self.unset_failed()

    def unset_failed(self):
        self.is_failed = False

    def set_failed(self):
        self.is_failed = True

    def is_failed_attempt(self):
        return self.is_failed

    def count_letter(self, letter):
        return len([l for l in self.letters if l==letter])

    def reveal_pos(self, pos):
        self.unset_failed()
        self.idx_reveal[pos-1] = self.IS_REVEALED

    def reveal_letter(self, letter):
        self.unset_failed()
        if letter.upper() not in self.letters:
            self.cnt_failed_attempt += 1
            self.set_failed()
        for idx, l in enumerate(self.letters):
            if l==letter.upper():
                self.idx_reveal[idx] = self.IS_REVEALED

    def reveal_random(self, num):
        self.unset_failed()
        import random
        indices = random.sample([i for i in range(len(self.idx_reveal)) if self.idx_reveal[i]==0], num)
        for idx in indices:
            self.idx_reveal[idx] =  self.IS_REVEALED
        
    def disp(self):
        ret = []
        for i,l in enumerate(self.letters):
            if self.idx_reveal[i] == self.IS_REVEALED:
                if self.idx_reveal[i] == self.idx_last_reveals[i]:
                    ret.append((l, 1)) # green box
                else:
                    ret.append((l, 2)) # blinking box
            else:
                ret.append(('', 0))    # grey box

        self.idx_last_reveals = self.idx_reveal.copy()
        return ret
    
    def is_solved(self):
        return all(self.idx_reveal)
    
    def has_no_attempt(self):
        return self.cnt_failed_attempt == self.MAX_NUM_ATTEMPTS
    

@app.route('/')
@app.route('/reveal' , methods=['GET', 'POST'])
def reveal():   
    global session
    if 'next' in request.form:
        reset_game()
        print(session.letters)

    if 'reset' in request.form:
        session.cnt_failed_attempt = max(0, session.cnt_failed_attempt-1)
        session.unset_failed()
    
    try: 
        if request.form['submit_button']=='reveal-by-letter':
            letter = request.form['letter']
            session.reveal_letter(letter)
        elif request.form['submit_button']=='reveal-by-pos':
            position = request.form['position']
            session.reveal_pos(int(position))
        elif request.form['submit_button']=='reveal-random':
            num_random = request.form['num_random']
            session.reveal_random(int(num_random))
    except: 
        pass

    if session.has_no_attempt():
        return render_template(r'entry.html',
                                total_attempts=session.MAX_NUM_ATTEMPTS,
                                num_failed_attempts=session.cnt_failed_attempt,
                                result = 0,
                                description = session.description,
                                box_values=session.disp())

    if session.is_solved():
        return render_template(r'entry.html',
                                total_attempts=session.MAX_NUM_ATTEMPTS,
                                num_failed_attempts=session.cnt_failed_attempt,
                                result = 1,
                                description = session.description,
                                box_values=session.disp())

    return render_template(r'entry.html',
                            total_attempts=session.MAX_NUM_ATTEMPTS,
                            num_failed_attempts=session.cnt_failed_attempt,
                            is_failed = session.is_failed_attempt(),
                            description = session.description,
                            box_values=session.disp())



if __name__ == '__main__':
    read_word_list()
    reset_game()
    app.run(debug=True)





