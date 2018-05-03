import locale
import argparse
import datetime


parser = argparse.ArgumentParser()
parser.add_argument('-L', '--no-locale',
                    action='store_false', dest='locale')
parser.add_argument('-g', '--genindlemmelse',
                    action='store_const', const='gen', default='')
parser.add_argument('name')

msg = ('Velkommen til {name}. For at vise vores tilfredsstillelse med '
       '{gen}indlemmelsen vil alle medlemmer, inden 14 dage, uploade (eller '
       'medvirke i) en ny bundevideo i denne tråd MED EN PERSONLIG HILSEN TIL '
       "{name}... Ellers bliver de sku' smidt ud og kan genansøge en anden "
       'gang!\n'
       'Deadline er altså {date}.')


def set_locale(category, loc):
    try:
        locale.setlocale(category, loc)
    except locale.Error as e:
        filename = '/etc/locale.gen'
        try:
            with open(filename) as fp:
                for line in fp:
                    l = line.split()[0]
                    if l == loc:
                        found = True
                        break
                    elif l.startswith(loc):
                        set_locale(category, l)  # Try again with longer name
                        return
                else:
                    found = False
        except FileNotFoundError:
            print('Could not set locale and could not open %s' % filename)
            raise e
        if found:
            print('Could not set locale to %s, ' % loc +
                  'but the locale is specified in %s. ' % filename +
                  'Maybe you need to run sudo locale-gen.')
        else:
            print('Could not set locale to %s.' % loc)
            print('You should add "%s UTF-8" to %s ' % (loc, filename) +
                  'and run sudo locale-gen.')
        print('Run this program with -L to disable setting the locale.')
        raise SystemExit(1)


def main():
    args = parser.parse_args()
    if args.locale:
        set_locale(locale.LC_ALL, 'da_DK')
    date = datetime.datetime.now()
    date += datetime.timedelta(14)
    date = date.strftime('%A d. {}. %B kl. %H:%M').format(date.day)
    print(msg.format(name=args.name, gen=args.genindlemmelse, date=date))


if __name__ == '__main__':
    main()
