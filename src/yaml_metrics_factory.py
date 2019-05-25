
from typing import Tuple
import yaml
import yaml.scanner

from src.suggestions.domain import metrics
from src.suggestions.domain import city_scorer


def _make_metric(metric_name, metric_args: dict):
    return metrics.ExactNameMatchMetric(), 10.0


def load_yaml(yaml_text):
    try:
        config = yaml.load(yaml_text)
    except yaml.scanner.ScannerError:
        raise ValueError("Invalid Yaml file")

    if not isinstance(config, dict):
        raise ValueError("The configuation file is invalid")

    return config


def _make_metrics_from_yaml_text(yaml_text) -> Tuple[city_scorer.SuggestionMetric]:

    if not yaml_text.strip():
        return tuple()

    config = load_yaml(yaml_text)

    return tuple(_make_metric(metric_name, metric_args) for metric_name, metric_args in config.items())


def make_metrics(yaml_file_path):
    with open(yaml_file_path, 'r') as yaml_file:
        return _make_metrics_from_yaml_text(yaml_file.read())
