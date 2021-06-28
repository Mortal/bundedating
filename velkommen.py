import locale
import argparse
import datetime


parser = argparse.ArgumentParser()
parser.add_argument("-L", "--no-locale", action="store_true", help="no-op")
parser.add_argument("-l", "--locale", action="store_true", dest="locale")
parser.add_argument(
    "-g", "--genindlemmelse", action="store_const", const="gen", default=""
)
parser.add_argument("name")

msg = (
    "Velkommen til {name}. For at vise vores tilfredsstillelse med "
    "{gen}indlemmelsen vil alle medlemmer, inden 14 dage, uploade (eller "
    "medvirke i) en ny bundevideo i denne tråd MED EN PERSONLIG HILSEN TIL "
    "{name}... Ellers bliver de sku' smidt ud og kan genansøge en anden "
    "gang!\n"
    "Deadline er altså {date}."
)

WEEKDAYS = "mandag tirsdag onsdag torsdag fredag lørdag søndag"
MONTHS = """- januar februar marts april maj juni
juli august september oktober november december"""


def main():
    args = parser.parse_args()
    if args.no_locale:
        parser.error("-L should not be specified as it is now the default")
    date = datetime.datetime.now()
    date += datetime.timedelta(14)
    if args.locale:
        set_locale(locale.LC_ALL, "da_DK")
        date_keys = dict(
            weekday=date.strftime("%A"),
            month=date.strftime("%B"),
            hour=date.strftime("%H"),
            minute=date.strftime("%M"),
            day=date.day,
        )
    else:
        # WEEKDAYS starts from Monday, so subtract some Monday.
        some_monday = datetime.date(2021, 6, 28).weekday()
        wd = (date.weekday() - some_monday) % 7
        weekday = WEEKDAYS.split()[wd]
        month = MONTHS.split()[date.month]
        date_keys = dict(
            weekday=weekday,
            month=month,
            hour="%02d" % date.hour,
            minute="%02d" % date.minute,
            day=date.day,
        )
    date_str = "{weekday} d. {day}. {month} kl. {hour}:{minute}".format(**date_keys)
    print(msg.format(name=args.name, gen=args.genindlemmelse, date=date_str))


def set_locale(category, loc):
    try:
        locale.setlocale(category, loc)
    except locale.Error as e:
        filename = "/etc/locale.gen"
        try:
            with open(filename) as fp:
                for line in fp:
                    line_loc = line.split()[0]
                    if line_loc == loc:
                        found = True
                        break
                    elif line_loc.startswith(loc):
                        # Try again with longer name
                        set_locale(category, line_loc)
                        return
                else:
                    found = False
        except FileNotFoundError:
            print("Could not set locale and could not open %s" % filename)
            raise e
        if found:
            print(
                "Could not set locale to %s, " % loc
                + "but the locale is specified in %s. " % filename
                + "Maybe you need to run sudo locale-gen."
            )
        else:
            print("Could not set locale to %s." % loc)
            print(
                'You should add "%s UTF-8" to %s ' % (loc, filename)
                + "and run sudo locale-gen."
            )
        print("Run this program with -L to disable setting the locale.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
