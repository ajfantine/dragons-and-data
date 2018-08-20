import nltk, re, pprint, sys, random
from nltk import word_tokenize
from collections import defaultdict

#note: program should always start by opening the universal dictionary
#and saving to the universal dictionary

class Player:
    def __init__(self):
        #can delete i think
        self._pos = {'Nouns': [], 'Adjectives': [], 'Verbs': [], 'Adverbs': []}
        #a dict of win and loss words, maintained throughout every run
        #of this program (i.e. saved to a file)
        self._dictionary = defaultdict(list)
        #a dict of keywords and their corresponding phrases
        self._keys = defaultdict(list)
        #a dict of keywords and the important words in their
        #corresponding phrase
        self._outcome_dict = defaultdict(list)
        #a list of important words encountered in a playthrough
        self._game_list = []

        self._win_freq_dict = defaultdict(lambda: 0)
        self._loss_freq_dict = defaultdict(lambda: 0)

    ''' Name: open_dictionary
        Purpose: to open the universal dictionary and give the playerbot
        access throughout the code'''
    def open_dictionary(self):
        try:
            markers = [':', ',', '.', '']
            #will always open a file specifically called 'dictionary.txt'
            #since this is where it will save new vocab to as well
            f = open('dictionary.txt', 'rU')
            #gather raw file text
            raw = ''.join([word for word in f])
            #split into lines by presence of newline character
            lines = raw.split('\n')
            lines = [line for line in lines if line not in markers]
            if lines == []:
                #sends empty files to the except block
                raise IndexError
            for line in lines:
                #split into key and value form
                keys = line.split(':')
                #tokenize and standardize values
                values = nltk.word_tokenize(keys[1])
                values = [value for value in values if value not in markers]
                values = [v.lower() for v in values]
                values = sorted(values)
                #update program variable dictionary
                self._dictionary[keys[0]] = values
        #in case the file has not been created or is empty
        except (FileNotFoundError, IndexError) as error:
            print('Error reading file, writing new file!')
            output_file = open('dictionary.txt', 'w')
            print('WIN:', end='', file= output_file)
            print('\n', file= output_file)
            print('LOSS:', end='', file= output_file)

    ''' Name: parse_script
        Purpose: to take a raw bit of text, tag it with parts of speech,
        and return it in phrases.
        Parameters: a str objects
        Returns: a list object, the phrases of the raw string,
        element of the list is a tuple object with the first position
        containing the word and the second its part of speech'''
    def parse_script(self, raw):
        tokens = word_tokenize(raw)
        tagged = nltk.pos_tag(tokens)
        phrases = []
        line = []
        for word in tagged:
            #the word, not the pos tag
            if word[0].isalnum():
                line.append(word)
            else:
                phrases.append(line)
                line = []
        #not sure why this is here, might be useful?
        text = nltk.Text(tokens)
        return(phrases)

    ''' Name: develop_dict
        Purpose: to take in phrases and separate the keyword (the word
        the player would input) from the actual phrase, developing
        the self._keys dictionary
        Parameters: a list of tuples, each obj is a word and its pos tag
        Returns: a dict object with phrase keywords as the keys and phrases
        as the values'''
    def develop_dict(self, phrases):
        #default dictionary in case a nonexistent key is entered
        inputs = defaultdict(lambda: 'NO KEY')
        for phrase in phrases:
            #set key as 'no key' until a key is found
            key = 'NO KEY'
            for word in phrase:
                #this relies on the assumption that keywords will always
                #be all uppercase
                if word[0].isupper():
                    key = word[0]
            inputs[key] = phrase
        #print(list(inputs.items()))
        return inputs

    ''' Name: gather_word_data
        Purpose: to add important words (nouns, adj, verb, adverb) to a
        univeral dictionary to be accessed by the playerbot, and to
        link keywords with their respective phrases in a separate dictionary.
        Parameters: a dict object
        Return: a dict containing keywords as the keys and their respective
        sentences as the values
        '''
    def gather_word_data(self, inputs):
        for key in inputs:
            for word in inputs[key]:
                #ignores data from the phrases lacking a key word
                if key == 'NO KEY':
                    None
                else:
                    self._keys[key].append(word[0].lower())
                    if word[1].startswith('NN'):
                        self._outcome_dict[key].append(word[0].lower())
                        #self._pos['Nouns'].append(word[0])
                    elif word[1].startswith('JJ'):
                        self._outcome_dict[key].append(word[0].lower())
                        #self._pos['Adjectives'].append(word[0])
                    elif word[1].startswith('VB'):
                        self._outcome_dict[key].append(word[0].lower())
                        #self._pos['Verbs'].append(word[0])
                    elif word[1].startswith('RB'):
                        self._outcome_dict[key].append(word[0].lower())
                        #self._pos['Adverbs'].append(word[0])

    ''' Name: save_to_dictionary
        Purpose: to save the new and categorized vocabulary from the
        text to the existing dictionary and onto the 'dictionary.txt' file
        '''
    def save_to_dictionary(self):
        output_file = open('dictionary.txt', 'w')
        for key in self._dictionary:
            try:
                #sort dictionary before reupload
                self._dictionary[key] = sorted(self._dictionary[key])
            except TypeError:
                pass

            print(key + ':', end='', file= output_file)

            try:
                for value in self._dictionary[key]:
                    print(value, end=',', file = output_file)
            except TypeError:
                print(self._dictionary[key], end='', file = output_file)

            print('\n', file= output_file)

    ''' Name: process
        Purpose: to consolidate the different methods for processing
        a script into one callable method.
        Parameters: Script, a bit of text to parse'''
    def process(self, Script):
        #clears so the same keywords cannot be selected multiple times
        #by the computer.
        self._keys.clear()
        phrases = self.parse_script(Script)
        inputs = self.develop_dict(phrases)
        self.gather_word_data(inputs)

    ''' Name: decide
        Purpose: to make a decision whether to use a semi-educated guess
        or a random choice when presented with an option.
        Returns: the keyword associated with the decision made, in str form'''
    def decide(self):
        #print(self._keys)
        self.gather_common_words()
        #print(self._dictionary)
        self.develop_freq_dict()
        #print('win freq dict', self._win_freq_dict)
        #print('loss freq dict', self._loss_freq_dict)

        decision = None

        random = False
        for key in self._outcome_dict:
            for word in self._outcome_dict[key]:
                if word in self._dictionary['CWW']:
                    pass
                elif word in self._dictionary['CLW']:
                    pass
                else:
                    print('WORD IN QUESTION: ', word)
                    random = True


        #checks if there are at least 10 distinct words gathered in the top 50
        #most common win and loss words
        if len(self._dictionary['CWW']) >= 10 and len(self._dictionary['CLW']) >= 10:
            #makes sure the frequencies are in float form
            ww_freq = str(self._dictionary['Average WW Freq'])
            ww_freq = float(ww_freq)
            lw_freq = str(self._dictionary['Average LW Freq'])
            lw_freq = float(lw_freq)
            #checks if the average frequency for a word is >= 10
            if random is True:
                print('1.WORD NOT ACCOUNTED FOR')
                decision = self.random_decision()
            elif ww_freq >= 10.0 and lw_freq >= 10.0:
                decision = self.educated_decision()
            else:
                print('ENOUGH WORDS, NOT ENOUGH TESTS.')
                decision = self.random_decision()
        #checks if there are over 50 examples of win and loss words
        elif len(self._dictionary['WIN']) >= 50 and len(self._dictionary['LOSS']) >= 50:
            if random is True:
                print('2.WORD NOT ACCOUNTED FOR')
                decision = self.random_decision()
            else:
                print('THE SAMPLE IS LARGE BUT NOT VARIED.')
                decision = self.educated_decision()
        else:
            decision = self.random_decision()

        return str(decision)

    ''' Name: educated_decision
        Purpose: to make a decision based on the presence of words associated
        with wins and losses in the phrases enveloping a keyword.
        Returns: a decision, in str form'''
    def educated_decision(self):
        score_dict = defaultdict(int)
        for key in self._keys:
            score = 0
            for word in self._keys[key]:
                if word in self._dictionary['CWW'] and word in self._dictionary['CLW']:
                    if self._win_freq_dict[word] > 5 + self._loss_freq_dict[word]:
                        print(word, ' gives +1 from freq disc')
                        score = score + 1
                    elif self._loss_freq_dict[word] > 5 + self._win_freq_dict[word]:
                        print(word, ' gives -1 from freq disc')
                        score = score - 1
                elif word in self._dictionary['CWW']:
                    print(word, ' gives +1')
                    score = score + 1
                elif word in self._dictionary['CLW']:
                    score = score - 1
                    print(word, ' gives -1')
            score_dict[key] = score
            print(key, ' score is ', score)
        #this is written as such to prevent the need of some arbitrary
        #greatest value, since the scores could be negative or positive
        if score_dict[list(score_dict)[0]] > score_dict[list(score_dict)[1]]:
            decision = list(score_dict)[0]
        else:
            decision = list(score_dict)[1]

        print('EDUCATED CHOICE IS ', str(decision))

        return decision

    ''' Name: random_decision
        Purpose: to make a random decision between the two given options
        Returns: a decision, in str form'''
    def random_decision(self):
        keys = [str(key) for key in self._keys]
        decision = random.choice(keys)
        #for final program, remove this print
        print('RANDOM CHOICE IS ' + decision)
        #this adds relevant words to the list of words encountered in a playthrough
        for value in self._outcome_dict[decision]:
            self._game_list.append(value)
        return decision

    ''' Name: gather_common_words
        Purpose: to gather data on the most common words in win and loss entries,
        and create new entries for those words and the avg freq of a word in the dict.
        '''
    def gather_common_words(self):
        win_text = nltk.Text(self._dictionary['WIN'])
        fdwin = nltk.FreqDist(win_text)
        #common win words
        cww = []
        cwwf = []
        win_sum = 0
        total_ww = 0
        for tup in fdwin.most_common(50):
            #changed to add whole tup so other methods can access freqs
            cwwf.append(tup)
            cww.append(tup[0])
            win_sum += tup[1]
            total_ww += 1
        try:
            avg_ww_freq = win_sum/total_ww
        except ZeroDivisionError:
            avg_ww_freq = 0
        #print('cww: ', cww)
        #print('avg win word freq: ', avg_ww_freq)
        self._dictionary['CWW'] = cww
        self._dictionary['CWWF'] = cwwf
        self._dictionary['Average WW Freq'] = avg_ww_freq

        loss_text = nltk.Text(self._dictionary['LOSS'])
        fdloss = nltk.FreqDist(loss_text)
        #common loss words
        clw = []
        clwf = []
        loss_sum = 0
        total_lw = 0
        for tup in fdloss.most_common(50):
            clwf.append(tup)
            clw.append(tup[0])
            loss_sum += tup[1]
            total_lw += 1
        try:
            avg_lw_freq = loss_sum/total_lw
        except ZeroDivisionError:
            avg_lw_freq = 0
        #print('clw: ', clw)
        #print('avg loss word freq: ', avg_lw_freq)
        self._dictionary['CLW'] = clw
        self._dictionary['CLWF'] = clwf
        self._dictionary['Average LW Freq'] = avg_lw_freq

    def develop_freq_dict(self):
        for tup in self._dictionary['CWWF']:
            self._win_freq_dict[tup[0]] = tup[1]
        for tup in self._dictionary['CLWF']:
            self._loss_freq_dict[tup[0]] = tup[1]

    ''' Name: update_game_dict
        Purpose: to update the universal dictionary with all the words the player
        encountered on its path to a win or loss.
        Paramters: result, either a WIN or LOSS'''
    def update_game_dict(self, result):
        print('The computer had a ' + result)
        if result == 'WIN':
            print('ADDED WIN WORDS ', str(self._game_list))
            for word in self._game_list:
                self._dictionary['WIN'].append(word)
        if result == 'LOSS':
            print('ADDED LOSS WORDS ', str(self._game_list))
            for word in self._game_list:
                self._dictionary['LOSS'].append(word)
        self.save_to_dictionary()

    ''' Name: __str__
        Purpose: to return an easily readable string of the entries
        in the universal dictionary.
        Returns: string, the entries of the universal dictionary'''
    def __str__(self):
        string = 'UNIVERSAL DICTIONARY:\n'
        dict_list = []
        for key in self._dictionary:
            try:
                value = ', '.join([value for value in self._dictionary[key]])
                dict_list.append(str(key) + ': ' + value)
            except TypeError:
                dict_list.append(str(key) + ': ' + str(self._dictionary[key]))
        string = string + '\n'.join([line for line in dict_list])
        return string

if __name__ == '__main__':
    pass
