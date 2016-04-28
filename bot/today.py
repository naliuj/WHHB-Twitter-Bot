import time


def now():
    n = time.localtime()
    return weekday(n[6]), n[3]


def weekday(day):
    return {
        0: "Monday",
        1: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday"
    }[day]
