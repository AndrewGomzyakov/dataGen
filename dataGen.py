import json
import sys
import random
import argparse


def get_ht(sex):
    if sex == "M":
        return round(random.gauss(178, 10), 1)
    else:
        return round(random.gauss(166, 10), 1)


def get_age(age):
    if age - 15 < 120 - age:
        return random.randint(15, age + (age - 15))
    else:
        return random.randint(age - (120 - age), 120)


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
            char = random.choice(alph)
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
    random.seed(random.randint(1, 10000))
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


def make_person_surname(sex):
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

    for i in range(1, len(man_surnames)):
        man_surnames[i]["PeoplesCount"] += man_surnames[i - 1]["PeoplesCount"]

    while True:
        if (sex == 'M'):
            surname = man_surnames[random.randint(1, len(man_surnames))]["Surname"]
            yield surname
        else:
            surname = woman_surnames[random.randint(1, len(woman_surnames))]["Surname"]
            yield surname

def make_persons_name(sex):
    man_names = []
    woman_names = []
    with open("man_name_prior.text", "r") as inp:
       for line in inp:
            a = line.split(" ")
            pers = {}
            pers["Name"] = a[0]
            pers["PeoplesCount"] = int(a[1])
            man_names.append(pers)

    with open("woman_name_prior.text", "r") as inp:
       for line in inp:
            a = line.split(" ")
            pers = {}
            pers["Name"] = a[0]
            pers["PeoplesCount"] = int(a[1])
            woman_names.append(pers)

    for i in range(1, len(woman_names)):
        woman_names[i]["PeoplesCount"] += woman_names[i - 1]["PeoplesCount"]
    for i in range(1, len(man_names)):
        man_names[i]["PeoplesCount"] += man_names[i - 1]["PeoplesCount"]

    while True:
        if (sex == 'W'):
            name = find_name(woman_names)["Name"]

        else:
            name = find_name(man_names)["Name"]
        yield name


def make_persons_data(args):
    man_name_gen = make_persons_name('M')
    man_surname_gen = make_person_surname("M")
    woman_name_gen = make_persons_name('W')
    woman_surname_gen = make_person_surname("W")
    mail_gen = get_mail()
    params = ["email", "sex", "name", "surname", "A", "ht", "wt"]
    ext = {}
    for i in params:
        ext[i] = False
    if args.ext != None:
        for i in range(len(args.ext)):
            ext[args.ext[i]] = True
    while True:
        info = {}
        sex = ""
        ht = 0
        if not ext["name"]:
            sex += get_sex(args.chance)
            if sex == "W":
                info["name"] = woman_name_gen.__next__()
            else:
                info["name"] = man_name_gen.__next__()
        if not ext["surname"]:
            if sex == "":
                sex += get_sex(args.chance)
            if sex == "W":
                info["surname"] = woman_surname_gen.__next__()
            else:
                info["surname"] = man_surname_gen.__next__()
        if not ext["sex"]:
            if sex == "":
                sex += get_sex(args.chance)
            info["sex"] = sex
        if not ext["A"]:
            info["age"] = str(get_age(args.age))
        if not ext["ht"]:
            if sex == "":
                sex += get_sex(args.chance)
            ht += get_ht(sex)
            info["ht"] = str(ht)
        if not ext["wt"]:
            if ht == 0:
                if sex == '':
                    sex += get_sex(args.chance)
                ht = get_ht(sex)
            info["wt"] = str(get_wt(ht))
        if not ext["email"]:
            info["mail"] = mail_gen.__next__()
        yield info



def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-c", dest="cnt", type=int, help="задает количество записей, которые необходимо создать")
    parser.add_argument("-s", dest="chance", type=int, help="задает количество запсей мужского пола на 100 записей")
    parser.add_argument("-a", dest="age", type=int, help="задает средний возраст среди всех записей")
    parser.add_argument("-output", dest="output", help="задает имя файла, содержащего сгенеированные данные")

    parser.add_argument("-ext", nargs="+", choices=['email', 'sex', 'surname', "A", "ht", "wt", "name"],
                        help="содержит список флагов, отменяющих создание некоторых данных \n"
                             "email флаг отменяет создание email во всех запися\n"
                             "sex флаг отменяет создание пола в записях\n"
                             "name флаг отменяет создание имени в записях\n"
                             "surname флаг отменяет создание фамилии в записях\n"
                             "A флаг отменяет создание возраста в записях\n"
                             "ht флаг отменяет создание роста в записях\n"
                             "wt флаг отменяет создание веса в записях\n")

    a = [sys.argv[i] for i in range(1, len(sys.argv))]
    args = parser.parse_args(a)
    if args.cnt == None:
        args.cnt = 100
    if args.chance == None:
        args.chance = 50
    if args.age == None:
        args.age = 30
    datagen = make_persons_data(args)
    if args.output == None:
        args.output = "output.text"
    with open(args.output, "w") as out:
        for i in range(args.cnt):
            a = datagen.__next__()
            for j in a.values():
                out.write(j + " ")
            out.write("\n")



if __name__ == "__main__":
    main()
