
from own_framework import *
from aggregation import aggregate_mt_quality
from langgraph.graph import START, END
import json

graph = StateGraph(MTState)

# --- Super-category Stage 1 nodes ---
graph.add_node("semantic_equivalent_stage1_node", semantic_equivalent_agent)
graph.add_node("semantic_contradiction_stage1_node", semantic_contradiction_agent)
graph.add_node("grammatical_morphological_distortion_stage1_node", grammatical_morphological_distortion_agent)
graph.add_node("information_completeness_stage1_node", information_completeness_agent)

# --- Sub-category Stage 2 nodes ---
graph.add_node("Identical_node", Identical_agent)
graph.add_node("Word_synm_node", Word_synm_agent)
graph.add_node("Fluent_node", Fluent_agent)
graph.add_node("Mixd_lang_node", Mixd_lang_agent)
graph.add_node("Negt_anto_node", Negt_anto_agent)
graph.add_node("Default_similar_node", Default_similar_agent)

graph.add_node("Anto_flip_node", Anto_flip_agent)
graph.add_node("Negt_flip_node", Negt_flip_agent)
graph.add_node("Word_rplc_node", Word_rplc_agent)
graph.add_node("Neutral_node", Neutral_agent)
graph.add_node("Default_dissimilar_node", Default_dissimilar_agent)

graph.add_node("Gend_flip_node", Gend_flip_agent)
graph.add_node("Sing_plul_node", Sing_plul_agent)
graph.add_node("Tens_chng_node", Tens_chng_agent)
graph.add_node("Word_ordr_node", Word_ordr_agent)

graph.add_node("Add_extra_node", Add_extra_agent)
graph.add_node("Omission_node", Omission_agent)

# --- Stage 3 cross-verification nodes ---
graph.add_node("semantic_equivalent_stage3_node", semantic_equivalent_stage3_agent)
graph.add_node("semantic_contradiction_stage3_node", semantic_contradiction_stage3_agent)
graph.add_node("grammatical_morphological_distortion_stage3_node", grammatical_morphological_distortion_stage3_agent)
graph.add_node("information_completeness_stage3_node", information_completeness_stage3_agent)

# --- Aggregation node ---
graph.add_node("aggregation_node", aggregate_mt_quality)

# --- Edges ---
graph.add_edge(START, "semantic_equivalent_stage1_node")
graph.add_edge(START, "semantic_contradiction_stage1_node")
graph.add_edge(START, "grammatical_morphological_distortion_stage1_node")
graph.add_edge(START, "information_completeness_stage1_node")

# Semantic Equivalent sub-categories
graph.add_edge("semantic_equivalent_stage1_node", "Identical_node")
graph.add_edge("semantic_equivalent_stage1_node", "Word_synm_node")
graph.add_edge("semantic_equivalent_stage1_node", "Fluent_node")
graph.add_edge("semantic_equivalent_stage1_node", "Mixd_lang_node")
graph.add_edge("semantic_equivalent_stage1_node", "Negt_anto_node")
graph.add_edge("semantic_equivalent_stage1_node", "Default_similar_node")

# Semantic Contradiction sub-categories
graph.add_edge("semantic_contradiction_stage1_node", "Anto_flip_node")
graph.add_edge("semantic_contradiction_stage1_node", "Negt_flip_node")
graph.add_edge("semantic_contradiction_stage1_node", "Word_rplc_node")
graph.add_edge("semantic_contradiction_stage1_node", "Neutral_node")
graph.add_edge("semantic_contradiction_stage1_node", "Default_dissimilar_node")

# Grammatical/Morphological Distortion sub-categories
graph.add_edge("grammatical_morphological_distortion_stage1_node", "Gend_flip_node")
graph.add_edge("grammatical_morphological_distortion_stage1_node", "Sing_plul_node")
graph.add_edge("grammatical_morphological_distortion_stage1_node", "Tens_chng_node")
graph.add_edge("grammatical_morphological_distortion_stage1_node", "Word_ordr_node")

# Information Completeness sub-categories
graph.add_edge("information_completeness_stage1_node", "Add_extra_node")
graph.add_edge("information_completeness_stage1_node", "Omission_node")

# Stage 3 cross-verification
graph.add_edge("Identical_node", "semantic_equivalent_stage3_node")
graph.add_edge("Word_synm_node", "semantic_equivalent_stage3_node")
graph.add_edge("Fluent_node", "semantic_equivalent_stage3_node")
graph.add_edge("Mixd_lang_node", "semantic_equivalent_stage3_node")
graph.add_edge("Negt_anto_node", "semantic_equivalent_stage3_node")
graph.add_edge("Default_similar_node", "semantic_equivalent_stage3_node")

graph.add_edge("Anto_flip_node", "semantic_contradiction_stage3_node")
graph.add_edge("Negt_flip_node", "semantic_contradiction_stage3_node")
graph.add_edge("Word_rplc_node", "semantic_contradiction_stage3_node")
graph.add_edge("Neutral_node", "semantic_contradiction_stage3_node")
graph.add_edge("Default_dissimilar_node", "semantic_contradiction_stage3_node")

graph.add_edge("Gend_flip_node", "grammatical_morphological_distortion_stage3_node")
graph.add_edge("Sing_plul_node", "grammatical_morphological_distortion_stage3_node")
graph.add_edge("Tens_chng_node", "grammatical_morphological_distortion_stage3_node")
graph.add_edge("Word_ordr_node", "grammatical_morphological_distortion_stage3_node")

graph.add_edge("Add_extra_node", "information_completeness_stage3_node")
graph.add_edge("Omission_node", "information_completeness_stage3_node")

# Aggregation
graph.add_edge("semantic_equivalent_stage3_node", "aggregation_node")
graph.add_edge("semantic_contradiction_stage3_node", "aggregation_node")
graph.add_edge("grammatical_morphological_distortion_stage3_node", "aggregation_node")
graph.add_edge("information_completeness_stage3_node", "aggregation_node")

graph.add_edge("aggregation_node", END)

app = graph.compile()

def serialize_state(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    elif isinstance(obj, dict):
        return {k: serialize_state(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_state(v) for v in obj]
    else:
        return obj

if __name__ == "__main__":
    intput_state = {
        "source": "The qualities that determine a subculture as distinct may be linguistic, aesthetic, religious, political, sexual, geographical, or a combination of factors.",
        "mt": "वे गुण जो किसी उप-संस्कृति को अलग बनाते हैं, जैसे कि भाषा, सौंदर्य, धर्म, राजनीति, यौन, भूगोल या कई सारे कारकों का मिश्रण हो सकते हैं.",
        "reference": "उपसंस्कृति को विशिष्ट रूप से निर्धारित करने वाले गुण भाषाई, सौंदर्य, धार्मिक, राजनीतिक, यौन, भौगोलिक या कारकों का संयोजन हो सकते हैं।",
    }

    result = app.invoke(intput_state)

    serialized_result = serialize_state(result)

    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(serialized_result, f, indent=4, ensure_ascii=False)

    print("Saved to result.json")