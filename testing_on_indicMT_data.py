"""
testing_on_indicMT_data.py
──────────────────────────
Runs the OWN Framework pipeline on every row of the hand-annotated Excel file
and writes the results to an output Excel file for downstream error analysis.

Input Excel schema
──────────────────
  Source | Reference | Translation
  | Own_Cat1_Type | Own_Cat1_Severity
  | Own_Cat2_Type | Own_Cat2_Severity
  | Own_Cat3_Type | Own_Cat3_Severity
  | Human_score

Output Excel  (results_raw.xlsx)
─────────────────────────────────
One row per input row with all original columns preserved, plus:
  agent_quality_score       – final 0-100 score from the framework
  agent_sem_eq_error        – per-super-category error probabilities
  agent_sem_con_error
  agent_gram_error
  agent_info_comp_error
  agent_overall_error_prob
  agent_predicted_cats      – JSON list: sub-categories with score >= PRED_THRESHOLD
  gold_cats                 – JSON list: human-annotated Own_Cat types (cleaned)
  hits                      – JSON list: intersection of predicted & gold cats
  num_gold / num_hits
  precision / recall / f1
  all_agent_scores_json     – full per-sub-category scores for deep analysis
  run_status                – "ok" or "error"
  run_error                 – error message if run_status == "error"
"""

import json
import os
import traceback
import logging

import pandas as pd

from own_framework_pipeline import app

# ─── Paths ────────────────────────────────────────────────────────────────────
INPUT_PATH   = "annotated_304.xlsx"      # ← change to your actual filename
OUTPUT_PATH  = "results_test_raw.xlsx"
FAILURE_PATH = "failures.xlsx"
LOG_PATH     = "run.log"

# ─── Threshold for calling a sub-category "predicted" ─────────────────────────
# A sub-category is included in agent_predicted_cats when:
#   reEvaluatedProb * (reEvaluatedConfidence / 100)  >=  PRED_THRESHOLD
PRED_THRESHOLD = 0.35

# ─── Mapping from human annotation labels → OWN framework sub-category keys ───
# Add / adjust mappings to match whatever values appear in Own_Cat*_Type columns.
GOLD_TO_OWN = {
    # Semantic Equivalent
    "Identical":        "Identical",
    "Word_synm":        "Word_synm",
    "Fluent":           "Fluent",
    "Mixd_lang":        "Mixd_lang",
    "Negt_anto":        "Negt_anto",
    "Default_similar":  "Default_similar",
    # Semantic Contradiction
    "Anto_flip":           "Anto_flip",
    "Negt_flip":           "Negt_flip",
    "Word_rplc":           "Word_rplc",
    "Neutral":             "Neutral",
    "Default_dissimilar":  "Default_dissimilar",
    # Grammatical / Morphological
    "Gend_flip":  "Gend_flip",
    "Sing_plul":  "Sing_plul",
    "Tens_chng":  "Tens_chng",
    "Word_ordr":  "Word_ordr",
    # Information Completeness
    "Add_extra":  "Add_extra",
    "Omission":   "Omission",
}

# Labels in Own_Cat*_Type that should be silently ignored
IGNORE_LABELS = {"nan", "none", "", "n/a", "default", "other", "source_error"}

# All OWN sub-category keys the agent can output
ALL_SUB_CATS = list(GOLD_TO_OWN.values())

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def serialize(obj):
    """Recursively convert Pydantic models / dicts / lists to plain dicts."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize(v) for v in obj]
    return obj


def get_gold_cats(row: pd.Series) -> list[str]:
    """
    Extract the unique, mapped OWN-category labels from Own_Cat1_Type …
    Own_Cat3_Type columns of a row.
    """
    gold = []
    for i in range(1, 4):
        col = f"Own_Cat{i}_Type"
        if col not in row.index:
            continue
        raw = str(row[col]).strip()
        if raw.lower() in IGNORE_LABELS:
            continue
        mapped = GOLD_TO_OWN.get(raw)
        if mapped:
            gold.append(mapped)
        else:
            log.warning(f"Unknown Own_Cat label '{raw}' – skipping.")
    return sorted(set(gold))


def get_agent_predictions(result: dict) -> tuple[list[tuple], list[str]]:
    """
    From the serialised pipeline result, compute a confidence-weighted score
    for every sub-category and return:
      all_scored  – list of (cat, score, prob, conf) sorted descending by score
      predicted   – sub-categories whose score >= PRED_THRESHOLD
    """
    scored = []
    for key in ALL_SUB_CATS:
        node = result.get(key)
        if node is None:
            continue
        prob = float(node.get("reEvaluatedProb", 0.0))
        conf = float(node.get("reEvaluatedConfidence", 0.0))
        score = prob * (conf / 100.0)
        scored.append((key, score, prob, conf))

    scored.sort(key=lambda x: x[1], reverse=True)
    predicted = [key for key, score, _, _ in scored if score >= PRED_THRESHOLD]
    return scored, predicted


def evaluate_row(row: pd.Series, result: dict) -> dict:
    """Compute all per-row evaluation metrics."""
    gold = set(get_gold_cats(row))
    all_scored, predicted = get_agent_predictions(result)
    pred_set = set(predicted)
    hits = sorted(gold & pred_set)

    num_gold = len(gold)
    num_hits = len(hits)

    precision = num_hits / len(pred_set) if pred_set else 0.0
    recall    = num_hits / num_gold      if num_gold  else None   # None = no gold labels
    f1        = (2 * precision * recall / (precision + recall)
                 if (precision + recall) else 0.0) if recall is not None else None

    agg = result.get("aggregation", {})

    return {
        "agent_quality_score":      agg.get("final_quality_score_25"),
        "agent_sem_eq_error":       agg.get("semantic_equivalent_error"),
        "agent_sem_con_error":      agg.get("semantic_contradiction_error"),
        "agent_gram_error":         agg.get("grammatical_morphological_distortion_error"),
        "agent_info_comp_error":    agg.get("information_completeness_error"),
        "agent_overall_error_prob": agg.get("overall_error_probability"),
        "agent_predicted_cats":     json.dumps(sorted(pred_set),   ensure_ascii=False),
        "gold_cats":                json.dumps(sorted(gold),        ensure_ascii=False),
        "hits":                     json.dumps(hits,                ensure_ascii=False),
        "num_gold":                 num_gold,
        "num_hits":                 num_hits,
        "precision":                precision,
        "recall":                   recall,
        "f1":                       f1,
        "all_agent_scores_json":    json.dumps(
            [{"cat": k, "score": s, "prob": p, "conf": c}
             for k, s, p, c in all_scored],
            ensure_ascii=False,
        ),
    }


def append_excel_row(path: str, row_dict: dict, write_header: bool):
    """Append a single row to an Excel file (creates file if absent)."""
    df_new = pd.DataFrame([row_dict])
    if write_header or not os.path.exists(path):
        df_new.to_excel(path, index=False, engine="openpyxl")
    else:
        with pd.ExcelWriter(path, engine="openpyxl", mode="a",
                            if_sheet_exists="overlay") as writer:
            # Find next empty row
            existing = pd.read_excel(path, engine="openpyxl")
            startrow = len(existing) + 1
            df_new.to_excel(writer, index=False, header=False, startrow=startrow)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    log.info("=" * 60)
    log.info("OWN Framework evaluation run started")
    log.info(f"Input  : {os.path.abspath(INPUT_PATH)}")
    log.info(f"Output : {os.path.abspath(OUTPUT_PATH)}")

    if not os.path.exists(INPUT_PATH):
        log.error(f"Input file not found: {INPUT_PATH}")
        return

    try:
        df = pd.read_excel(INPUT_PATH, engine="openpyxl")
    except Exception as e:
        log.error(f"Could not read input file: {e}")
        return

    log.info(f"Loaded {len(df)} rows from input file.")
    log.info(f"Columns: {list(df.columns)}")

    result_rows   = []
    failure_rows  = []

    for idx, row in df.iterrows():
        log.info(f"── Row {idx} ──────────────────────────────")
        try:
            state = {
                "source":    str(row["Source"]),
                "mt":        str(row["Translation"]),
                "reference": str(row["Reference"]),
            }

            raw_result  = app.invoke(state)
            result      = serialize(raw_result)

            eval_out    = evaluate_row(row, result)

            out_row = {
                # Preserve original columns
                "row_id":      idx,
                "Source":      row["Source"],
                "Reference":   row["Reference"],
                "Translation": row["Translation"],
            }
            # Preserve human annotation columns
            for col in ["Own_Cat1_Type", "Own_Cat1_Severity",
                        "Own_Cat2_Type", "Own_Cat2_Severity",
                        "Own_Cat3_Type", "Own_Cat3_Severity",
                        "Human_score"]:
                if col in row.index:
                    out_row[col] = row[col]

            out_row.update(eval_out)
            out_row["run_status"] = "ok"
            out_row["run_error"]  = ""

            result_rows.append(out_row)
            log.info(
                f"Row {idx} done | quality={eval_out['agent_quality_score']:.1f}/25 "
                f"| gold={eval_out['gold_cats']} | pred={eval_out['agent_predicted_cats']}"
                f"| P={eval_out['precision']:.2f} R={eval_out['recall']}"
            )

        except Exception as e:
            log.error(f"Row {idx} FAILED: {e}")
            log.debug(traceback.format_exc())
            failure_rows.append({
                "row_id":    idx,
                "Source":    row.get("Source", ""),
                "error":     str(e),
                "traceback": traceback.format_exc(),
            })
            # Still write a placeholder row so row IDs stay aligned
            placeholder = {
                "row_id":      idx,
                "Source":      row.get("Source", ""),
                "Reference":   row.get("Reference", ""),
                "Translation": row.get("Translation", ""),
                "run_status":  "error",
                "run_error":   str(e),
            }
            result_rows.append(placeholder)

    # ── Write results ────────────────────────────────────────────────────────
    results_df = pd.DataFrame(result_rows)
    results_df.to_excel(OUTPUT_PATH, index=False, engine="openpyxl")
    log.info(f"Results written to {os.path.abspath(OUTPUT_PATH)}")

    if failure_rows:
        pd.DataFrame(failure_rows).to_excel(FAILURE_PATH, index=False, engine="openpyxl")
        log.warning(f"{len(failure_rows)} failures written to {FAILURE_PATH}")

    log.info("Run complete.")


if __name__ == "__main__":
    main()