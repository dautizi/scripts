import sys
import os
import json
import codecs
import csv
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


class GeoIP2Location:
    def __init__(self, geoname_id, locale_code, continent_code, continent_name, country_iso_code,
                 country_name, subdivision_1_iso_code, subdivision_1_name, subdivision_2_iso_code,
                 subdivision_2_name, city_name, metro_code, time_zone):

        self.geoname_id = geoname_id
        self.locale_code = locale_code
        self.continent_code = continent_code
        self.continent_name = continent_name
        self.country_iso_code = country_iso_code
        self.country_name =country_name
        self.subdivision_1_iso_code =subdivision_1_iso_code
        self.subdivision_1_name =subdivision_1_name
        self.subdivision_2_iso_code = subdivision_2_iso_code
        self.subdivision_2_name = subdivision_2_name
        self.city_name = city_name
        self.metro_code = metro_code
        self.time_zone = time_zone

    def get_geoname_id(self):
        return self.geoname_id

    def set_geoname_id(self, geoname_id):
        self.geoname_id = geoname_id

    def get_locale_code(self):
        return self.locale_code

    def set_locale_code(self, locale_code):
        self.locale_code = locale_code

    def get_continent_code(self):
        return self.continent_code

    def set_continent_code(self, continent_code):
        self.continent_code = continent_code

    def get_continent_name(self):
        return self.continent_name

    def set_continent_name(self, continent_name):
        self.continent_name = continent_name

    def get_country_iso_code(self):
        return self.country_iso_code

    def set_country_iso_code(self, country_iso_code):
        self.country_iso_code = country_iso_code

    def get_country_name(self):
        return self.country_name

    def set_country_name(self, country_name):
        self.country_name = country_name

    def get_subdivision_1_iso_code(self):
        return self.subdivision_1_iso_code

    def set_subdivision_1_iso_code(self, subdivision_1_iso_code):
        self.subdivision_1_iso_code = subdivision_1_iso_code

    def get_subdivision_1_name(self):
        return self.subdivision_1_name

    def set_subdivision_1_name(self, subdivision_1_name):
        self.subdivision_1_name = subdivision_1_name

    def get_subdivision_2_iso_code(self):
        return self.subdivision_2_iso_code

    def set_subdivision_2_iso_code(self, subdivision_2_iso_code):
        self.subdivision_2_iso_code = subdivision_2_iso_code

    def get_subdivision_2_name(self):
        return self.subdivision_2_name

    def set_(self, subdivision_2_name):
        self.subdivision_2_name = subdivision_2_name

    def get_city_name(self):
        return self.city_name

    def set_city_name(self, city_name):
        self.city_name = city_name

    def get_metro_code(self):
        return self.metro_code

    def set_metro_code(self, metro_code):
        self.metro_code = metro_code

    def get_time_zone(self):
        return self.time_zone

    def set_time_zone(self, time_zone):
        self.time_zone = time_zone


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


    def open_and_convert_csv_file_into_json(self, filepath):
        json_file = None
        if filepath is not None:
            filename, file_extension = os.path.splitext(filepath)

            if os.path.isfile(filepath) and file_extension == '.csv':
                with codecs.open(filepath, 'r') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)

                json_file = '%s.%s' % (filename, 'json')
                with codecs.open(json_file, 'w') as outfile:
                    json.dump(rows, outfile)

            else:
                print 'Input file %s not found or not in a valid csv format.' % (filepath)
        else:
            print 'You did not provide an input file. '

        return json_file

    def read_json_file(self, filepath):
        d = None
        if filepath is not None:
            with codecs.open(filepath, 'r', encoding='utf8') as json_data:
                d = json.load(json_data)

        return d

    def write_json_file(self, absolute_path, stuff_to_write):
        with codecs.open(absolute_path, 'w', encoding='utf8') as outfile:
            json.dump(stuff_to_write, outfile, indent=4, ensure_ascii=False)

    def generate_map_from_geoIP2_list(self, output):
        self.final_country_map = {}

        # CONVERT CSV FILE
        csv_file = self.get_filepath_1()
        json_file = self.open_and_convert_csv_file_into_json(csv_file)

        if json_file is None:
            print 'Nothing has been generated!'
            return None

        # LOAD FILE 1
        geo_ip2_location_list = self.read_json_file(json_file)

        # ITERATE OVER COUNTRY LIST AND CHECK ON MAP
        for l in geo_ip2_location_list:
            location = GeoIP2Location(l['geoname_id'], l['locale_code'], l['continent_code'], l['continent_name'],
                                    l['country_iso_code'], l['country_name'], l['subdivision_1_iso_code'],
                                    l['subdivision_1_name'], l['subdivision_2_iso_code'], l['subdivision_2_name'],
                                    l['city_name'], l['metro_code'], l['time_zone'])

            country_code = location.get_country_iso_code()
            if country_code is not None and country_code != "":
                # CHECK IF LOCATION IS ALREADY IN THE MAP
                if country_code in self.final_country_map:
                    self.set_subdivisions(location)

                else:
                    self.final_country_map[country_code] = {'name': location.get_country_name(), 'divisions': {}}
                    print ('%s - %s' % (country_code, location.get_country_name()))
                    self.set_subdivisions(location)

        # SORT
        self.final_country_map = self.sort_map(self.final_country_map)

        if output is not None:
            self.write_json_file(output, self.final_country_map)

    def set_subdivisions(self, location):
        country_code = location.get_country_iso_code()

        # CHECK THE SUBDIVISION_1
        subdivision_1_code = location.get_subdivision_1_iso_code()
        subdivision_1_name = location.get_subdivision_1_name()
        if subdivision_1_code is not None and subdivision_1_code != "":
            division_code = '%s-%s' % (country_code, subdivision_1_code)

            if division_code not in self.final_country_map[country_code]['divisions']:
                self.final_country_map[country_code]['divisions'][division_code] = subdivision_1_name

    def sort_map(self, map_to_sort):
        final_map = OrderedDict()
        sorted_map = sorted(map_to_sort)
        for i in sorted_map:
            final_map[i] = map_to_sort[i]

        return final_map



if __name__ == "__main__":
    # HOW TO CALL
    # 1. install OrderedDict module: pip install ordereddict
    # python geo-comparator.py /your_path/GeoIP2-City-Locations-en.csv /your_path/xxx.json
    default_output = "/tmp/country_map.json"

    # GET FILE PATHS
    argv_size = len(sys.argv)
    filepath_1 = None

    if argv_size > 1:
        filepath_1 = sys.argv[1]

    print("######### COUNTRY MAP BUILDING [BEGIN] #########")
    geoTool = GeoTool(filepath_1, None)

    if argv_size > 2:
        default_output = sys.argv[2]
        geoTool.generate_map_from_geoIP2_list(default_output)

    else:
        geoTool.generate_map_from_geoIP2_list(default_output)

    print("Output: %s" % default_output)
    print("######### COUNTRY MAP BUILDING [END] #########")