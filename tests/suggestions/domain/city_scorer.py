
DEFAULT_CITY_SCORE = 0.0


class FakeCityScorer:

    def __init__(self):
        self._city_scores_by_name = {}

    def compute_score_for_city(self, city_infos, query):
        del query
        return self._city_scores_by_name.get(city_infos['name'], DEFAULT_CITY_SCORE)

    def set_score_for_city(self, city_name, score):
        self._city_scores_by_name[city_name] = score
