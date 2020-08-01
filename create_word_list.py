#! /usr/bin/python3

import click
import os
# from os import listdir
from os.path import isfile, join
import re
import ntpath


class Word:

    def __init__(self, word):
        self.word = word
        self.meanings = []

    def add_meaning(self, meaning):
        self.meanings.append(meaning)

    def add_meanings(self, meanings):
        self.meanings.extend(meanings)


#def path_leaf(path):
#    head, tail = ntpath.split(path)
#    return tail or ntpath.basename(head)


def process_file(filePath):
    # meanings = []
    print("filePath = " + filePath)
    leafname = os.path.basename(filePath)
    word_re = re.compile('([^0-9]+)[0-9]?.md')
    word_match = word_re.match(leafname)
    print("leafname = " + leafname)
    if(not word_match):
        raise NameError('word file name did not match <word>.md pattern')
    word_string = word_match.group(1)
    print("word string = " + word_string)
    result = Word(word_string)
    p = re.compile('\*\*([^*]+)\*\*')
    with open(filePath, "r", encoding='utf-8') as file:
        for line in file:
            matches = p.findall(line)
            for i in matches:
                print("meaning = " + i)
                result.add_meaning(i)
    return result


def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def generate_trainer_file(words, output_file_name):
    with open(output_file_name, "w", encoding="utf-8") as outfile:
        for word in words:
            outfile.write(word.word + " - ")
            last_x = ""
            for x in word.meanings:
                outfile.write(x)
                if(not last_x.endswith(",")):
                    outfile.write(",")
                last_x = x
            outfile.write("\n")
        outfile.close
    return


@click.command()
@click.option('--input-folder', type=click.Path(file_okay=False, readable=True, exists=True), required=True, help='The folder which contains the individual dictionary entries')
@click.option('--output-file', type=click.Path(dir_okay=False, writable=True, exists=False), required=True, help='The path to the trainer file to generate')
def process_folder(input_folder, output_file):
    # onlyfiles = [f for f in listdir(input_folder) if isfile(join(input_folder, f))]
    words = []
    for file in files(input_folder):
        # print(file)
        words.append(process_file(os.path.join(input_folder, file)))
    generate_trainer_file(words, output_file)


if __name__ == "__main__":
    process_folder()
