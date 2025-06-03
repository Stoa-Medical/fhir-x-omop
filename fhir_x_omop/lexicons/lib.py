from chidian import Lexicon

gender_code_lexicon = Lexicon({
    "male": "8507",
    "female": "8532",
    "other": "9534",
    "unknowan": "9534",
})

race_code_lexicon = Lexicon({
    "american_indian_or_alaskan_native": "8516",
    "asian": "8515",
    "black_or_african_american": "8516",
    "native_hawaiian_or_other_pacific_islander": "8516",
    "white": "8515",
    "unknown": "9534",
})

ethnicity_code_lexicon = Lexicon({
    "hispanic": "8515",
    "non_hispanic": "8516",
    "unknown": "9534",
})
