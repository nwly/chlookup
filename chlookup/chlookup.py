#!/usr/bin/env python

#####################################
#
# chlookup - looks up and returns the Cantonese and Mandarin pronunciations for given Chinese characters
#          - looks up http://www.mandarintools.com/chardict.html
#
# Author: Nathan Yeung (nathan.yeung at alum.mit.edu)
#
#####################################

import argparse
import random
import robobrowser   # Requires bs4
from tabulate import tabulate

chardictURL = 'http://www.mandarintools.com/chardict.html'

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
               'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',)


def clean(charstr):
    """
    Cleans charstr for dupes
    """
    return charstr

def chlookup(charstr):
    """
    :param charstr: string of Chinese characters
    """

    cleaned_charstr = clean(charstr)

    rb = robobrowser.browser.RoboBrowser(parser='html.parser', user_agent=random.choice(USER_AGENTS))
    rb.open(chardictURL)

    # fill in form
    f = rb.get_forms()[0]
    f['whatchar'].value = cleaned_charstr

    # submit form and collect results
    rb.submit_form(form=f, submit=f.submit_fields['searchchar'])
    soup = rb.parsed

    table_rows = soup.find_all('tr')[1:]

    dialects = {'mando': 3, 'canto': 5}
    mando = dict()
    canto = dict()

    count = 0
    for row in table_rows:
        for dialect in dialects:
            try:
                td = row.find_all('td')[dialects[dialect]]
                if dialect == 'mando':
                    mando[cleaned_charstr[count]] = td.getText()
                elif dialect == 'canto':
                    canto[cleaned_charstr[count]] = td.getText()
            except IndexError:
                continue
        count += 1
    return cleaned_charstr, canto, mando


def print_pronunciation_table(charstr, *args):
    print('======== 真好笑 牛上樹 ========')
    # print('===============================')

    table = list()
    headers = ['', 'Canto', 'Mando']

    for char in charstr:
        printline = [char]
        for arg in args:
            printline.append(arg[char])
            # printline = ' .... '.join([printline, arg[char]])
        table.append(printline)
        # print('{} .. {:^12} .. {:^12}'.format(*printline))
    print(tabulate(table, headers=headers, tablefmt='grid', numalign='center'))


def get_parser():
    parser = argparse.ArgumentParser(description='Regurgitate command line params')
    parser.add_argument('chars', action='append',
                        help='Chinese characters to lookup')
    return parser

def run_command_line():
    parser = get_parser()

    # args is string of Chinese characters
    args = vars(parser.parse_args())['chars'][0]

    cleaned_charstr, canto, mando = chlookup(args)

    print_pronunciation_table(cleaned_charstr, canto, mando)


if __name__ == '__main__':
    run_command_line()
    # cleaned_charstr, canto, mando = chlookup('你好吗')

    # print_pronunciation_table(cleaned_charstr, canto, mando)

    # run_command_line()

    # print(args.accumulate(args.integers))