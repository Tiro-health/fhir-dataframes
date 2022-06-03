from typing import List, Literal, TypedDict
from fhir_dataframes.sequences import filter_sequences
import pytest_check as check

class Event(TypedDict):
    time: int
    a: Literal["cat", "dog"]
    b: Literal["home" ,"sea", "mountains"]


events:List[Event] = [
    {"time": 0, "a": "cat", "b": "home"},
    {"time": 1, "a": "dog", "b": "sea"},
    {"time": 2, "a": "cat", "b": "mountains"},
    {"time": 3, "a": "cat", "b": "sea"},
    {"time": 4, "a": "dog", "b": "mountains"},
    {"time": 5, "a": "cat", "b": "sea"},
    {"time": 6, "a": "cat", "b": "sea"},
    {"time": 7, "a": "dog", "b": "mountains"},
    {"time": 8, "a": "cat", "b": "sea"},
]


def test_two_events():
    event_match_funcs = [
        lambda r: r["a"] == "cat" and r["b"] == "sea",
        lambda r: r["a"] == "dog" and r["b"] == "mountains",
    ]

    matched_sequences = filter_sequences(events, event_match_funcs)
    check.equal(len(matched_sequences), 2)
    for match in matched_sequences:
        check.equal(match[0]["a"], "cat")
        check.equal(match[0]["b"], "sea")
        check.equal(match[1]["a"], "dog")
        check.equal(match[1]["b"], "mountains")
        check.less(match[0]["time"], match[1]["time"])

def test_three_events():
    event_match_funcs = [
        lambda r: r["a"] == "cat" and r["b"] == "sea",
        lambda r: r["a"] == "dog" and r["b"] == "mountains",
        lambda r: r["a"] == "cat" and r["b"] == "sea",
    ]

    matched_sequences = filter_sequences(events, event_match_funcs)
    check.equal(len(matched_sequences), 2)
    for match in matched_sequences:
        check.equal(match[0]["a"], "cat")
        check.equal(match[0]["b"], "sea")
        check.equal(match[1]["a"], "dog")
        check.equal(match[1]["b"], "mountains")
        check.equal(match[2]["a"], "cat")
        check.equal(match[2]["b"], "sea")

        check.less(match[0]["time"], match[1]["time"])        
        check.less(match[1]["time"], match[2]["time"])        



    
