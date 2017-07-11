import sys
import json
import codecs
from collections import OrderedDict


class Country:
    def __init__(self, code, name, divisions, code_3, numeric_code):
        self.code = code
        self.name = name
        self.divisions = divisions
        self.code_3 = code_3
        self.numeric_code = numeric_code

    def get_code(self):
        return self.code

    def set_code(self, code):
        self.code = code

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_divisions(self):
        return self.divisions

    def set_divisions(self, divisions):
        self.divisions = divisions

    def get_code_3(self):
        return self.code_3

    def set_code_3(self, code_3):
        self.code = code_3

    def get_numeric_code(self):
        return self.numeric_code

    def set_numeric_code(self, numeric_code):
        self.numeric_code = numeric_code

    def are_names_equal(self, name_2):
        return self.name_1 == name_2


class Division:
    def __init__(self, code, name, type):
        self.code = code
        self.name = name
        self.type = type

    def get_code(self):
        return self.code

    def set_code(self, code):
        self.code = code

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type


class GeoTool:
    def __init__(self, filepath_1, filepath_2):
        self.filepath_1 = filepath_1
        self.filepath_2 = filepath_2

        self.json_countries_1 = None
        self.json_countries_2 = None

        self.diff_1 = None
        self.diff_2 = None

        self.final_country_map = None
        self.differences = None

    def get_json_countries_1(self):
        return self.json_countries_1

    def set_json_countries_1(self, json_countries_1):
        self.json_countries_1 = json_countries_1

    def get_json_countries_2(self):
        return self.json_countries_2

    def set_json_countries_2(self, json_countries_2):
        self.json_countries_2 = json_countries_2

    def get_filepath_1(self):
        return self.filepath_1

    def get_filepath_2(self):
        return self.filepath_2

    def read_json_file(self, filepath):
        d = None
        if filepath is not None:
            with codecs.open(filepath, 'r', encoding='utf8') as json_data:
                d = json.load(json_data)

        return d


    def write_json_file(self, absolute_path, stuff_to_write):
        with codecs.open(absolute_path, 'w', encoding='utf8') as outfile:
            json.dump(stuff_to_write, outfile, indent=4, ensure_ascii=False)


    def compare(self, output):
        final_country_map = {}

        # LOAD FILE 1
        file_1 = self.get_filepath_1()
        country_list = self.read_json_file(file_1)

        # LOAD FILE 2
        file_2 = self.get_filepath_2()
        country_map = self.read_json_file(file_2)

        # ITERATE OVER COUNTRY LIST AND CHECK ON MAP
        for c in country_list:
            country = Country(c['code'], c['name'], None, c['code3'], c['numeric'])

            # CHECK IF COUNTRY IS IN THE MAP
            if country_map.has_key(country.get_code()):
                countryByCode = country_map[country.get_code()]

                # ADD DIVISIONS TO COUNTRY
                divisions = countryByCode['divisions']
                country.set_divisions(divisions)

                # CONVERT INTO JSON AND ADD TO THE FINAL MAP
                final_country_map[country.get_code()] = {'name': country.get_name(), 'divisions': divisions}

            else:
                final_country_map[country.get_code()] = {'name': country.get_name(), 'divisions': {}}
                print ('%s - %s' % (country.get_code(), country.get_name()))

        # SORT
        self.final_country_map = self.sort_map(final_country_map)

        if output is not None:
            self.write_json_file(output, self.final_country_map)


    def division_mapper(self, output):
        final_country_map = {}

        # LOAD FILE 1
        file_1 = self.get_filepath_1()
        division_list = self.read_json_file(file_1)

        # ITERATE OVER DIVISION LIST AND COLLECT THEM
        for d in division_list:
            country_code = d['country_code']
            division = Division(d['code'], d['subdivision_name'], None)
            divisionCode = '%s' % (d['code'])

            # if divisionCode != "-":
            # BUILD A MAP COLLECTING COUNTRY CODE AS KEY AND DIVISION AS VALUE
            if final_country_map.has_key(country_code):
                final_country_map[country_code]['divisions'][divisionCode] = d['subdivision_name']

            else:
                final_country_map[country_code] = {'divisions': {}}
                final_country_map[country_code]['divisions'][divisionCode] = d['subdivision_name']

        # SORT
        self.final_country_map = self.sort_map(final_country_map)

        if output is not None:
            self.write_json_file(output, self.final_country_map)


    def sort_map(self, map_to_sort):
        final_map = OrderedDict()
        sorted_map = sorted(map_to_sort)
        for i in sorted_map:
            final_map[i] = map_to_sort[i]

        return final_map



if __name__ == "__main__":
    # GET FILE PATHS
    argv_size = len(sys.argv)
    filepath_1 = None
    filepath_2 = None

    if argv_size > 1:
        filepath_1 = sys.argv[1]

    if argv_size > 2:
        filepath_2 = sys.argv[2]
        print("######### COUNTRY LISTS COMPARISON [BEGIN] #########")
        geoTool = GeoTool(filepath_1, filepath_2)
        output = "/Users/daniele.autizi/Downloads/subdivision_export.json"
        geoTool.compare(output)
        print("######### COUNTRY LISTS COMPARISON [END] #########")

    else:
        print("######### DIVISIONS MAPPER [BEGIN] #########")
        geoTool = GeoTool(filepath_1, None)
        output = "/Users/daniele.autizi/Downloads/subdivision_export-1.json"
        geoTool.division_mapper(output)
        print("######### DIVISIONS MAPPER [END] #########")
