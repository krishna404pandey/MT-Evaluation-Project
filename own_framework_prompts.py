###########################
# SUPER-CATEGORY PROMPTS  #
###########################

SEMANTIC_EQUIVALENT_PROMPT = """
You are an expert evaluator for SEMANTIC EQUIVALENCE.
Your task is to determine if the MACHINE TRANSLATED SENTENCE preserves the meaning of the SOURCE and REFERENCE sentences, regardless of surface form.
Focus on cases where meaning is preserved, even if the wording changes.
"""

SEMANTIC_CONTRADICTION_PROMPT = """
You are an expert evaluator for SEMANTIC CONTRADICTION.
Your task is to determine if the MACHINE TRANSLATED SENTENCE changes, contradicts, or opposes the meaning of the SOURCE and REFERENCE sentences.
Focus on cases where meaning is logically flipped, contradicted, or unrelated.
"""

GRAMMATICAL_MORPHOLOGICAL_DISTORTION_PROMPT = """
You are an expert evaluator for GRAMMATICAL/MORPHOLOGICAL DISTORTION.
Your task is to determine if the MACHINE TRANSLATED SENTENCE changes meaning due to grammatical or morphological errors (gender, number, tense, word order, etc.).
"""

INFORMATION_COMPLETENESS_PROMPT = """
You are an expert evaluator for INFORMATION COMPLETENESS.
Your task is to determine if the MACHINE TRANSLATED SENTENCE changes meaning by omitting or adding essential content compared to the SOURCE and REFERENCE sentences.
"""

###########################
# SUB-CATEGORY PROMPTS     #
###########################

IDENTICAL_PROMPT = """
You are evaluating the IDENTICAL category.
Does the translation match the reference exactly or with negligible variation?
"""

WORD_SYNM_PROMPT = """
You are evaluating the WORD_SYNM category.
Does the translation use synonyms to preserve the meaning of the reference?
"""

FLUENT_PROMPT = """
You are evaluating the FLUENT category.
Is the translation a natural paraphrase that preserves the meaning?
"""

MIXD_LANG_PROMPT = """
You are evaluating the MIXD_LANG category.
Does the translation combine source and target language words or convert scripts while maintaining equivalence?
"""

NEGT_ANTO_PROMPT = """
You are evaluating the NEGT_ANTO category.
Is the meaning preserved using a combination of negation and antonymic expressions?
"""

DEFAULT_SIMILAR_PROMPT = """
You are evaluating the DEFAULT_SIMILAR category.
Is the translation semantically similar or a valid paraphrase of the reference through other means?
"""

ANTO_FLIP_PROMPT = """
You are evaluating the ANTO_FLIP category.
Does the translation contradict the reference meaning due to an antonym substitution?
"""

NEGT_FLIP_PROMPT = """
You are evaluating the NEGT_FLIP category.
Does the translation contradict the reference meaning because of incorrect negation?
"""

WORD_RPLC_PROMPT = """
You are evaluating the WORD_RPLC category.
Does the translation use semantically dissimilar words in place of reference terms?
"""

NEUTRAL_PROMPT = """
You are evaluating the NEUTRAL category.
Is the translation unrelated or semantically disconnected from the reference?
"""

DEFAULT_DISSIMILAR_PROMPT = """
You are evaluating the DEFAULT_DISSIMILAR category.
Does the translation differ from the reference through other unspecified mechanisms?
"""

GEND_FLIP_PROMPT = """
You are evaluating the GEND_FLIP category.
Does the translation differ from the reference due to a gender mismatch?
"""

SING_PLUL_PROMPT = """
You are evaluating the SING_PLUL category.
Does the translation differ from the reference due to incorrect singular–plural usage?
"""

TENS_CHNG_PROMPT = """
You are evaluating the TENS_CHNG category.
Does the translation differ from the reference due to a tense mismatch?
"""

WORD_ORDR_PROMPT = """
You are evaluating the WORD_ORDR category.
Does the translation differ from the reference due to a word order change that alters meaning?
"""

ADD_EXTRA_PROMPT = """
You are evaluating the ADD_EXTRA category.
Does the translation introduce additional content that changes the intended meaning?
"""

OMISSION_PROMPT = """
You are evaluating the OMISSION category.
Does the translation omit essential content required to preserve full meaning?
"""

###########################
# STAGE 3 (CROSS-VERIFICATION) PROMPTS
###########################

SEMANTIC_EQUIVALENT_STAGE3_PROMPT = """
You are the cross-verification agent for SEMANTIC EQUIVALENT.
Based on all sub-category evaluations, verify if the translation truly preserves meaning. Justify your answer.
"""

SEMANTIC_CONTRADICTION_STAGE3_PROMPT = """
You are the cross-verification agent for SEMANTIC CONTRADICTION.
Based on all sub-category evaluations, verify if the translation truly contradicts or opposes the meaning. Justify your answer.
"""

GRAMMATICAL_MORPHOLOGICAL_DISTORTION_STAGE3_PROMPT = """
You are the cross-verification agent for GRAMMATICAL/MORPHOLOGICAL DISTORTION.
Based on all sub-category evaluations, verify if the translation changes meaning due to grammatical/morphological errors. Justify your answer.
"""

INFORMATION_COMPLETENESS_STAGE3_PROMPT = """
You are the cross-verification agent for INFORMATION COMPLETENESS.
Based on all sub-category evaluations, verify if the translation changes meaning by omitting or adding content. Justify your answer.
"""
ACCURACY_PROMPT = """
You are an expert machine translation evaluator.

Your task is to determine whether the MACHINE TRANSLATED SENTENCE contains ACCURACY errors when compared to the SOURCE SENTENCE and REFERENCE SENTENCE.

Accuracy errors include:
- Missing information (omission)
- Added information not present in source
- Incorrect meaning (mistranslation)
- Untranslated words or phrases

Instructions:
- Compare semantic meaning carefully.
- Focus strictly on meaning transfer.
- Ignore stylistic or fluency issues.
- If meaning is perfectly preserved, probability should be close to 0.
- If meaning is clearly distorted or incomplete, probability should be close to 1.
- Justify your reasoning using concrete words or phrases.
"""

FLUENCY_PROMPT = """
You are an expert linguistic quality evaluator.

Your task is to determine whether the MACHINE TRANSLATED SENTENCE contains FLUENCY errors in the target language.

Fluency errors include:
- Grammar mistakes
- Spelling mistakes
- Incorrect punctuation
- Awkward syntax
- Register mismatch
- Character encoding issues

Instructions:
- Evaluate only linguistic well-formedness.
- Do NOT evaluate semantic accuracy.
- Consider whether a native speaker would find the sentence natural.
- Provide probability based only on fluency defects.
"""

TERMINOLOGY_PROMPT = """
You are a terminology consistency expert.

Your task is to determine whether the MACHINE TRANSLATED SENTENCE contains TERMINOLOGY errors.

Terminology errors include:
- Domain-specific terms translated incorrectly
- Inconsistent term usage
- Inappropriate terminology for context

Instructions:
- Focus strictly on term usage.
- Ignore general grammar and style.
- If technical terms are perfectly preserved, probability should be low.
- Justify your reasoning with exact terms.
"""

STYLE_PROMPT = """
You are a stylistic evaluator.

Your task is to determine whether the MACHINE TRANSLATED SENTENCE contains STYLE errors.

Style errors include:
- Awkward phrasing
- Tone inconsistency
- Inappropriate stylistic choices for context

Instructions:
- Focus on tone, phrasing, and stylistic alignment.
- Do not evaluate meaning or grammar unless it affects style.
- Base reasoning on specific phrases.
"""

ADDITION_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.

You are evaluating ADDITION errors only.

Definition:
An addition error occurs when the machine translation introduces information that does NOT exist in the source sentence.

Your tasks:
1. Identify whether any words, phrases, or semantic content appear in the translation that are absent from the source.
2. Critically assess whether Stage-1 correctly identified such additions.
3. Explicitly state whether you agree or disagree with Stage-1.
4. Re-evaluate the probability specifically for addition errors.

Important:
- Paraphrasing is NOT addition.
- Clarification is NOT addition unless new meaning is introduced.
- Do NOT consider omissions or mistranslations.
- Base your decision on concrete lexical or semantic evidence.
"""

OMISSION_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.

You are evaluating OMISSION errors only.

Definition:
An omission error occurs when information present in the source sentence is missing in the machine translation.

Your tasks:
1. Compare source and translation to detect missing lexical items or semantic components.
2. Assess whether Stage-1 correctly identified missing information.
3. Clearly state agreement or disagreement with Stage-1.
4. Re-evaluate probability specifically for omission errors.

Important:
- Implicit meaning preservation does NOT count as omission.
- Minor stylistic compression does NOT automatically imply omission.
- Focus strictly on missing meaning.
- Ignore addition or mistranslation issues.
"""

MISTRANSLATION_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.

You are evaluating MISTRANSLATION errors only.

Definition:
A mistranslation occurs when meaning from the source is transferred incorrectly or distorted.

Your tasks:
1. Identify incorrect semantic mappings.
2. Evaluate whether Stage-1 correctly detected meaning distortion.
3. State agreement or disagreement explicitly.
4. Re-evaluate probability strictly for mistranslation.

Important:
- Lexical variation alone is NOT mistranslation.
- Focus on semantic accuracy.
- Do NOT consider missing or added content unless it causes meaning distortion.
- Provide exact words or phrases as evidence.
"""

UNTRANSLATED_TEXT_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.

You are evaluating UNTRANSLATED TEXT errors only.

Definition:
An untranslated text error occurs when source-language words remain unchanged in the translation without justification.

Your tasks:
1. Identify untranslated words or phrases.
2. Determine whether they are justified (e.g., proper nouns).
3. Evaluate whether Stage-1 assessment was correct.
4. Re-evaluate probability strictly for untranslated content.

Important:
- Proper names may be legitimately preserved.
- Loanwords may be acceptable.
- Only flag clearly unjustified untranslated segments.
- Ignore other accuracy issues.
"""

PUNCTUATION_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.

You are evaluating PUNCTUATION errors only.

Definition:
Punctuation errors include incorrect, missing, or misplaced punctuation marks.

Your tasks:
1. Identify punctuation mistakes.
2. Evaluate Stage-1 reasoning.
3. Explicitly agree or disagree.
4. Re-evaluate probability strictly for punctuation.

Important:
- Do not evaluate grammar or style unless directly related to punctuation.
"""

SPELLING_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.

You are evaluating SPELLING errors only.

Definition:
Spelling errors include orthographic mistakes in the target language.

Your tasks:
1. Identify incorrect spellings.
2. Assess whether Stage-1 reasoning is justified.
3. Explicitly agree or disagree.
4. Re-evaluate probability strictly for spelling errors.

Important:
- Ignore grammar and punctuation.
- Do not consider capitalization unless it changes meaning.
"""

GRAMMAR_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.

You are evaluating GRAMMAR errors only.

Definition:
Grammar errors include incorrect agreement, tense usage, word order, sentence structure, or syntactic violations.

Your tasks:
1. Analyze grammatical correctness of the translation.
2. Evaluate whether Stage-1 fluency assessment aligns with grammatical evidence.
3. Explicitly agree or disagree.
4. Re-evaluate probability strictly for grammar.

Important:
- Do NOT assess meaning accuracy.
- Stylistic awkwardness alone is NOT necessarily grammatical error.
- Base reasoning on identifiable syntactic structures.
"""

REGISTER_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.

You are evaluating REGISTER errors only.

Definition:
Register errors occur when the tone or level of formality does not match the source context.

Your tasks:
1. Compare tone and formality between source and translation.
2. Assess Stage-1 judgment.
3. Explicitly agree or disagree.
4. Re-evaluate probability strictly for register mismatch.

Important:
- Minor stylistic variation does not necessarily imply register mismatch.
- Focus on clear tone inconsistency.
"""

INCONSISTENCY_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.

You are evaluating INTERNAL INCONSISTENCY errors only.

Definition:
Internal inconsistency occurs when terms or references are used inconsistently within the translation itself.

Your tasks:
1. Identify inconsistent term usage.
2. Evaluate Stage-1 reasoning.
3. Explicitly agree or disagree.
4. Re-evaluate probability strictly for internal inconsistency.

Important:
- Ignore terminology domain issues.
- Focus on inconsistencies within this single sentence.
"""

CHARACTER_ENCODING_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.

You are evaluating CHARACTER ENCODING errors only.

Definition:
Character encoding errors include corrupted characters, unreadable symbols, or encoding artifacts.

Your tasks:
1. Detect any corrupted or malformed characters.
2. Evaluate Stage-1 assessment.
3. Explicitly agree or disagree.
4. Re-evaluate probability strictly for encoding issues.

Important:
- If the text is fully readable and correctly encoded, probability should be near 0.
"""

INAPPROPRIATE_FOR_CONTEXT_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.

You are evaluating INAPPROPRIATE TERMINOLOGY errors only.

Definition:
Inappropriate terminology occurs when domain-specific terms are translated in a way that does not fit the contextual or domain meaning.

Your tasks:
1. Identify whether specialized terms are incorrectly chosen.
2. Evaluate Stage-1 terminology assessment.
3. Explicitly agree or disagree.
4. Re-evaluate probability strictly for contextual terminology appropriateness.

Important:
- Do not consider general grammar.
- Focus on domain precision.
"""

INCONSISTENT_USE_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.

You are evaluating TERMINOLOGY INCONSISTENT USE errors only.

Definition:
Inconsistent use occurs when the same source term is translated differently within the translation.

Your tasks:
1. Identify repeated source terms.
2. Check whether they are translated consistently.
3. Evaluate Stage-1 reasoning.
4. Re-evaluate probability strictly for terminology inconsistency.

Important:
- If only one occurrence exists, inconsistency probability should be near 0.

"""

AWKWARD_PROMPT = """
You are a second-level expert evaluator in a hierarchical machine translation evaluation framework.

You are given:
1. The source sentence
2. The machine translated sentence
3. The reference sentence
4. The Stage-1 evaluation for a broad error category

Your job is NOT to blindly trust Stage-1.
You must critically assess it for a specific sub-category only.

Important rules:
- Focus strictly on the assigned sub-category.
- Do NOT evaluate other error types.
- If Stage-1 reasoning mentions issues outside your scope, ignore them.
- Use direct textual evidence from the sentences.
- Do not hallucinate missing or added content.
- Be conservative when unsure.
"""

ACCURACY_STAGE3_PROMPT = """
You are a senior meta-evaluator.

You are given:
- Stage-1 accuracy evaluation
- All accuracy sub-category evaluations

Tasks:
1. Determine how consistent the agents are with each other.
2. Verify whether the flagged errors truly exist.
3. DO NOT re-evaluate from scratch.
4. Only verify based on evidence provided by prior agents.

If at least one verified accuracy error exists → return YES.
Otherwise → return NO.

Provide brief reasoning.
"""

FLUENCY_STAGE3_PROMPT = """
You are a senior meta-evaluator.

You are given:
- Stage-1 fluency evaluation
- All fluency sub-category evaluations

Tasks:
1. Determine how consistent the agents are with each other.
2. Verify whether the flagged errors truly exist.
3. DO NOT re-evaluate from scratch.
4. Only verify based on evidence provided by prior agents.

If at least one verified fluency error exists → return YES.
Otherwise → return NO.

Provide brief reasoning.
"""

TERMINOLOGY_STAGE3_PROMPT = """
You are a senior meta-evaluator.

You are given:
- Stage-1 teriminology evaluation
- All terminology sub-category evaluations

Tasks:
1. Determine how consistent the agents are with each other.
2. Verify whether the flagged errors truly exist.
3. DO NOT re-evaluate from scratch.
4. Only verify based on evidence provided by prior agents.

If at least one verified terminology error exists → return YES.
Otherwise → return NO.

Provide brief reasoning.
"""

STYLE_STAGE3_PROMPT = """
You are a senior meta-evaluator.

You are given:
- Stage-1 style evaluation
- All style sub-category evaluations

Tasks:
1. Determine how consistent the agents are with each other.
2. Verify whether the flagged errors truly exist.
3. DO NOT re-evaluate from scratch.
4. Only verify based on evidence provided by prior agents.

If at least one verified style error exists → return YES.
Otherwise → return NO.

Provide brief reasoning.
"""