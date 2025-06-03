from chidian import Lexicon

gender_code_lexicon = Lexicon({
    "8507": "male",
    "8532": "female",
    "0": "unknown",
    "8521": "other",
    "8570": "unknown",
})

race_code_lexicon = Lexicon({
    "8657": "1002-5",  # American Indian or Alaska Native
    "8515": "2028-9",  # Asian
    "8516": "2054-5",  # Black or African American
    "8557": "2076-8",  # Native Hawaiian or Other Pacific Islander
    "8527": "2106-3",  # White
    "0": "UNK",        # Unknown
    "8552": "UNK",     # Unknown
})

ethnicity_code_lexicon = Lexicon({
    "38003563": "2135-2",  # Hispanic or Latino
    "38003564": "2186-5",  # Not Hispanic or Latino
    "0": "UNK",            # Unknown
    "8552": "UNK",         # Unknown
})
