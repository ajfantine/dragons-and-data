import nltk, time, sys, os
from nltk import word_tokenize
from Player import Player
from collections import defaultdict

choice_dict = defaultdict(int)
#represents the different script sections, where choices are made
end = False
win_loss_dict = defaultdict(list)
win_loss_seq = ''
section_dict = defaultdict(str)

'''Name: get_win_loss()
    Purpose: to pull the win and loss codes from the start of the script.
    Program updates a universal dict with the keys as either win or loss
    and the values as the codes.
    Parameters: the text of the whole script, in str form'''
def get_win_loss(text):
    try:
        markers = [':', ',', '.', '']

        win = text[text.find('WIN'):text.find('\n')]
        elements = win.split(':')
        win_vals = nltk.word_tokenize(elements[1])
        win_vals = [value for value in win_vals if value not in markers]
        win_loss_dict[elements[0]] = win_vals

        text = text[text.find('\n')+1:]

        loss = text[text.find('LOSS'):text.find('\n')]
        elements = loss.split(':')
        loss_vals = nltk.word_tokenize(elements[1])
        loss_vals = [value for value in loss_vals if value not in markers]
        win_loss_dict[elements[0]] = loss_vals

    except IndexError:
        print('File needs win and loss sequences')

'''Name: get_script()
    Purpose: to open any given file, read its contents, and build a
    dict containing each section of text and the code needed to access it.
    Parameters: script, some sort of .txt file'''
def get_script(script):
    script = open(script, 'rU')
    text = ''.join([line for line in script])
    #builds win and loss condition local dictionary
    get_win_loss(text)
    #repeats in case there are multiple script sections
    while text != '':
        start = text.find('START')
        end = text.find('END')

        code = text[start+5:text.find('#')]

        text_bit = text[start+7+len(code):end-1]
        code = 'S' if code == '' else code
        section_dict[code] = text_bit
        text = text[end+4:]

'''Name: play_game()
    Purpose: the method to be used in main, initiates the game
    playing sequence and clears the universal variables when the game ends.
    Parameters: script, some .txt file to be used as the script
                player, an object of the Player class, set to None if
                no parameter is passed'''
def play_game(script, player = None):
    get_script(script)
    play_section(section_dict['S'], player)
    global end
    while end is not True:
        play_section(section_dict[win_loss_seq], player)
    clear()

'''Name: play_section()
    Purpose: to play through a single section at a time, comparing the
    input to the dict containing different options and adding to
    a sequence representing the player's choices.
    Parameters: section, a section of text in str form
                player, an object of the Player class'''
def play_section(section, player):
    ai_input = False
    decision = None

    get_options(section)
    print(section)

    #runs if a Player has been passed
    if player is not None:
        player.open_dictionary()
        player.process(section)
        decision = player.decide()
        ai_input = True

    choice = get_input(decision, ai_input)
    choice = choice.upper()

    for key in choice_dict:
        if choice == key:
            global win_loss_seq
            win_loss_seq += str(choice_dict[key])
        else:
            None

    result = check_win()

    #allows the Player to update its universal dictionary
    if player is not None:
        if result is not None:
            player.update_game_dict(result)

    #must clear choice_dict in case another section has the same
    #keywords with different values
    choice_dict.clear()

'''Name: get_options()
    Purpose: to build a dictionary of all the possible choices and their
    corresponding sequence value in a single section
    Parameters: a section of text, in str form'''
def get_options(text):
    tokens = word_tokenize(text)
    for word in tokens:
        #keywords must be in all caps
        if word.isupper():
            #the first keyword in the section is 0, the second is 1
            if len(choice_dict) % 2 == 0:
                choice_dict[word] = 0
            elif len(choice_dict) % 2 == 1:
                choice_dict[word] = 1

'''Name: get_input()
    Purpose: to check and see if a Player has been passed
    Parameters: decision, the decision given by the player
                ai_input, a bool, whether a Player has been passed
    Returns: decision, the Player's decision
             input(), the user's decision'''
def get_input(decision, ai_input):
    if ai_input is True:
        print('Computer chose ' + decision)
        return decision
    else:
        return input()

'''Name: check_win()
    Purpose: to check and see if the player's choice sequence is
    equal to one of the win or loss sequences, and if so, end the game.'''
def check_win():
    for key in win_loss_dict:
        for sequence in win_loss_dict[key]:
            if win_loss_seq == str(sequence):
                print(section_dict[win_loss_seq])
                print(str(key) + '!')
                global end
                end = True
                return str(key)

'''Name: clear()
    Purpose: to clear all of the universal variables so they can
    be used again if need be in a new game.'''
def clear():
    choice_dict.clear()
    win_loss_dict.clear()
    global win_loss_seq
    win_loss_seq = ''
    section_dict.clear()
    global end
    end = False

if __name__ == '__main__':
    #for i in range(15):
    player = Player()
    play_game('Script.txt', player)
