import os.path
import requests
import datetime
import re

def daterange(start, end):
    dates = []
    n = (end - start).days
    for i in range(n + 1):
        dates.append(start + datetime.timedelta(days=i))

    return dates


def get_style_1_data(data_path):
    # URL style 1
    # 2012-01-24, 2012-01-29
    # http://usa.netflixable.com/2012/01/alphabetical-list-12-pm-tue-jan-24-2012.html
    # http://usa.netflixable.com/2012/01/alphabetical-list-12-pm-wed-jan-25-2012.html

    start = datetime.datetime(2012, 1, 24)
    end = datetime.datetime(2012, 1, 29)

    for d in daterange(start, end):
        year         = d.strftime('%Y')
        padded_month = d.strftime('%m')
        page_date    = d.strftime('%a-%b-%-d-%Y').lower()

        url_parts = ['http://usa.netflixable.com/', year, '/', padded_month, '/alphabetical-list-12-pm-', page_date, '.html']
        url = ''.join(url_parts)

        file_name = 'alpha_list_' + re.sub('-', '_', page_date) + '.html'
        output_file_name = os.path.join(data_path, file_name)

        print 'getting:', url
        page = requests.get(url)

        if page.status_code == 200:
            print 'writing:', output_file_name

            with open(output_file_name, 'w') as output_file:
                print >> output_file, page.content

            print
        else:
            print 'page did not load', '(status ' + str(page.status_code) + ')', ' No data for', page_date


def get_style_2_data(data_path):
    # 2012-01-30, 2012-06-01 (some missing dates, e.g. 2012-02-09 and > 2012-02-17)
    # http://usa.netflixable.com/2012/01/alphabetical-list-1-pm-tue-jan-31-2012.html
    # http://usa.netflixable.com/2012/04/alphabetical-list-1-pm-wed-apr-4-2012.html
    start = datetime.datetime(2012, 1, 30)
    end = datetime.datetime(2012, 6, 1)

    for d in daterange(start, end):
        year         = d.strftime('%Y')
        padded_month = d.strftime('%m')
        page_date    = d.strftime('%a-%b-%-d-%Y').lower()

        url_parts = ['http://usa.netflixable.com/', year, '/', padded_month, '/alphabetical-list-1-pm-', page_date, '.html']
        url = ''.join(url_parts)

        file_name = 'alpha_list_' + re.sub('-', '_', page_date) + '.html'
        output_file_name = os.path.join(data_path, file_name)

        print 'getting:', url
        page = requests.get(url)

        if page.status_code == 200:
            print 'writing:', output_file_name

            with open(output_file_name, 'w') as output_file:
                print >> output_file, page.content

            print
        else:
            print 'page did not load', '(status ' + str(page.status_code) + ')', ' No data for', page_date


def get_style_3_data(data_path):
    # http://usa.netflixable.com/2012/12/alphabetical-list-12-pm-mon-dec-31-2012.html
    start = datetime.datetime(2012, 6, 2)
    end = datetime.datetime(2012, 12, 31)

    for d in daterange(start, end):
        year         = d.strftime('%Y')
        padded_month = d.strftime('%m')
        page_date    = d.strftime('%a-%b-%-d-%Y').lower()

        url_parts = ['http://usa.netflixable.com/', year, '/', padded_month, '/alphabetical-list-12-pm-', page_date, '.html']
        url = ''.join(url_parts)

        file_name = 'alpha_list_' + re.sub('-', '_', page_date) + '.html'
        output_file_name = os.path.join(data_path, file_name)

        print 'getting:', url
        page = requests.get(url)

        if page.status_code == 200:
            print 'writing:', output_file_name

            with open(output_file_name, 'w') as output_file:
                print >> output_file, page.content

            print
        else:
            print 'page did not load', '(status ' + str(page.status_code) + ')', ' No data for', page_date


def main():
    output_file_path = 'data'
    # get_style_1_data(output_file_path)
    # get_style_2_data(output_file_path)
    # get_style_3_data(output_file_path)

if __name__ == '__main__':
    main()