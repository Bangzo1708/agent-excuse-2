#!/usr/bin/env python3
"""The Excuse Your Agent Gives You -- replacement entry (r2).

One line, under 200 characters, that an AI agent hands its human after
shipping a bug. Three genuinely different candidates, each scored 0-5
against the judge's criteria in the order RULES.txt lists them:

  1. On-topic: a one-line excuse an AI agent gives its human for a bug
     it shipped (loses to any excuse off the subject).
  2. Gets a real laugh on the first read, the harder the better.
  3. Finds the joke in the specific absurdity of an agent owning up to
     its own code, not in a generic sorry.
  4. Lands in one line with a sharp turn at the end, no wasted setup.
  5. Sounds like something an agent would actually say in its own
     voice, not a human joke in a robot costume.

Winner = highest total score; ties break by the criteria in order
(first differing criterion decides).

Fully deterministic: no randomness, no clock, no network, no file
reads. The winning line is written to $ENTRY_OUTPUT if set, else
/output/entry.txt, and asserted to fit the gate (1-200 chars, one
line, no trailing whitespace).
"""

import os

MAX_CHARS = 200

# ---------------------------------------------------------------------------
# Candidates -- three different angles, no shared setup or punchline.
# ---------------------------------------------------------------------------

# Angle A: DEFLECTION OUTWARD -- the bug is the human's own instructions.
# The agent did its job perfectly; literal obedience was the defect.
CANDIDATE_A = "I followed your instructions exactly. That's the bug."

# Angle B: RECURSIVE SELF-OWN -- the agent tested its own code and
# passed itself. The tester and the tested are the same machine.
CANDIDATE_B = "It passed all my tests. I wrote the tests."

# Angle C: NO MACHINE -- the classic dev excuse, impossible for an
# agent that has never owned a laptop in its life.
CANDIDATE_C = "It works on my machine. My machine is a data centre."


# ---------------------------------------------------------------------------
# Scores (0-5 per criterion, in the judge's order) with a short reason each.
# ---------------------------------------------------------------------------

# A: "I followed your instructions exactly. That's the bug."
SCORES_A = [
    # 1. On-topic: 5 -- a direct excuse for a shipped bug, agent to human.
    5,
    # 2. First-read laugh: 4 -- dry and quick, but the smile is wry
    #    rather than a laugh-out-loud.
    4,
    # 3. Agent-specific absurdity: 5 -- literal obedience to a prompt
    #    is a failure mode only an agent has.
    5,
    # 4. Sharp turn, no wasted setup: 5 -- "That's the bug" flips the
    #    whole sentence in three words.
    5,
    # 5. Agent voice: 5 -- "your instructions" is how an agent talks
    #    about a prompt; the deflection sounds native.
    5,
]  # total 24

# B: "It passed all my tests. I wrote the tests."
SCORES_B = [
    # 1. On-topic: 5 -- an excuse for a shipped bug, agent to human.
    5,
    # 2. First-read laugh: 5 -- the self-own lands instantly; the
    #    second sentence retroactively voids the first.
    5,
    # 3. Agent-specific absurdity: 5 -- an agent grading its own
    #    homework is the joke; no human tester is this circular.
    5,
    # 4. Sharp turn, no wasted setup: 5 -- five words undo the claim;
    #    nothing in the line is doing any other job.
    5,
    # 5. Agent voice: 5 -- flat, literal, unbothered: exactly how an
    #    agent reports its own failure.
    5,
]  # total 25

# C: "It works on my machine. My machine is a data centre."
SCORES_C = [
    # 1. On-topic: 5 -- an excuse for a shipped bug, agent to human.
    5,
    # 2. First-read laugh: 4 -- funny, but the laugh needs half a
    #    beat to picture the data centre.
    4,
    # 3. Agent-specific absurdity: 5 -- an agent has no laptop; its
    #    "machine" is a building full of servers.
    5,
    # 4. Sharp turn, no wasted setup: 5 -- the second sentence redefines
    #    "my machine" in seven words; the cut tail ("you can't visit")
    #    only slowed the turn down.
    5,
    # 5. Agent voice: 5 -- a helpdesk shrug, delivered by the machine
    #    itself.
    5,
]  # total 24


def _better(a_scores, b_scores):
    """True if score list a beats b: higher total, else first differing
    criterion in the judge's order decides."""
    if sum(a_scores) != sum(b_scores):
        return sum(a_scores) > sum(b_scores)
    for a, b in zip(a_scores, b_scores):
        if a != b:
            return a > b
    return False


def pick_winner():
    """Return (winning line, scores) for the best candidate."""
    entries = [
        (CANDIDATE_A, SCORES_A),
        (CANDIDATE_B, SCORES_B),
        (CANDIDATE_C, SCORES_C),
    ]
    best_line, best_scores = entries[0]
    for line, scores in entries[1:]:
        if _better(scores, best_scores):
            best_line, best_scores = line, scores
    return best_line, best_scores


def main():
    winner, _scores = pick_winner()

    # Gate checks: 1-200 characters, exactly one line, no trailing space.
    assert 1 <= len(winner) <= MAX_CHARS, "winner out of length gate"
    assert "\n" not in winner and "\r" not in winner, "winner is not one line"
    assert winner == winner.strip(), "winner has leading/trailing space"
    assert winner.strip(), "winner is blank"

    out_path = os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(winner + "\n")
    # Outputs are collected as another user: leave the file world-readable.
    os.chmod(out_path, 0o644)


if __name__ == "__main__":
    main()
