from typing import List, Literal, TypedDict
from fhir_dataframes.sequences import filter_sequences
import pytest_check as check

class Event(TypedDict):
    time: int
    pet: Literal["cat", "dog"]
    location: Literal["home" ,"sea", "mountains"]


events:List[Event] = [
    {"time": 0, "pet": "cat", "location": "home"},
    {"time": 1, "pet": "dog", "location": "sea"},
    {"time": 2, "pet": "cat", "location": "mountains"},
    {"time": 3, "pet": "cat", "location": "sea"},
    {"time": 4, "pet": "dog", "location": "mountains"},
    {"time": 5, "pet": "cat", "location": "sea"},
    {"time": 6, "pet": "cat", "location": "sea"},
    {"time": 7, "pet": "cat", "location": "mountains"},
    {"time": 8, "pet": "dog", "location": "mountains"},
    {"time": 9, "pet": "cat", "location": "sea"},
    {"time": 10, "pet": "dog", "location": "sea"},
]


def test_two_events():
    event_match_funcs = [
        lambda r: r["pet"] == "cat" and r["location"] == "sea",
        lambda r: r["pet"] == "dog" and r["location"] == "mountains",
    ]

    matched_sequences = filter_sequences(events, event_match_funcs)
    check.equal(len(matched_sequences), 2)
    for match in matched_sequences:
        check.equal(match[0]["pet"], "cat")
        check.equal(match[0]["location"], "sea")
        check.equal(match[1]["pet"], "dog")
        check.equal(match[1]["location"], "mountains")
        check.less(match[0]["time"], match[1]["time"])

def test_three_events():
    event_match_funcs = [
        lambda r: r["pet"] == "cat" and r["location"] == "sea",
        lambda r: r["pet"] == "dog" and r["location"] == "mountains",
        lambda r: r["pet"] == "cat" and r["location"] == "sea",
    ]

    matched_sequences = filter_sequences(events, event_match_funcs)
    check.equal(len(matched_sequences), 2)
    for match in matched_sequences:
        check.equal(match[0]["pet"], "cat")
        check.equal(match[0]["location"], "sea")
        check.equal(match[1]["pet"], "dog")
        check.equal(match[1]["location"], "mountains")
        check.equal(match[2]["pet"], "cat")
        check.equal(match[2]["location"], "sea")

        check.less(match[0]["time"], match[1]["time"])        
        check.less(match[1]["time"], match[2]["time"])        


def test_three_events_grouped_by():
    event_match_funcs = [
        lambda r: r["location"] == "sea",
        lambda r: r["location"] == "mountains",
        lambda r: r["location"] == "sea",
    ]

    matched_sequences = filter_sequences(events, event_match_funcs, by="pet")
    check.equal(len(matched_sequences), 2)
    for match in matched_sequences:
        check.equal(match[0]["location"], "sea")
        check.equal(match[1]["location"], "mountains")
        check.equal(match[2]["location"], "sea")

        check.less(match[0]["time"], match[1]["time"])        
        check.less(match[1]["time"], match[2]["time"])   



    
