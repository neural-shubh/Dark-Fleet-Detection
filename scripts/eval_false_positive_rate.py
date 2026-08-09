"""
False-positive rate check on known-legitimate vessel traffic (issue #2).

The model's reported numbers so far come from labeled dark-fleet cases
(recall-side). This script is the other half: run the trained
CNN+LSTM/RNN fusion model on a held-out sample of KNOWN LEGITIMATE
vessels (normal AIS-transmitting traffic, not flagged as dark) and
report how often it wrongly fires an anomaly flag.

This is a template, not a finished result — it doesn't ship any numbers.
Point LEGIT_VESSEL_DATA_PATH at your held-out legitimate-traffic sample
(same format the training/eval pipeline in the notebook already uses)
and MODEL_PATH at the trained model, then run it.

Usage:
    python scripts/eval_false_positive_rate.py \
        --model models/dark_fleet_fusion_model.<ext> \
        --legit-data data/legit_vessel_holdout.<ext> \
        --threshold 0.5
"""

import argparse
import json


def compute_false_positive_rate(y_true_legit, y_pred_scores, threshold=0.5):
    """
    y_true_legit  : iterable, all entries should be legitimate (label 0)
                    vessels — this function assumes the whole input set
                    is known-legit, so every positive prediction is a
                    false positive by construction.
    y_pred_scores : model's anomaly probability/score per vessel-track,
                    same order as y_true_legit
    threshold     : score above which the model flags "dark fleet"

    Returns a dict with the FP rate and supporting counts, ready to
    drop into the README's results table.
    """
    if len(y_true_legit) != len(y_pred_scores):
        raise ValueError("y_true_legit and y_pred_scores must be the same length")
    if len(y_pred_scores) == 0:
        raise ValueError("Need at least one held-out legitimate-vessel sample")

    false_positives = sum(1 for score in y_pred_scores if score >= threshold)
    total = len(y_pred_scores)

    return {
        "threshold": threshold,
        "total_legit_vessels_checked": total,
        "false_positives": false_positives,
        "false_positive_rate": false_positives / total,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Path to trained fusion model")
    parser.add_argument("--legit-data", required=True,
                         help="Path to held-out known-legitimate vessel dataset")
    parser.add_argument("--threshold", type=float, default=0.5,
                         help="Anomaly score threshold used for flagging (match training config)")
    args = parser.parse_args()

    # NOTE: wire these up to however the notebook currently loads the model
    # and builds vessel-track feature sequences for the LSTM/RNN branch.
    # Left unimplemented here since that depends on the notebook's exact
    # preprocessing (kept out of this script to avoid guessing at it).
    raise NotImplementedError(
        "Plug in model loading + inference here, matching the notebook's "
        "existing prediction pipeline, then call compute_false_positive_rate()."
    )


if __name__ == "__main__":
    main()
