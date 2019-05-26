
from typing import Tuple
import yaml
import yaml.scanner

from src.suggestions.domain import metrics
from src.suggestions.domain import city_scorer

_name_to_class_map = {
    "ExactNameMatch": metrics.ExactNameMatchMetric,
    "NameStartsWith": metrics.NameStartsWithMetric,
    "LevenshteinCityNameSimilarity": metrics.LevenshteinCityNameSimilarityMetric,
    "HaversineLocationDistance": metrics.HaversineLocationDistanceMetric,
    "LogarithmicPopulation": metrics.LogarithmicPopulationMetric,
}


class WeightNotFoundError(RuntimeError):
    pass


class MetricNotFoundError(NameError):
    pass


def _make_metric(metric_name, metric_args: dict):
    try:
        metric_class = _name_to_class_map[metric_name]
    except KeyError:
        raise MetricNotFoundError("Unknown metric \"%s\"" % metric_name)

    if not metric_args:
        metric_args = {}

    try:
        metric_weight = metric_args["weight"]
    except KeyError:
        raise WeightNotFoundError

    return metric_class(), metric_weight


def _load_yaml(yaml_text):
    try:
        config = yaml.load(yaml_text)
    except yaml.scanner.ScannerError:
        raise ValueError("Invalid Yaml file")

    if not isinstance(config, dict):
        raise ValueError("The configuation file is invalid")

    return config


def _load_metrics(yaml_text):
        if not yaml_text.strip():
            return tuple()

        config = _load_yaml(yaml_text)

        return tuple(_make_metric(metric_name, metric_args) for metric_name, metric_args in config.items())


class YamlMetricsFactory:

    def __init__(self, yaml_text):
        self.metrics = None
        self._yaml_text = yaml_text

    def make_metrics(self) -> Tuple[city_scorer.SuggestionMetric]:
        if self.metrics:
            return self.metrics

        self.metrics = _load_metrics(self._yaml_text)
        del self._yaml_text
        return self.metrics

    @staticmethod
    def from_yaml_text(yaml_text):
        return YamlMetricsFactory(yaml_text)

    @staticmethod
    def from_file_path(yaml_file_path):
        with open(yaml_file_path, 'r') as yaml_file:
            return YamlMetricsFactory(yaml_file.read())
