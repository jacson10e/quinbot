# JTP-001
#
# JSON Tagger Program
#
# Version 1.0

import json
import collections
import re

import spacy as spacy

# should probably be replaced with random strings to allow the train.py to assign the tags
def findKeywords(line):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(line)
    tags = []
    for entity in doc.ents:
        tags.append(entity.label_)
    return tags
    # return {"conversation", "conversation2"}

def scrub_string(text):
    regex_patterns = ["\(\(.*\)\)", "\[.*\]"]
    new_text = text
    for rgx_match in regex_patterns:
        new_text = re.sub(rgx_match, "", new_text)
    new_text = new_text.strip()
    return new_text

# return a list of intents from a file
def loadIntentsFromFile(conversationFilePath, intents):
    # ignore comments
    current_is_a = True
    curr_string = ""
    pattern = ""
    response = ""
    tags = None
    with open(conversationFilePath, "r") as conversationFile:
        for line in conversationFile:
            #-----------------------------------------------
            #This section is dependent on formatting and will vary from database to database
            line = conversationFile.readline()
            if ":" not in line:
                continue
            line_halves = line.split(":")
            first_half_of_line = line_halves[0]
            second_half_of_line = line_halves[1]
            if (first_half_of_line[len(first_half_of_line) - 1] == 'A') & (current_is_a is True):
                curr_string += " " + second_half_of_line.strip()
                continue
            elif (first_half_of_line[len(first_half_of_line) - 1] == 'A') & (current_is_a is False):
                response = curr_string
                # reset curr_string to start the pattern
                curr_string = second_half_of_line.strip()
                current_is_a = True
                pattern = scrub_string(pattern)
                response = scrub_string(response)
                #don't continue: we now have a pattern and response so find a tag for it
                tags = findKeywords(pattern)
            elif (first_half_of_line[len(first_half_of_line) - 1] == 'B') & (current_is_a is True):
                pattern = curr_string
                # reset curr_string to start the response
                curr_string = second_half_of_line.strip()
                current_is_a = False
                continue
            elif (first_half_of_line[len(first_half_of_line) - 1] == 'B') & (current_is_a is False):
                curr_string += " " + second_half_of_line.strip()
                continue
            else:
                continue

            #--------------------------------------------------------

            #now we have the tags and a pattern/response pair so add the intents
            for tag in tags:
                newIntent = collections.defaultdict(list)
                newIntent["tag"] = tag
                newIntent["patterns"].append(pattern)
                newIntent["responses"].append(response)
                for intent in intents:
                    if (intent["tag"] is not None) and (intent["tag"] == tag):
                        if "patterns" in intent:
                            setWithoutDuplicates = set(intent["patterns"]) - set(newIntent["patterns"])
                            newIntent["patterns"].extend(list(setWithoutDuplicates))
                        if "responses" in intent:
                            setWithoutDuplicates = set(intent["responses"]) - set(newIntent["responses"])
                            newIntent["responses"].extend(list(setWithoutDuplicates))
                        intents.remove(intent)
                intents.append(newIntent)

    return intents


def addExistingIntentsFromFile(jsonFilePath, intents):
    with open(jsonFilePath, "r") as jsonFile:
        rawJsonIntents = json.load(jsonFile)
    print("Type:", type(rawJsonIntents))
    # newIntents = collections.defaultdict(list)
    newIntents = rawJsonIntents["intents"]
    for newIntent in newIntents:
        for intent in intents:
            if (intent["tag"] is not None) and (intent["tag"] == newIntent["tag"]):
                if "patterns" in intent:
                    setWithoutDuplicates = set(intent["patterns"]) - set(newIntent["patterns"])
                    newIntent["patterns"].extend(list(setWithoutDuplicates))
                if "responses" in intent:
                    setWithoutDuplicates = set(intent["responses"]) - set(newIntent["responses"])
                    newIntent["responses"].extend(list(setWithoutDuplicates))
                intents.remove(intent)
        intents.append(newIntent)
    return intents


def addIntentsToJsonFile(jsonFilePath, intents):
    jsonOutput = collections.defaultdict(list)
    for intent in intents:
        jsonOutput["intents"].append(intent)
    with open(jsonFilePath, 'w') as json_file:
        json.dump(jsonOutput, json_file, indent=4, sort_keys=True)
    return


def main():
    jsonFilePath = "jsonFile.json"
    intents = []
    # intents = addExistingIntentsFromFile(jsonFilePath, intents)
    for i in range (5851, 11700):
        leading_zero = ""
        if i < 10000:
            leading_zero = "0"
        conversationFilePath = "C:\\Users\\Ethan\\Documents\\Capstone_Files\\fe_03_p2_tran_LDC2005T19\\fe_03_p2_tran" \
                               "\\data\\trans\\" + leading_zero + str(i // 100) + "\\fe_03_" + leading_zero + str(i) + ".txt"
        intents = loadIntentsFromFile(conversationFilePath, intents)
        print("Finished writing intents in file " + str(i))
        addIntentsToJsonFile(jsonFilePath, intents)
    return


if __name__ == '__main__':
    main()
