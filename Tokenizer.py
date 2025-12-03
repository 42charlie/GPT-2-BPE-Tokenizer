from collections import defaultdict
import json
from typing import List, Dict # Added for precise type hinting

class Tokenizer :
    def __init__ (self) :
        '''Initializes the tokenizer with empty corpus, merges, and vocab.'''
        self.corpus = []
        self.merges = []
        self.vocab = {}
        self.vocab_file = "vocab.json"
        self.merges_file = "merges.txt"

    def train(self, filename : str, ntokens : int) -> None:
        '''Trains the tokenizer on a text file for a specific number of tokens.'''
        with open(filename, "r") as file:
            rawData = file.read()
        self.corpus = self.refineRawData(rawData) 
        self.vocab = set(self.corpus)

        for i in range(ntokens):
            print(i, flush=True)
            pairs = self.getPairsFreq()
            if not pairs:
                break
            highPair = max(pairs, key=lambda x: pairs[x])
            
            self.vocab.add("".join(highPair))
            self.merges.append(list(highPair))
            self.updateCorpus(list(highPair))

        self.saveVocab()
        self.saveMerge()

    def getPairsFreq(self) -> Dict[tuple, int]:
        '''Calculates the frequency of adjacent character pairs in the corpus.'''
        pairs = defaultdict(int)
        for i in range(len(self.corpus) - 1):
            pairs[(self.corpus[i], self.corpus[i + 1])] += 1
        return pairs

    def updateCorpus(self, Pair : list) -> None:
        '''Updates the corpus by merging the most frequent pair into a single token.'''
        i = 0
        newCorpus = []
        while (i < len(self.corpus)) :
            if i + 1 < len(self.corpus) and self.corpus[i] == Pair[0] and self.corpus[i+1] == Pair[1] :
                newCorpus.append("".join(Pair))
                i+=2
            else :
                newCorpus.append(self.corpus[i])
                i+=1
        self.corpus = newCorpus

    def saveVocab(self) -> None:
        '''Saves the vocabulary to a JSON file.'''
        vocabJson = {}
        with open(self.vocab_file, "w") as file:
            if isinstance(self.vocab, set):
                vocabJson = {key : int(value) for value, key in enumerate(self.vocab)}
            else:
                vocabJson = self.vocab
            json.dump(vocabJson, file)

    def saveMerge(self) -> None:
        '''Saves the merge rules to a text file.'''
        with open(self.merges_file, "w") as file :
            newData = ""
            for merge in self.merges :
                newData += " ".join(merge) + "\n"
            file.write(newData)

    def getMerge(self) -> None:
        '''Loads merge rules from the file into memory.'''
        with open("merges.txt", "r") as file:
            plainMerges = file.read().splitlines()
        self.merges = [line.split(" ") for line in plainMerges]

    def generatePairs(self, plainText : list) -> Dict[tuple, int]:
        '''Finds valid merge pairs in the current text sequence.'''
        pairs = {}
        for i in range(len(plainText) - 1):
            tmp = plainText[i] + " " + plainText[i+1]
            if [plainText[i], plainText[i+1]] in self.merges: 
                pairs[(plainText[i], plainText[i+1])] = self.merges.index([plainText[i], plainText[i+1]])
            else:
                pass 
        return pairs

    def updatePlainBytes(self, plainText : list, Pair : tuple) -> list[str]:
        '''Replaces a specific pair of tokens in the text with their merged version.'''
        i = 0
        newPlainText = []
        while (i < len(plainText)) :
            if i + 1 < len(plainText) and plainText[i] == Pair[0] and plainText[i+1] == Pair[1] :
                newPlainText.append("".join(Pair))
                i+=2
            else :
                newPlainText.append(plainText[i])
                i+=1
        return newPlainText

    def refineRawData(self, rawData : str) -> list[str]:
        '''Refines raw text by handling spaces and converting to a list of characters.'''
        corpus = []
        for c in rawData :
            if c.isprintable():
                if c == " " :
                    corpus.append("Ġ")
                else :
                    corpus.append(c)
        return corpus

    def encode(self, plainText : str) -> List[int]:
        '''Encodes a string into a list of token IDs.'''
        if not self.merges:
            self.getMerge()
            
        plainBytes = self.refineRawData(plainText)
        
        while True:
            pairs = self.generatePairs(plainBytes)
            if not pairs :
                break
            highPair = min(pairs, key=lambda x: pairs[x])
            plainBytes = self.updatePlainBytes(plainBytes, highPair)
        
        with open(self.vocab_file, "r") as file :
            vocabJson = json.load(file)

        ids = [vocabJson[c] for c in plainBytes]
        return ids

    def decode(self, ids : List[int]) -> str:
        '''Decodes a list of token IDs back into a string.'''
        with open(self.vocab_file, "r") as file :
            vocabJson = json.load(file)
                
        reversedMerges = { key: value for value, key in vocabJson.items()}
        plainTextList = [reversedMerges[_id] for _id in ids]
        plainText = "".join(plainTextList).replace("Ġ", " ")
        return plainText