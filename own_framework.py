from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from typing import TypedDict, Dict, List, Optional, Literal, Annotated, Any
from own_framework_prompts import *
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()

class AgentOutputStage1(BaseModel):
    probability: float = Field(..., description="The probability that the error is present", ge=0.0, le=1.0)
    reason: str = Field(..., description="Explanation pointing to concrete words, phrases, or structures that justify the probability.")
    confidence: float = Field(..., description="Score out of 100 on how confident you are that this error is present in the sentence.", ge=0.0, le=100.0)

class AgentOutputStage2(BaseModel):
    reEvaluatedProb: float = Field(..., description="Based on your evaluation re evaluate the probability while considering the probability given by the previous agent.", ge=0.0, le=1.0)
    thoughtsOnStage1: str = Field(..., description="Based on your evaluations, what are your thoughts on evaluations of the previous agent?")
    reason: str = Field(..., description="Give a brief explanation of your thoughts on the previous agent's evaluations. If you agree of disagree with the previous evaluation give concrete evidence for your specific error.")
    reEvaluatedConfidence: float = Field(..., description="Based on your evaluations score out of 100 on how confident are that this error is present in the sentence and that your thoughts and explanations are valid", ge=0.0, le=100.0)

class AgentOutputStage3(BaseModel):
    consistencyScore: float = Field(..., description="Based on the evaluations of the previous agents, generate a score out of 100 on how consistent the agents are with each other.")
    errorsExists: Literal["NO", "YES"] = Field(..., description="Based on the evaluations of the previous agents i want you to verify whether these errors exists or not. Dont re evaluate. You have to search whether the error flagged by the previous agents exists or not. If it exists then return 'YES' otherwise return 'NO'")
    existanceReasoning: str = Field(..., description="Give brief explanation on your verification of the existance of the errors.")

class AggregationOutput(TypedDict):
    accuracy_error: float
    fluency_error: float
    terminology_error: float
    style_error: float
    overall_error_probability: float
    final_quality_score_100: float


# --- NEW CATEGORY STRUCTURE ---
# Super-categories and their sub-categories
SUPER_CATEGORIES = {
    "semantic_equivalent": [
        "Identical", "Word_synm", "Fluent", "Mixd_lang", "Negt_anto", "Default_similar"
    ],
    "semantic_contradiction": [
        "Anto_flip", "Negt_flip", "Word_rplc", "Neutral", "Default_dissimilar"
    ],
    "grammatical_morphological_distortion": [
        "Gend_flip", "Sing_plul", "Tens_chng", "Word_ordr"
    ],
    "information_completeness": [
        "Add_extra", "Omission"
    ]
}

class MTState(TypedDict):
    source: str
    mt: str
    reference: str

    # Stage 1: Super-category outputs
    semantic_equivalent_stage1: Optional[AgentOutputStage1]
    semantic_contradiction_stage1: Optional[AgentOutputStage1]
    grammatical_morphological_distortion_stage1: Optional[AgentOutputStage1]
    information_completeness_stage1: Optional[AgentOutputStage1]

    # Stage 2: Sub-category outputs
    Identical: Optional[AgentOutputStage2]
    Word_synm: Optional[AgentOutputStage2]
    Fluent: Optional[AgentOutputStage2]
    Mixd_lang: Optional[AgentOutputStage2]
    Negt_anto: Optional[AgentOutputStage2]
    Default_similar: Optional[AgentOutputStage2]

    Anto_flip: Optional[AgentOutputStage2]
    Negt_flip: Optional[AgentOutputStage2]
    Word_rplc: Optional[AgentOutputStage2]
    Neutral: Optional[AgentOutputStage2]
    Default_dissimilar: Optional[AgentOutputStage2]

    Gend_flip: Optional[AgentOutputStage2]
    Sing_plul: Optional[AgentOutputStage2]
    Tens_chng: Optional[AgentOutputStage2]
    Word_ordr: Optional[AgentOutputStage2]

    Add_extra: Optional[AgentOutputStage2]
    Omission: Optional[AgentOutputStage2]

    # Stage 3: Cross-verification for each super-category
    semantic_equivalent_stage3: Optional[AgentOutputStage3]
    semantic_contradiction_stage3: Optional[AgentOutputStage3]
    grammatical_morphological_distortion_stage3: Optional[AgentOutputStage3]
    information_completeness_stage3: Optional[AgentOutputStage3]

    aggregation: Optional[AggregationOutput]


llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

def make_error_agent_stage1(system_prompt: str, state_key: str):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", """
        SOURCE SENTENCE: {source}
         
        MACHINE TRANSLATED SENTENCE: {translated}
         
        REFERENCE SENTENCE: {reference}
        """)
    ])

    chain = prompt_template | llm.with_structured_output(AgentOutputStage1)

    def agent_fn(state: MTState) -> Dict[str, AgentOutputStage1]:
        output = chain.invoke({
            "source": state["source"],
            "translated": state["mt"],
            "reference": state["reference"],
        })

        return {state_key: output}
    return agent_fn

def make_error_agent_stage2(system_prompt: str, state_key: str, SuperCategory: str):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", """
        SOURCE SENTENCE: {source}
         
        MACHINE TRANSLATED SENTENCE: {translated}
         
        REFERENCE SENTENCE: {reference}
        
        PREVIOUS AGENT EVALUATIONS: {previous_agent}
        """)
    ])

    chain = prompt_template | llm.with_structured_output(AgentOutputStage2)

    def agent_fn_stage2(state: MTState) -> Dict[str, AgentOutputStage2]:
        output = chain.invoke({
            "source": state["source"],
            "translated": state["mt"],
            "reference": state["reference"],
            "previous_agent": state[SuperCategory]
        })

        return {state_key: output}
    return agent_fn_stage2

def make_error_agent_stage3(system_prompt: str, state_key: str, SuperCategory: str):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", """
        SOURCE SENTENCE: {source}
         
        MACHINE TRANSLATED SENTENCE: {translated}
         
        REFERENCE SENTENCE: {reference}
        
        SUPER CATEGORY AGENT EVALUATIONS: {previous_agent}
         
        SUB CATEGORY AGENTS EVALUATIONS: {sub_category_agent}
        """)
    ])

    chain = prompt_template | llm.with_structured_output(AgentOutputStage3)

    def agent_fn_stage3(state: MTState) -> Dict[str, AgentOutputStage3]:
        # Define sub-category keys for each super-category
        if SuperCategory == "semantic_equivalent_stage1":
            sub = ["Identical", "Word_synm", "Fluent", "Mixd_lang", "Negt_anto", "Default_similar"]
        elif SuperCategory == "semantic_contradiction_stage1":
            sub = ["Anto_flip", "Negt_flip", "Word_rplc", "Neutral", "Default_dissimilar"]
        elif SuperCategory == "grammatical_morphological_distortion_stage1":
            sub = ["Gend_flip", "Sing_plul", "Tens_chng", "Word_ordr"]
        elif SuperCategory == "information_completeness_stage1":
            sub = ["Add_extra", "Omission"]
        else:
            sub = []

        combined_sub_category = [state[s] for s in sub if state.get(s) is not None]

        output = chain.invoke({
            "source": state["source"],
            "translated": state["mt"],
            "reference": state["reference"],
            "previous_agent": state[SuperCategory],
            "sub_category_agent": combined_sub_category,
        })

        return {state_key: output}
    return agent_fn_stage3



# --- NEW AGENT DEFINITIONS ---
# Stage 1: Super-category agents
semantic_equivalent_agent = make_error_agent_stage1(SEMANTIC_EQUIVALENT_PROMPT, "semantic_equivalent_stage1")
semantic_contradiction_agent = make_error_agent_stage1(SEMANTIC_CONTRADICTION_PROMPT, "semantic_contradiction_stage1")
grammatical_morphological_distortion_agent = make_error_agent_stage1(GRAMMATICAL_MORPHOLOGICAL_DISTORTION_PROMPT, "grammatical_morphological_distortion_stage1")
information_completeness_agent = make_error_agent_stage1(INFORMATION_COMPLETENESS_PROMPT, "information_completeness_stage1")

# Stage 2: Sub-category agents (one for each sub-category)
Identical_agent = make_error_agent_stage2(IDENTICAL_PROMPT, "Identical", "semantic_equivalent_stage1")
Word_synm_agent = make_error_agent_stage2(WORD_SYNM_PROMPT, "Word_synm", "semantic_equivalent_stage1")
Fluent_agent = make_error_agent_stage2(FLUENT_PROMPT, "Fluent", "semantic_equivalent_stage1")
Mixd_lang_agent = make_error_agent_stage2(MIXD_LANG_PROMPT, "Mixd_lang", "semantic_equivalent_stage1")
Negt_anto_agent = make_error_agent_stage2(NEGT_ANTO_PROMPT, "Negt_anto", "semantic_equivalent_stage1")
Default_similar_agent = make_error_agent_stage2(DEFAULT_SIMILAR_PROMPT, "Default_similar", "semantic_equivalent_stage1")

Anto_flip_agent = make_error_agent_stage2(ANTO_FLIP_PROMPT, "Anto_flip", "semantic_contradiction_stage1")
Negt_flip_agent = make_error_agent_stage2(NEGT_FLIP_PROMPT, "Negt_flip", "semantic_contradiction_stage1")
Word_rplc_agent = make_error_agent_stage2(WORD_RPLC_PROMPT, "Word_rplc", "semantic_contradiction_stage1")
Neutral_agent = make_error_agent_stage2(NEUTRAL_PROMPT, "Neutral", "semantic_contradiction_stage1")
Default_dissimilar_agent = make_error_agent_stage2(DEFAULT_DISSIMILAR_PROMPT, "Default_dissimilar", "semantic_contradiction_stage1")

Gend_flip_agent = make_error_agent_stage2(GEND_FLIP_PROMPT, "Gend_flip", "grammatical_morphological_distortion_stage1")
Sing_plul_agent = make_error_agent_stage2(SING_PLUL_PROMPT, "Sing_plul", "grammatical_morphological_distortion_stage1")
Tens_chng_agent = make_error_agent_stage2(TENS_CHNG_PROMPT, "Tens_chng", "grammatical_morphological_distortion_stage1")
Word_ordr_agent = make_error_agent_stage2(WORD_ORDR_PROMPT, "Word_ordr", "grammatical_morphological_distortion_stage1")

Add_extra_agent = make_error_agent_stage2(ADD_EXTRA_PROMPT, "Add_extra", "information_completeness_stage1")
Omission_agent = make_error_agent_stage2(OMISSION_PROMPT, "Omission", "information_completeness_stage1")

# Stage 3: Cross-verification agents for each super-category
semantic_equivalent_stage3_agent = make_error_agent_stage3(SEMANTIC_EQUIVALENT_STAGE3_PROMPT, "semantic_equivalent_stage3", "semantic_equivalent_stage1")
semantic_contradiction_stage3_agent = make_error_agent_stage3(SEMANTIC_CONTRADICTION_STAGE3_PROMPT, "semantic_contradiction_stage3", "semantic_contradiction_stage1")
grammatical_morphological_distortion_stage3_agent = make_error_agent_stage3(GRAMMATICAL_MORPHOLOGICAL_DISTORTION_STAGE3_PROMPT, "grammatical_morphological_distortion_stage3", "grammatical_morphological_distortion_stage1")
information_completeness_stage3_agent = make_error_agent_stage3(INFORMATION_COMPLETENESS_STAGE3_PROMPT, "information_completeness_stage3", "information_completeness_stage1")