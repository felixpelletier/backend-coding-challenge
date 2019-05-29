
class SuggestionMetric:

    def compute_score(self, city_infos, query):
        """
        :param city_infos: All the city's infos.
        :param query: The full partial_name
        :return: A similarity score between 0.0 and 1.0. Higher means more similar.
                 A score of None indicates that some information was missing when computing the metric.
                 Ex: If the metrics uses a location and the partial_name has none
        """
        raise NotImplementedError


class CityScorer:

    def __init__(self):
        self._metrics_with_weight = []

    def add_metric(self, metric: SuggestionMetric, weight: float):
        self._metrics_with_weight.append((metric, weight))

    def compute_score_for_city(self, city_infos, query) -> float:
        total_weight = 0.0
        total_score = 0.0
        for metric, weight in self._metrics_with_weight:
            metric_score = metric.compute_score(city_infos, query)
            if metric_score is not None:
                total_score += metric_score * weight
                total_weight += weight

        if total_weight > 0:
            normalized_score = total_score / total_weight
            return normalized_score
        else:
            return 0.0
