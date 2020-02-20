import csv
from collections import defaultdict

def csv2py(filename):
    l = list()
    with open('../resources/' + filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            l.append(row)
    return l


class VenezuelaSchema:
    def __init__(self):
        self.__states = dict()
        self.__cities = dict()
        self.__load_city_state_rel()

    def get_states(self):
        return [v for k, v in self.__states.items()]

    def get_cities(self):
        return [k for k, v in self.__cities.items() if len(k) > 2]

    def __load_city_state_rel(self):
        """All cities and states are set to be lower case"""
        new_list_d = csv2py("ciudades.csv")
        for row in new_list_d:
            self.__cities[row[3][1: -1].lower()] = int(row[2][1: -1])

        new_list_d = csv2py("estados.csv")
        for row in new_list_d:
            self.__states[int(row[0][1: -1])] = row[1][1: -1].lower()

        self.__grouped_cities_by_state = defaultdict(list)
        for key, val in sorted(self.__cities.items()):
            # print(key, val)
            self.__grouped_cities_by_state[val].append(key)


    def get_state_from_city(self, ciudad):
        """uses the model created on https://github.com/csalazart/Venezuela-Schema to determine which state the
        city belongs to"""
        return self.__states[self.__cities[ciudad.lower()]]

    def get_cities_of_a_state(self, state):
        """
        No name on city, instead number 1, belonging to state 8

        1536	0	8	1	0241	2006
        1537	0	8	1

        :param state: a string with the name of the state to look up
        :return: a list with the cities that belong to the stated passed as an input
        """
        st_needed = list(self.__states.keys())[list(self.__states.values()).index(state.lower())]
        return [key for (key, value) in self.__cities.items() if value == st_needed]


if __name__ == '__main__':
    rep = VenezuelaSchema()
    print(rep)
    print(rep.get_cities())
    print(rep.get_states())

    ciudad_test = 'Chachopo'
    print('\nA que estado pertenece ' + ciudad_test + '?')
    state = rep.get_state_from_city(ciudad_test)
    print(state)

    edo_test = 'miranda'
    print('\nlas ciudades que pertenecen a: ', edo_test)
    print(rep.get_cities_of_a_state(edo_test))
