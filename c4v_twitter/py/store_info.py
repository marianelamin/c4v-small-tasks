import json
import unicodedata
from py.vzla_schema import VenezuelaSchema
import csv


def write2file(filenum, text):
    filename = 'lista_corpoelec' + filenum + '.json'
    try:
        with open('../resources/' + filename, 'w') as f:
            f.write(text)
    except OSError:
        # 'File not found' error message.
        print("File not found")

def csv2file(filenum, my_list):
    filename = 'lista_corpoelec' + filenum + '.csv'

    try:
        with open('../resources/' + filename, mode='w') as twitter_account_list:
            employee_writer = csv.writer(twitter_account_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in my_list:
                employee_writer.writerow(row)
        # with open('../resources/' + filename, 'w') as f:
        #     f.write(text)
    except OSError:
        # 'File not found' error message.
        print("File not found" + filename)


def file2py(filename):
    f = open('../resources/' + filename, 'r')
    text = f.read()
    # print(text)
    print("****************************")
    return json.loads(text)


if __name__ == '__main__':
    v_s = VenezuelaSchema()
    print(v_s.get_states())

    new_list = file2py("response.json")
    print(len(new_list))
    # print(type(new_list))

    # json_file = '[{"name": "ha1", "age": 12, "bo": true}, {"name": "Manuel", "age": 12.3, "bo": false}]'
    # json2py = json.loads(json_file)
    # print(json2py)
    # print(type(json2py))

    states = [(s, list()) for s in v_s.get_states()]

    text_to_save = ""
    for state in states:
        # state = 'Lara'
        st = state[0].lower()
        print('\n*******************************')
        print('state: ', st)
        account_matched = False
        for account in new_list:
            handler = "@" + account['screen_name']
            acc_name = account['name']
            acc_location = account['location']
            acc_desc = account['description']
            # Mon Mar 08 13:32:59 +0000 2010
            # acc_joined_year = int(account['created_at'].split()[-1])
            acc_verify = account['verified']

            account_info = (handler + ' ' + acc_name + ' ' + acc_desc + ' ' + acc_location).lower()
            text = unicodedata.normalize('NFD', account_info) \
            .encode('ascii', 'ignore') \
            .decode("utf-8")

            # print(account_info)
            # print('\t', text)
            if st in text:
                account_matched = True
                print('\t\tmatched-- :', text)
                state[1].append(
                    {"handler": '@'+account['screen_name'],
                     "acc_name": account['name'],
                     "acc_descripción": account['description'],
                     "acc_location": account['location']}
                )
                # print(acc_name, '\t', state)
                # delete the acc from new_list
                try:
                    new_list.remove(account)
                    continue
                except ValueError:
                    print('---Already deleted: @', account['screen_name'])
        if not account_matched:
            print('State "has no" account')


    # TODO: classify if it matches a city.
    #  This doesnt work because there are cities with names such as "La Luz"
    # print('Not classified: ')
    # count = 0
    # for i in new_list:
    #
    #     acc_content = ('@'+i['screen_name'] + i['name'] + i['location'] + i['description']).lower()
    #     acc_content_test = ('@' + i['screen_name'] + i['name'] + i['location'] + i['description']).lower()\
    #         .replace('corpoelec', ' ')
    #     for ciudad in v_s.get_cities():
    #         ciudad_match = False
    #         if ciudad in acc_content_test:
    #             ciudad_match = True
    #             print('--------- account\t', acc_content, '\t matched ---- ', ciudad)
    #             count = count + 1
    #             continue
    #     print(acc_content)
    #
    # print('matched',  count)

    print('elements in new_list: ', len(new_list))
    rows = list()
    for s in states:
        cols = list()
        # print(s[0])
        cols.append(s[0].upper())
        for acc in s[1]:
            # print(acc['handler'])
            cols.append(acc['handler'])
        rows.append(cols)

    # print(rows)

    # how many accounts were saved?
    print(sum([(len(r)-1) for r in rows]))

    # Save as csv the state and handler
    csv2file("", rows)
    # Save as json the accounts that were not classified
    write2file("_non_classified_accounts", json.dumps(new_list, indent=4))
