"""
Compare a KRROOD-only rerun of the agent loop with the stored results of run ae0b139a: per seed and step, KRROOD's
own action and its candidates digest against those of each stored variant, and the medians of KRROOD's counters.

Usage: python compare_krrood_rerun.py <stored results_agentloop dir> <rerun dir with seed0..seed4/agent_loop_krrood.json>
"""

from __future__ import annotations

import json
import statistics
import sys
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Dict, List


class StepField(StrEnum):
    """
    The fields of a step record that the comparison reads.
    """

    STEPS = "steps"
    ACTION = "action"
    DIGEST = "candidates_digest"
    TOTAL_SECONDS = "total_seconds"
    PROCEDURE_CALLS = "procedure_calls"


STORED_VARIANTS = ("graphdb", "graphdb_push", "krrood")
"""
The stored variants of every seed that the rerun is compared with (KRROOD's own earlier run included).
"""

SEEDS = range(5)


@dataclass
class SeedComparison:
    """
    The differences between the rerun's KRROOD steps and one stored variant's steps of one seed.
    """

    seed: int
    variant: str
    steps: int
    differing_actions: int
    differing_digests: int


def stored_file(stored: Path, seed: int, variant: str) -> Path:
    """
    :return: The stored step file of a variant; seed 0 is at the top level, the others under ``seeds/``.
    """
    directory = stored if seed == 0 else stored / "seeds" / f"seed{seed}"
    return directory / f"agent_loop_{variant}.json"


def steps_of(path: Path) -> List[Dict[str, Any]]:
    """
    :return: The step records of a variant's result file.
    """
    return json.loads(path.read_text())[StepField.STEPS]


def compare(rerun: List[Dict[str, Any]], stored: List[Dict[str, Any]], seed: int, variant: str) -> SeedComparison:
    """
    :return: How many steps differ in the action and in the candidates digest.
    """
    assert len(rerun) == len(stored), (seed, variant, len(rerun), len(stored))
    return SeedComparison(
        seed,
        variant,
        len(rerun),
        sum(a[StepField.ACTION] != b[StepField.ACTION] for a, b in zip(rerun, stored)),
        sum(a[StepField.DIGEST] != b[StepField.DIGEST] for a, b in zip(rerun, stored)),
    )


def main(stored: Path, rerun_root: Path) -> None:
    comparisons: List[SeedComparison] = []
    rerun_steps: List[Dict[str, Any]] = []
    for seed in SEEDS:
        rerun = steps_of(rerun_root / f"seed{seed}" / "agent_loop_krrood.json")
        rerun_steps += rerun
        for variant in STORED_VARIANTS:
            path = stored_file(stored, seed, variant)
            if path.exists():
                comparisons.append(compare(rerun, steps_of(path), seed, variant))
    for comparison in comparisons:
        print(comparison)
    calls = sorted({name for step in rerun_steps for name in step[StepField.PROCEDURE_CALLS]})
    summary = {
        "median_step_ms": 1000 * statistics.median(s[StepField.TOTAL_SECONDS] for s in rerun_steps),
        "median_calls_per_step": {
            name: statistics.median(s[StepField.PROCEDURE_CALLS].get(name, 0) for s in rerun_steps) for name in calls
        },
        "all_actions_and_digests_equal": all(
            c.differing_actions == 0 and c.differing_digests == 0 for c in comparisons
        ),
    }
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
