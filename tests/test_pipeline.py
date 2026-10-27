
import pandas as pd
import pytest

import pipeline


def test_pipeline_stops_if_extraction_fails(monkeypatch):
    def fake_fetch_weather(latitude, longitude):
        raise RuntimeError("Simulated API failure")

    def fail_if_called(*args, **kwargs):
        pytest.fail("Pipeline continued after extraction failed")

    monkeypatch.setattr(
        pipeline,
        "fetch_weather",
        fake_fetch_weather,
    )
    monkeypatch.setattr(
        pipeline,
        "transform_weather",
        fail_if_called,
    )
    monkeypatch.setattr(
        pipeline,
        "validate_weather_data",
        fail_if_called,
    )
    monkeypatch.setattr(
        pipeline,
        "load_weather_data",
        fail_if_called,
    )

    with pytest.raises(RuntimeError, match="Simulated API failure"):
        pipeline.run_pipeline(
            latitude=28.6139,
            longitude=77.2090,
            city="Delhi",
            country="India",
        )


def test_pipeline_stops_if_validation_fails(monkeypatch):
    sample_df = pd.DataFrame({"city": ["Delhi"]})

    monkeypatch.setattr(
        pipeline,
        "fetch_weather",
        lambda latitude, longitude: {"sample": "data"},
    )
    monkeypatch.setattr(
        pipeline,
        "transform_weather",
        lambda raw_data, city_name: sample_df,
    )
    monkeypatch.setattr(
        pipeline,
        "validate_weather_data",
        lambda df: ["Simulated validation failure"],
    )

    def fail_if_called(*args, **kwargs):
        pytest.fail("Database loader called despite validation failure")

    monkeypatch.setattr(
        pipeline,
        "load_weather_data",
        fail_if_called,
    )

    with pytest.raises(ValueError, match="validation failed"):
        pipeline.run_pipeline(
            latitude=28.6139,
            longitude=77.2090,
            city="Delhi",
            country="India",
        )
