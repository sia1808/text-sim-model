import math

def clean_text(txt):
    """ takes a string of text txt as a parameter and returns a list
    containing the words in txt after it has been “cleaned” """
    for symbol in """.,?"'!;:""":
        txt = txt.replace(symbol, '')
    txt = txt.lower()
    txt = txt.split()
    return txt

def clean_sentences(txt):
    """ Takes string of text and helps generate splits by sentence in a list """
    for symbol in """!.?""":
        txt = txt.replace(symbol, '%')
    txt = txt.lower()
    txt = txt.split('%')
    return txt[:-1]

def sentence_helper(txt):
    """ Helps the dictionary for sentence lengths"""
    list1 = clean_sentences(txt)
    adder = []
    for i in range(len(list1)):
        y = [list1[i].split()]
        adder += y
    return adder

def clean_punct(txt):
    """ Cleans the text to return a list with all puncuations in the text that are ?!:;
     These are characterised as unique. """
    lst = []
    for x in txt:
        if x == '?':
            lst += ['?']
        elif x == '!':
            lst += ['!']
        elif x == ':':
            lst += [':']
        elif x == ';':
            lst += [';']
        else:
            lst = lst
    return lst
   

def stem(s):
    """The function should then return the stem of s. The stem of a word is
    the root part of the word, which excludes any prefixes and suffixes """
    if s == '':
        return s
    if len(s) == 1:
        return s
    if s[-1] == 's':
        s = s[:-1]
    if s[-3:] == 'ing':
        if len(s) < 5:
            s = s
        else:
            if s[-4] == s[-5]:
                if s[-5:-3] == 'll' or s[-5:-3] == 'ss':
                    s = s[:-3]
                else:
                    s = s[:-4]
            else:
               s = s[:-3]
    elif s[-2:] == 'er' or s[-2:] == 'ed' or s[-2:] == 'al':
        s = s[:-2]
    elif s[-2:] == 'ly':
        s = s[:-3]
    elif s[-2:] == 'es':
        s = s[:-2]
    elif s[-3:] == 'ful':
        if s[-5:-3] == 'er':
            s = s[:-5]
        else:
            s = s[:-3]      
    elif s[-3:] == 'ion':
        s = s[:-3]
    elif s[-1] == 'e':
        if len(s) > 3:
            s = s[:-1]
        else:
            s = s
    elif s[-4:] == 'ally':
        s = s[:-4]
    else:
        s = s
    if len(s) > 1 and s[-1] == 'y':
        s = s[:-1] + 'i'

    return s


def compare_dictionaries(d1, d2):
    """ It should take two feature dictionaries d1 and d2 as inputs, and it
    should compute and return their log similarity score """
    if d1 == {}:
        return -50
    else:
        score = 0
        total = 0
        for x in d1:
            total += d1[x]
        for y in d2:
            if y in d1:
                probability = d1[y]/total
                log_sim_score = d2[y] * math.log(probability)
                score += log_sim_score
            else:
                score += (d2[y] * (math.log(0.5/total)))
        return score


class TextModel:
    """ blueprint for objects that model a body of text  """
   
    def __init__(self, model_name):
        """ constructs a new TextModel object by accepting a string
        model_name as a parameter and initializing name, words,
        and word lengths """
        self.model_name = model_name
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punct = {}
       
    def __repr__(self):
        """ returns a string that includes the name of the model as well as
        the sizes of the dictionaries for each feature of the text """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of unique punctuations: ' + str(len(self.punct)) + '\n'
        return s
   
    def add_string(self, s):
        """ adds a string of text s to the model by augmenting the feature
        dictionaries defined in the constructor. It should not explicitly
        return a value. """
        # Add code to clean the text and split it into a list of words.
        # *Hint:* Call one of the functions you have already written!
        sentence_lengths_list = sentence_helper(s)
        sentence_lengths_list = [len(y) for y in sentence_lengths_list]
        word_list = clean_text(s)
        word_lengths_list = [len(x) for x in word_list]
        stems_list = clean_text(s)
        stems_list = [stem(x) for x in stems_list]
        punct_list = clean_punct(s)
       
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
        for x in word_lengths_list:
            if x not in self.word_lengths:
                self.word_lengths[x] = 1
            else:
                self.word_lengths[x] += 1
        for y in sentence_lengths_list:
            if y not in self.sentence_lengths:
                self.sentence_lengths[y] = 1
            else:
                self.sentence_lengths[y] += 1
        for z in stems_list:
            if z not in self.stems:
                self.stems[z] = 1
            else:
                self.stems[z] += 1
        for a in punct_list:
            if a not in self.punct:
                self.punct[a] = 1
            else:
                self.punct[a] += 1
       
               
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to the
        model. It should not explicitly return a value """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        file_text = f.read()
        self.add_string(file_text)
       
    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores measuring
        the similarity of self and other – one score for each type of feature
        (words, word lengths, stems, sentence lengths, and your
         additional feature). """
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punct_score = compare_dictionaries(other.punct, self.punct)
       
        return [word_score, word_lengths_score, stems_score, sentence_lengths_score, punct_score]
       
    def classify(self, source1, source2):
        """ compares the called TextModel object (self) to two other “source”
        TextModel objects (source1 and source2) and determines which of these
        other TextModels is the more likely source of the called TextModel. """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for ' + source1.name + ': ' + str(scores1))
        print('scores for ' + source2.name + ': ' + str(scores2))
        count1 = 0
        count2 = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                count1 += 1
            else:
                count2 += 1
        if count1 > count2:
            print(self.name + ' is more likely to have come from ' + source1.name)
        else:
            print(self.name + ' is more likely to have come from ' + source2.name)
           
       
    def save_model(self):
        """ saves the TextModel object self by writing its various feature
        dictionaries to files """
        filename_words = self.name + '_' + 'words'
        filename_word_lengths = self.name + '_' + 'word_lengths'
        filename_stems = self.name + '_' + 'stems'
        filename_sentence_lengths = self.name + '_' + 'sentence_lengths'
        filename_punct = self.name + '_' + 'unique_puncts'
        f1 = open(filename_words, 'w')
        f2 = open(filename_word_lengths, 'w')
        f3 = open(filename_stems, 'w')
        f4 = open(filename_sentence_lengths, 'w')
        f5 = open(filename_punct, 'w')
        f1.write(str(self.words))
        f2.write(str(self.word_lengths))
        f3.write(str(self.stems))
        f4.write(str(self.sentence_lengths))
        f5.write(str(self.punct))
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()
       
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object
        from their files and assigns them to the attributes of the
        called TextModel """
        filename_words = self.name + '_' + 'words'
        filename_word_lengths = self.name + '_' + 'word_lengths'
        filename_stems = self.name + '_' + 'stems'
        filename_sentence_lengths = self.name + '_' + 'sentence_lengths'
        filename_punct = self.name + '_' + 'unique_puncts'
        f1 = open(filename_words, 'r')
        f2 = open(filename_word_lengths, 'r')
        f3 = open(filename_stems, 'r')
        f4 = open(filename_sentence_lengths, 'r')
        f5 = open(filename_punct, 'r')
        words_str = f1.read()
        word_lengths_str = f2.read()
        stems_str = f3.read()
        sentence_lengths_str = f4.read()
        punct_str = f5.read()
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()
       
        self.words = dict(eval(words_str))
        self.word_lengths = dict(eval(word_lengths_str))
        self.stems = dict(eval(stems_str))
        self.sentence_lengths = dict(eval(sentence_lengths_str))
        self.punct = dict(eval(punct_str))
       
 

def test():
    """ test your TextModel implementation """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

   
def run_tests():
    """ running tests on all files with models based on Percy Jackson Books
    by Rick Riordan and complete works of Shakespeare. They are tested
    against text sources from another Riordan Percy Jackson Book, a text
    from Shakespeare, Sia's Final Paper on the ethicality of meat consumption,
    and Om's final paper on the analysis of 'No Country for Old Men'. """
   
    source1 = TextModel('rickriordan')
    source1.add_file('rick_riordan.txt')
   
    source2 = TextModel('shakespeare')
    source2.add_file('shakespeare.txt')

    new1 = TextModel('shakespearetest')
    new1.add_file('shakespeareTEST.txt')
    new1.classify(source1, source2)

    # Add code for three other new models below.
   
    new2 = TextModel('riordantest')
    new2.add_file('riordan_test.txt')
    new2.classify(source1, source2)
   
    new3 = TextModel('siafinalpaper')
    new3.add_file('sia_finalpaper.txt')
    new3.classify(source1, source2)
   
    new4 = TextModel('omfinalpaper')
    new4.add_file('Om_WR152_test.txt')
    new4.classify(source1, source2)