"""Starter tests for the weather module.

These tests deliberately cover only ordinary examples. They show how pytest works,
but they are not a sufficient test suite for the specification in SPECIFICATION.md.
"""
import pytest
from weather import (
    average_temperature,
    filter_by_temperature,
    hottest_measurement,
    parse_measurement,
    parse_time,
)


def test_parse_time_regular_time():
    assert parse_time("14:21") == 861


def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)


def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]


def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0


def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)



def test_parse_time_edge_cases():
    assert parse_time("00:00") == 0
    assert parse_time("23:59") == 1439


def test_parse_time_special_time():
    with pytest.raises(ValueError, match="Time must have HH:MM format"):
        parse_time("23::05")
    with pytest.raises(ValueError, match="Minute must be between 0 and 59"):
        parse_time("12:80")
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        parse_time("-23:12")
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        parse_time("23:-12")
    with pytest.raises(ValueError, match="Hour must be between 0 and 23."):
        parse_time("24:45")
    with pytest.raises(ValueError, match="Minute must be between 0 and 59"):
        parse_time("23:60")


def test_parse_measurement_separator():
    with pytest.raises(ValueError, match="Expected exactly three fields."):
        parse_measurement("Berlin;;04:23;;12.8")

def test_parse_measurement_blank():
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        parse_measurement("Düsseldorf;2 3:49; 3 1.5")
    with pytest.raises(ValueError, match="City must not be empty."):
        parse_measurement(" ;12:51; 13.4")


def test_parse_measurement_convert():
    with pytest.raises(ValueError, match="Temperature must be numeric."):
        parse_measurement("Essen;08:34;gulasch")


def test_filter_by_temperature():
    with pytest.raises(ValueError, match="lower must not be greater than upper."):
        filter_by_temperature(23, 34, 2)

def test_filter_temperature_order():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert filter_by_temperature(measurements, 10, 20) == [("Köln", 600, 10.0), ("Bonn", 900, 20.0)]


def test_filter_temperature_doubles():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 600, 10.0),
        ("Bonn", 900, 20.0),
    ]

    assert filter_by_temperature(measurements, 10, 20) == [("Köln", 600, 10.0),
        ("Köln", 600, 10.0),
        ("Bonn", 900, 20.0)]


def test_filter_temperature_type():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert isinstance(filter_by_temperature(measurements, 10, 25), list) == True


def test_average_temperature_case_sensitivity():
    with pytest.raises(ValueError, match="No measurements found for city."):
        average_temperature([("Köln", 600, 25.0)], "köln")


def test_averagde_temperature_mean():
    measurements = [
        ("Köln", 600, 10.0),
        ("Berlin", 720, 25.0),
        ("Köln", 900, 20.0),
    ]
    assert average_temperature(measurements, "Köln") == (10  + 20) / 2


def test_hottest_measurement_occurrence():
    measurements = [
        ("Köln", 600, 25.0),
        ("Düsseldorf", 600, 25.0),
        ("Bonn", 900, 25.0),
    ]

    assert hottest_measurement(measurements) == ("Köln", 600, 25.0)
    assert hottest_measurement(measurements) == ("Köln", 600, 25.0)


def test_hottest_measurement_blank():
    measurements = []
    with pytest.raises(ValueError, match="No measurements available."):
        hottest_measurement(measurements)


def test_hottest_measurement_latest():
    measurements = [
        ("Köln", 600, 25.0),
        ("Düsseldorf", 500, 25.0),
        ("Bonn", 900, 25.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 500, 25.0)