from typing import Dict, List
from own_framework import MTState, AggregationOutput

def weighted_mean(probs: List[float], confs: List[float]) -> float:
    if not probs or not confs:
        return 0.0
    
    weights = [c / 100.0 for c in confs]
    total_weight = sum(weights)

    if total_weight == 0:
        return 0.0
    
    return sum(p * w for p, w in zip(probs, weights)) / total_weight

def aggregate_super_category(state: MTState, sub_keys: List[str], stage3_key: str) -> float:
    probs = []
    confs = []

    for key in sub_keys:
        agent_output = state.get(key)
        if agent_output is not None:
            probs.append(agent_output.reEvaluatedProb)
            confs.append(agent_output.reEvaluatedConfidence)
    
    base_score = weighted_mean(probs, confs)

    stage3 = state.get(stage3_key)

    if stage3 is None:
        return base_score
    
    if stage3.errorsExists == "NO":
        return base_score * 0.3
    
    consistency_factor = stage3.consistencyScore / 100.0
    return base_score * consistency_factor

def aggregate_mt_quality(state: MTState) -> Dict[str, AggregationOutput]:
    # New super-category and sub-category structure
    semantic_equivalent_subs = [
        "Identical", "Word_synm", "Fluent", "Mixd_lang", "Negt_anto", "Default_similar"
    ]
    semantic_contradiction_subs = [
        "Anto_flip", "Negt_flip", "Word_rplc", "Neutral", "Default_dissimilar"
    ]
    grammatical_morphological_distortion_subs = [
        "Gend_flip", "Sing_plul", "Tens_chng", "Word_ordr"
    ]
    information_completeness_subs = [
        "Add_extra", "Omission"
    ]

    sem_eq_score = aggregate_super_category(state, semantic_equivalent_subs, "semantic_equivalent_stage3")
    sem_contr_score = aggregate_super_category(state, semantic_contradiction_subs, "semantic_contradiction_stage3")
    gmd_score = aggregate_super_category(state, grammatical_morphological_distortion_subs, "grammatical_morphological_distortion_stage3")
    info_comp_score = aggregate_super_category(state, information_completeness_subs, "information_completeness_stage3")

    # You can adjust weights as needed
    weights = {
        "semantic_equivalent": 0.25,
        "semantic_contradiction": 0.25,
        "grammatical_morphological_distortion": 0.25,
        "information_completeness": 0.25,
    }

    overall_error_prob = (
        weights["semantic_equivalent"] * sem_eq_score +
        weights["semantic_contradiction"] * sem_contr_score +
        weights["grammatical_morphological_distortion"] * gmd_score +
        weights["information_completeness"] * info_comp_score
    )

    final_quality_score_25 = (1 - overall_error_prob) * 25

    return {"aggregation": {
        "semantic_equivalent_error": sem_eq_score,
        "semantic_contradiction_error": sem_contr_score,
        "grammatical_morphological_distortion_error": gmd_score,
        "information_completeness_error": info_comp_score,
        "overall_error_probability": overall_error_prob,
        "final_quality_score_25": final_quality_score_25
    }}