import locale
import argparse
import datetime


locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8')

parser = argparse.ArgumentParser()
parser.add_argument('-g', '--genindlemmelse',
                    action='store_const', const='gen', default='')
parser.add_argument('name')

msg = ('Velkommen til {name}. For at vise vores tilfredsstillelse med '
       '{gen}indlemmelsen vil alle medlemmer, inden 14 dage, uploade (eller '
       'medvirke i) en ny bundevideo i denne tråd MED EN PERSONLIG HILSEN TIL '
       "{name}... Ellers bliver de sku' smidt ud og kan genansøge en anden "
       'gang!\n'
       'Deadline er altså {date}.')


def main():
    args = parser.parse_args()
    date = datetime.datetime.now()
    date += datetime.timedelta(14)
    date = date.strftime('%A d. {}. %B kl. %H:%M').format(date.day)
    print(msg.format(name=args.name, gen=args.genindlemmelse, date=date))


if __name__ == '__main__':
    main()
