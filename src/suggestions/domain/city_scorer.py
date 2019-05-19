
class CityScorer:

    def __init__(self):
        self._metrics_with_weight = []

    def add_metric(self, metric, weight : float):
        self._metrics_with_weight.append((metric, weight))

    def compute_score_for_city(self, city_infos, query):
        total_weight = sum(weight for metric, weight in self._metrics_with_weight)
        if total_weight == 0:
            return 0.0

        total_score = sum(metric.compute_score(city_infos, query) * weight for metric, weight in self._metrics_with_weight)
        normalized_score = total_score / total_weight
        return normalized_score

