
class GeonameGazetterFileCityInfoProvider:

    def __init__(self, geoname_tsv_file_path):
        self.geoname_tsv_file_path = geoname_tsv_file_path

    def get_city_infos_list(self):
        geoname_formatted_city_info_list = _load_geoname_city_file(self.geoname_tsv_file_path)
        city_info_list = [_adapt_city_infos_from_geoname_format(raw_city_infos)
                          for raw_city_infos in geoname_formatted_city_info_list]
        return city_info_list

def _load_geoname_city_file(tsv_path):
    with open(tsv_path, 'r', encoding='utf8') as tsv_file:
        column_names = _tokenize_line(next(tsv_file))
        return [_convert_line_to_dict(column_names, line) for line in tsv_file]


def _convert_line_to_dict(column_names, city_row):
    row_data = _tokenize_line(city_row)

    # If this breaks, the file must be wrongly formatted.
    assert len(row_data) == len(column_names)

    return dict(zip(column_names, row_data))


# TODO: Probably safer to use a dataclass
def _adapt_city_infos_from_geoname_format(geoname_city_info):
    # TODO: Add test for not alt_names
    return {
        'name': geoname_city_info['ascii'],
        'alt_names': geoname_city_info['alt_name'].split(',') if geoname_city_info['alt_name'] else [],
        'coordinates': {
            'lat': float(geoname_city_info['lat']),
            'long': float(geoname_city_info['long'])
        },
        'country': geoname_city_info['country'],
    }


def _tokenize_line(line):
    # TODO: Add test to check if any line ends with newline
    return line.rstrip("\n\r").split("\t")
