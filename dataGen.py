import json
import sys
import random
import argparse


def get_ht(sex):
    if sex == "M":
        return round(random.gauss(178, 10), 1)
    else:
        return round(random.gauss(166, 10), 1)


def get_age():
    return random.randint(15, 120)


def get_sex(chance):
    num = random.randint(1, 100)
    if num >= chance:
        return "W"
    else:
        return "M"


def get_wt(ht):
    imt = random.gauss(28, 4)
    return round(imt * ((ht / 100) ** 2), 1)


def get_mail():
    with open("mail.text", "w") as file:
        file.write("\n")
    while True:
        alph = "qwertyuiopasdfghjklzxcvbnm_"
        a = ["gmail.com", "yandex.ru", "mail.ru", "rambler.ru"]
        mail_name = ""
        flag = False
        length = random.randint(5, 10)
        for i in range(length):
            char = alph[random.randint(0, 26)]
            mail_name += char
        with open("mail.text", "r") as file:
            for line in file:
                if line  == mail_name:
                    flag = True
                    break
        if flag:
            continue
        with open("mail.text", "a+") as file:
            file.write(mail_name + "\n")
        yield mail_name + "@" + a[random.randint(0, 3)]


def find_name(names):
    kol = names[len(names) - 1]["PeoplesCount"]
    num = random.randint(0, kol)
    l = 0
    r = len(names)
    while(r - l > 1):
        med = (l + r) // 2
        if names[med]["PeoplesCount"] > num:
            r = med
        else:
            l = med
    if (names[l]["PeoplesCount"] < num):
        return names[r]
    else:
        return names[l]


def make_persons_data(chance):
    man_ends = ["ов", "ев", "ин", "ын", "ий", "ой", "ый"]
    woman_ends = ["ова", "ева", "ина", "ына", "ая"]
    man_names = []
    man_surnames = []
    woman_names = []
    woman_surnames = []
    with open("russian_names.json", "r", encoding="utf8") as inp:
        inp.read(1)
        names = json.load(inp)
    with open("russian_surnames.json", "r", encoding="utf8") as inp:
        inp.read(1)
        surnames = json.load(inp)
    for i in names:
        if i["Sex"] == 'Ж':
            woman_names.append(i)
        else:
            man_names.append(i)
    for i in surnames:
        if i["Surname"][-2:] in man_ends:
            man_surnames.append(i)
        elif i["Surname"][-3:] in woman_ends or i["Surname"][-2:] in woman_ends:
            woman_surnames.append(i)
        else:
            man_surnames.append(i)
            woman_surnames.append(i)

    for i in range(1, len(woman_names)):
        woman_names[i]["PeoplesCount"] += woman_names[i - 1]["PeoplesCount"]
    for i in range(1, len(man_names)):
        man_names[i]["PeoplesCount"] += man_names[i - 1]["PeoplesCount"]

    for i in range(1, len(woman_surnames)):
        woman_surnames[i]["PeoplesCount"] += woman_surnames[i - 1]["PeoplesCount"]
    for i in range(1, len(man_surnames)):
        man_surnames[i]["PeoplesCount"] += man_surnames[i - 1]["PeoplesCount"]
    mail_gen = get_mail()
    while True:
        sex = get_sex(chance)
        age = get_age()
        if (sex == 'M'):
            name = find_name(man_names)["Name"]
            surname = find_name(man_surnames)["Surname"]
        else:
            name = find_name(woman_names)["Name"]
            surname = find_name(woman_surnames)["Surname"]
        email = mail_gen.__next__()
        ht = get_ht(sex)
        wt = get_wt(ht)
        yield (name + " " + surname + " " + str(sex) + " " + str(age) + " " +str(ht) + " " + str(wt) + " " + str(email) + "\n")


def main():

    parser = argparse.ArgumentParser()
    #parser.add_argument("out_file", type = str)
    #parser.add_argument("cnt", type = int)
    #parser.add_argument("chance", type = int)
    #args = parser.parse_args()
    gen = make_persons_data(50)
    for i in range(10):
        print(gen.__next__())

if __name__ == "__main__":
    main()
