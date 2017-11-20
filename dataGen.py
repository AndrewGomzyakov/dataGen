import json
import sys
import random

def get_ht(sex):
    if sex == "M":
        return random.gauss(178, 10)
    else:
        return random.gauss(166, 10)

def get_age():
    return random.randint(15, 120)

def get_sex(chance):
    num = random.randint(1, 100)
    if (num >= chance):
        return "W"
    else:
        return "M"

def get_wt(ht):
    imt = random.gauss(28, 4)
    return imt * ((ht / 100) ** 2)

def get_mail(mails):
    alph = "qwertyuiopasdfghjklzxcvbnm_"
    a = ["gmail.com", "yandex.ru", "mail.ru", "rambler.ru"]
    mail_name = ""
    len = random.randint(5, 10)
    for i in range(len):
        char = alph[random.randint(0, 26)]
        mail_name += char
    if mail_name in mails:
        get_mail(mails)
    else:
        mails.append(mail_name)
        return mail_name + "@" + a[random.randint(0, 3)]

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


def make_persons_data(output, cnt,  man_names, man_surnames, woman_names, woman_surnames, chance):
    with open("output.text", "w") as out:
        for i in range(cnt):
            mails = []
            sex = get_sex(chance)
            age = get_age()
            name = ''
            surname = ""
            if (sex == 'M'):
                name = find_name(man_names)["Name"]
                surname = find_name(man_surnames)["Surname"]
            else:
                name = find_name(woman_names)["Name"]
                surname = find_name(woman_surnames)["Surname"]
            email = get_mail(mails)
            ht = get_ht(sex)
            wt = get_wt(ht)
            out.write(name + " " + surname + " " + str(sex) + " " + str(age) + " " +str(ht) + " " + str(wt) + " " + str(email) + "\n")


def main():
    man_ends = ["ов", "ев", "ин", "ын", "ий", "ой", "ый"]
    woman_ends = ["ова", "ева", "ина", "ына", "ая"]
    names = []
    surnames = []
    man_names = []
    man_surnames = []
    woman_names = []
    woman_surnames = []
    with open("D:\\DB\\russian_names.json", "r", encoding="utf8") as inp:
        inp.read(1)
        names = json.load(inp)
    with open("D:\\DB\\russian_surnames.json", "r", encoding="utf8") as inp:
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

    make_persons_data("output.text", 200, man_names, man_surnames, woman_names, woman_surnames, 50)

if __name__ == "__main__":
    main()