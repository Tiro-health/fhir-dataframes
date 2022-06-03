from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union
import pandas as pd

Record = Dict[str, Any]
EventMatchFunc = Callable[[Record], bool]
EventSequence = Tuple[Record, ...]

def filter_sequences(
    events: Iterable[Record],
    event_match_funcs: Sequence[Callable[[Record], bool]],
    include_incomplete=False,
):
    """Filter sequences of events (records) based on a set of boolean test criteria. The resulting sequences contain events that match the test criteria in order.

    ## General idea of the algorithm

    We are looking for a sequence with ordered target events.
    Each target event that we're search for is described by a function that receives a record and returns a boolean value indicating a match or not.
    We start by building a 'state' dictionary containing an entry for each target event plus a dummy start entry. 
    So the number of key-value pairs in the dictionary equals the length of the sequence we are searching for plus one.

    ex. 
    
    Let's say we are searching for three events then our state dict is initialized as

    ```python
    state = {
        -1: tuple(),
        0: None,
        1: None,
        2: None,
    }
    ```

    By iterating through all events in order, we will gradually build candidate sequences. These candidate sequences are stored in the state dict. 
    Each state dict can contain at most one candidate sequence.

    For each event in the events iterable, we evaluate wether it is a match with one of the target events or not. 
    The first match with the first target_event will result in extending the empty tuple with this first matching event. 
    This tuple is our first candidate sequence and is stored inside the state dictionary at key = 0.
    Next matching event we'll check if it is the first target event of our sequence or if all other previous target_events are already available in our candidate sequence. 
    If that is the case, we can extend the candidate sequence with one more target event and store it in the next entry of our state dictionary. 
    
    """
    
    # the number of event_matc_funcs deterimine
    seq_length = len(event_match_funcs)
    seq_matches: List[Tuple[Record, ...]] = list()

    # we'll use a dict as a state machine to build the sequences
    states: Dict[int, Optional[EventSequence]] = {
        i: None for i in range(seq_length)
    }
    # the -1 state is the start of an empty candidate sequence (represented by an empty tuple)
    states[-1] = tuple()
    
    event_match_iter = (tuple(f(event) for f in event_match_funcs) for event in events) 


    # iterate over all events
    for event_dict, event_matches in zip(events, event_match_iter):
        # check whether the current record matches the expected event
        for event_index, event_is_a_match in enumerate(event_matches):

            # check wether a we have a match for an event and
            # check wether a candidate sequence with all previous events is available
            prev_state = states[event_index - 1] # note that key = -1 => empty tuple()
            candidate_sequence_is_available = prev_state is not None 
            if event_is_a_match and candidate_sequence_is_available:

                # if there was an existing candidate sequence under construction 
                # that hasn't got futher than event_index, either append it (if include_incomplete == True)
                # or discard it completly by overwriting it 
                seq = states[event_index]
                sequence_is_complete = event_index == seq_length - 1

                if seq is not None and (include_incomplete or sequence_is_complete):
                    # add unfininished sequence before overwriting with new sequence candidate
                    seq_matches.append(seq)

                assert prev_state is not None # mypy doesn't reallize that prev_state can't be None
                states[event_index] = prev_state + (event_dict,)  # add current event to candidate sequence and pass the sequence to next state
                states[event_index - 1] = (
                    None if event_index > 0 else tuple()
                )  # the state at -1 should always be ready

    # gather the remaining sequences in the state machine
    for state_index, seq in states.items():
        if (include_incomplete or state_index == seq_length - 1) and seq:
            seq_matches.append(seq)
    return seq_matches



