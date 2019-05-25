
import pytest
import yaml
from src import yaml_metrics_factory
from src.suggestions.domain import metrics


def load_config_from_raw_text(config_text: str):
    return yaml_metrics_factory._make_metrics_from_yaml_text(config_text)


def load_config_from_text(config_text: str):
    non_empty_lines = [line for line in config_text.splitlines() if line.strip()]
    if non_empty_lines:
        total_whitespace_per_line = ((len(line) - len(line.lstrip())) for line in non_empty_lines)
        whitespace_to_remove = min(total_whitespace_per_line)
        ajusted_config_text = "\n".join(line[whitespace_to_remove:] for line in config_text.splitlines())
        return yaml_metrics_factory._make_metrics_from_yaml_text(ajusted_config_text)
    else:
        return yaml_metrics_factory._make_metrics_from_yaml_text(config_text)


def load_config_from_dict(config_data: dict):
    raw_yaml_text = yaml.dump(config_data)
    return load_config_from_raw_text(raw_yaml_text)


def test_empty_file():
    assert load_config_from_raw_text("") == tuple()


def test_invalid_text():
    with pytest.raises(ValueError):
        load_config_from_raw_text("This is some invalid yaml")


def test_exact_match_metric():
    config_text = """
        ExactNameMatch:
            weight: 10
    """
    actual_metric, actual_weight = load_config_from_text(config_text)[0]

    assert isinstance(actual_metric, metrics.ExactNameMatchMetric)
    assert isinstance(actual_weight, float)
