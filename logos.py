import sys
import string
import random
import phrase_utils as utils

'''
Creation started on: 2019-06-12
Current version: 2019-06-12
'''

# to extract punctuation
translator = str.maketrans('','',string.punctuation)

def conversation():
    min_similarity = 0.6
    exit_logos = False
    f = open('brain.txt')
    brain = []
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        entries = line.split(" ### ")
        brain.append(entries)
    f.close()
    while exit_logos == False:
        sys.stdout.write('>>>USER: ')
        user_input = input()
        if user_input == 'exit' or user_input == 'end' or user_input == 'quit':
            exit_logos = True
            break
        answer_found = False
        possible_answers = []
        for entry in brain:
            if entry[0] == user_input or utils.similarityIndex(words(user_input), words(entry[0])) > min_similarity:
                possible_answers.append(entry[1])
                answer_found = True
        if answer_found == False:
            print('Please enter the desired response to your input: ')
            new_response = input()
            b = open('brain.txt', 'a')
            b.write("\n" + user_input + " ### " + new_response)
            b.close()
            answer(new_response)
        else:
            if len(possible_answers) == 1:
                answer(possible_answers[0])
            elif len(possible_answers) > 1:
                answer(random.choice(possible_answers))


def answer(text):
    print('>>>LOGOS: ' + text.rstrip())

'''Returns a list of lowercase words without punctuation for a given sentence'''
def words(sentence):
    wrds = sentence.split(" ")
    for i in range(len(wrds)):
        if not "'" in wrds[i]:
            wrds[i] = wrds[i].translate(translator).lower()
    return wrds  

if __name__ == '__main__':
    print('<<<<<<<<LOGOS>>>>>>>>')
    conversation()
