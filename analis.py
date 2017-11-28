import json
import dataGen
import re
import random


def alal():
    names = []
    with open("name_prior_wom.txt", "r", encoding="utf8") as inp:
        for line in inp:
            s = line.split(" ")
            for i in s:
                if i[0].isalnum() and not i[0].isdigit():
                    if i[-1] == "\n":
                        names.append(i[:-1])
                    else:
                        names.append(i)

    with open("woman_name_prior.text", 'w') as out:
        for i in range(len(names)):
            if i < 33:
                out.write(names[i] +  " " + str(random.randint(100, 700)) + '\n')
            elif i < 66:
                out.write(names[i] +  " " + str(random.randint(25, 100)) + "\n")
            else:
                out.write(names[i] +  " " + str(random.randint(6, 25)) + "\n")

alal()