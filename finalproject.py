



def clean_text(txt):
    """ takes a string of text txt as a parameter and returns a list 
    containing the words in txt after it has been “cleaned” """
    for symbol in """.,?"'!;:""":
        txt = txt.replace(symbol,'')
    txt = txt.lower()
    txt = txt.split()
    return txt


class TextModel:
    """ blueprint for objects that model a body of text  """
    
    def __init__(self, model_name):
        """ constructs a new TextModel object by accepting a string model_name
        as a parameter and initializes attributes """
        self.model_name = model_name
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        
    def __repr__(self):
        """ returns a string that includes the name of the model as well as 
        the sizes of the dictionaries for each feature of the text """
        s = 'text model name: '  + str(self.name) + '\n'
        s +='  number of words: ' + str(len(self.words)) + '\n'
        s +='  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        return s
    
    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
        to all of the dictionaries in this text model.
        """
        word_list = clean_text(s)
        word_length_list = [len(x) for x in word_list]

        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
                
        for x in word_length_list:
            if x not in self.word_lengths:
                self.word_lengths[x] = 1
            else:
                self.word_lengths[x] += 1
        
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to the 
        model. It should not explicitly return a value """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        file_text = f.read()
        self.add_string(file_text)
    
    def save_model(self):
        """ saves the TextModel object self by writing its various 
        feature dictionaries to files """
        file_name_words = self.name + '_' + 'words'
        file_name_word_lengths = self.name + '_' + 'word_lengths'
        f_words = open(file_name_words, 'w')
        f_words.write(str(self.words))
        f_wordlengths = open(file_name_word_lengths, 'w')
        f_wordlengths.write(str(self.word_lengths))
        f_words.close()
        f_wordlengths.close()
    
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object 
        from their files and assigns them to the attributes of the 
        called TextModel """
        file_name_words = self.name + '_' + 'words'
        file_name_word_lengths = self.name + '_' + 'word_lengths'
        f1 = open(file_name_words,'r')
        f2 = open(file_name_word_lengths, 'r')
        words_str = f1.read()
        word_lengths_str = f2.read()
        f1.close()
        f2.close()
        self.words = dict(eval(words_str))
        self.word_lengths = dict(eval(word_lengths_str))
    
    
        
        
                