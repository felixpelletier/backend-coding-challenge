
from typing import ClassVar
import pytest
import yaml
from src import yaml_metrics_factory
from src.suggestions.domain import metrics


def load_config_from_raw_text(config_text: str):
    factory = yaml_metrics_factory.YamlMetricsFactory.from_yaml_text(config_text)
    return factory.make_metrics()


def load_config_from_text(config_text: str):
    non_empty_lines = [line for line in config_text.splitlines() if line.strip()]
    if non_empty_lines:
        total_whitespace_per_line = ((len(line) - len(line.lstrip())) for line in non_empty_lines)
        whitespace_to_remove = min(total_whitespace_per_line)
        ajusted_config_text = "\n".join(line[whitespace_to_remove:] for line in config_text.splitlines())
        return load_config_from_raw_text(ajusted_config_text)
    else:
        return load_config_from_raw_text(config_text)


def load_config_from_dict(config_data: dict):
    raw_yaml_text = yaml.dump(config_data)
    return load_config_from_raw_text(raw_yaml_text)


def assert_right_metric_is_created(config_text: str, metric_class: ClassVar):
    actual_metric, actual_weight = load_config_from_text(config_text)[0]
    assert isinstance(actual_metric, metric_class)


def test_empty_file():
    assert load_config_from_raw_text("") == tuple()


def test_invalid_text():
    with pytest.raises(ValueError):
        load_config_from_raw_text("This is some invalid yaml")


def test_weight():
    expected_weight = 42.4
    config_text = """
        ExactNameMatch:
            weight: %f
    """ % expected_weight
    _, actual_weight = load_config_from_text(config_text)[0]
    assert actual_weight == expected_weight


def test_when_no_weight_raises_weight_not_found_error():
    config_text = """
        ExactNameMatch:
    """
    with pytest.raises(yaml_metrics_factory.WeightNotFoundError):
        load_config_from_text(config_text)


def test_when_metric_doesnt_exist_raises_metric_not_found_error():
    config_text = """
        SomeNonExistentMetric:
            weight: 10
    """
    with pytest.raises(yaml_metrics_factory.MetricNotFoundError):
        load_config_from_text(config_text)


def test_exact_match_metric():
    config_text = """
        ExactNameMatch:
            weight: 10
    """
    assert_right_metric_is_created(config_text, metrics.ExactNameMatchMetric)


def test_starts_with_metric():
    config_text = """
        NameStartsWith:
            weight: 20
    """
    assert_right_metric_is_created(config_text, metrics.NameStartsWithMetric)


def test_levenshtein_metric():
    config_text = """
        LevenshteinCityNameSimilarity:
            weight: 20
    """
    assert_right_metric_is_created(config_text, metrics.LevenshteinCityNameSimilarityMetric)


def test_haversine_metric():
    config_text = """
        HaversineLocationDistance:
            weight: 20
    """
    assert_right_metric_is_created(config_text, metrics.HaversineLocationDistanceMetric)


def test_log_population_metric():
    config_text = """
        LogarithmicPopulation:
            weight: 20
    """
    assert_right_metric_is_created(config_text, metrics.LogarithmicPopulationMetric)


