import json
import dataGen


def alal():
    man_ends = ["ов", "ев", "ин", "ын", "ий", "ой", "ый"]
    woman_ends = ["ова", "ева", "ина", "ына", "ая"]
    man_surnames = []
    woman_surnames = []
    with open("russian_surnames.json", "r", encoding="utf8") as inp:
        inp.read(1)
        surnames = json.load(inp)
    for i in surnames:
        if i["Surname"][-2:] in man_ends:
            man_surnames.append(i)
        elif i["Surname"][-3:] in woman_ends or i["Surname"][-2:] in woman_ends:
            woman_surnames.append(i)
        else:
            man_surnames.append(i)
            woman_surnames.append(i)

    for i in range(1, len(woman_surnames)):
        woman_surnames[i]["PeoplesCount"] += woman_surnames[i - 1]["PeoplesCount"]
    gen = dataGen.make_person_surname("W")

    for i in range(100):
        print(gen.__next__())
alal()