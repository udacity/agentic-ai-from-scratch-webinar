"""Housing facts and recommendation rules shared across agents."""


HOUSING_RECOMMENDATION_RULES = (
    "A housing recommendation should consider budget, bedrooms, and location.",
    "Rent and availability can change and must be verified before signing a lease.",
    "Only claim housing facts found in application-supplied data.",
)

AUSTIN_NEIGHBORHOOD_KNOWLEDGE = (
    "Cedar Park is suburban and quiet, with a typical example commute of 35 minutes.",
    "Lakeway is walkable and family-friendly, but the commute downtown might be close to an hour.",
    "Downtown Austin is urban and lively, with parks, hiking trails, and outdoor activities nearby; its typical example commute is 8 minutes.",
    "Mueller is walkable and family-friendly, with a typical example commute of 18 minutes.",
    "Shorter commutes often involve tradeoffs in space, price, or neighborhood character.",
)

# Agents can import one shared collection while the source remains organized into
# factual domain knowledge and behavioral recommendation rules.
HOUSING_RECOMMENDATION_KNOWLEDGE = (
    HOUSING_RECOMMENDATION_RULES + AUSTIN_NEIGHBORHOOD_KNOWLEDGE
)
