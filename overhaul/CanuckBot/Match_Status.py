from enum import IntEnum


class Match_Status(IntEnum):
    Pending = 0     # Match in scheduled but not yet reached match's hours_before_kickoff
    Ready = 1       # We reached match's hours_before_kickoff, channel should be created
    Active = 2      # Match in progress
    Completed = 3   # Match reached match's hours_after_kickoff, time to cleanup
