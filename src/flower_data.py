"""Human-readable metadata for each of the 17 flower classes."""

FLOWER_INFO: dict[str, dict[str, str]] = {
    "bluebell": {
        "emoji": "🔔",
        "common_name": "English Bluebell",
        "family": "Asparagaceae",
        "description": "Woodland perennial with nodding, violet-blue bell-shaped flowers blooming in spring.",
    },
    "buttercup": {
        "emoji": "🌟",
        "common_name": "Meadow Buttercup",
        "family": "Ranunculaceae",
        "description": "Glossy yellow cup-shaped flowers common in grasslands and meadows across Europe.",
    },
    "colts_foot": {
        "emoji": "🟡",
        "common_name": "Coltsfoot",
        "family": "Asteraceae",
        "description": "Dandelion-like yellow flower that appears before its hoof-shaped leaves in early spring.",
    },
    "cowslip": {
        "emoji": "🌼",
        "common_name": "Cowslip",
        "family": "Primulaceae",
        "description": "Clusters of fragrant, deep-yellow drooping flowers on a single tall stem.",
    },
    "crocus": {
        "emoji": "💜",
        "common_name": "Spring Crocus",
        "family": "Iridaceae",
        "description": "Cup-shaped blooms in purple, yellow or white; one of the first flowers of spring.",
    },
    "daffodil": {
        "emoji": "📯",
        "common_name": "Wild Daffodil",
        "family": "Amaryllidaceae",
        "description": "Iconic pale-yellow petals surrounding a trumpet-shaped corona; symbol of spring.",
    },
    "daisy": {
        "emoji": "🌸",
        "common_name": "Common Daisy",
        "family": "Asteraceae",
        "description": "Classic white ray florets around a bright yellow disc; opens at dawn, closes at dusk.",
    },
    "dandelion": {
        "emoji": "☀️",
        "common_name": "Dandelion",
        "family": "Asteraceae",
        "description": "Bright yellow composite flower that transforms into a spherical seed head.",
    },
    "fritillary": {
        "emoji": "🧩",
        "common_name": "Snakeshead Fritillary",
        "family": "Liliaceae",
        "description": "Distinctive checkered purple-pink bells dangling from slender stems.",
    },
    "iris": {
        "emoji": "👑",
        "common_name": "Yellow Iris",
        "family": "Iridaceae",
        "description": "Showy flowers with three upright and three drooping petals; loves wetlands.",
    },
    "lily_valley": {
        "emoji": "🤍",
        "common_name": "Lily of the Valley",
        "family": "Asparagaceae",
        "description": "Tiny, sweetly scented white bells dangling in a row along an arching stem.",
    },
    "pansy": {
        "emoji": "🎨",
        "common_name": "Garden Pansy",
        "family": "Violaceae",
        "description": "Large two-tone face-like blooms in nearly every colour combination imaginable.",
    },
    "snowdrop": {
        "emoji": "❄️",
        "common_name": "Snowdrop",
        "family": "Amaryllidaceae",
        "description": "Delicate white drooping bells; often the very first flower to bloom after winter.",
    },
    "sunflower": {
        "emoji": "🌻",
        "common_name": "Sunflower",
        "family": "Asteraceae",
        "description": "Tall annual with enormous yellow heads that track the sun across the sky.",
    },
    "tigerlily": {
        "emoji": "🐯",
        "common_name": "Tiger Lily",
        "family": "Liliaceae",
        "description": "Vivid orange recurved petals covered in bold dark spots on tall stems.",
    },
    "tulip": {
        "emoji": "🌷",
        "common_name": "Tulip",
        "family": "Liliaceae",
        "description": "Cup-shaped spring bulb flower famous for its vivid, saturated colours.",
    },
    "windflower": {
        "emoji": "🌬️",
        "common_name": "Wood Anemone",
        "family": "Ranunculaceae",
        "description": "White star-shaped flowers that tremble in the slightest breeze, hence the name.",
    },
}


def get_info(class_name: str) -> dict[str, str]:
    return FLOWER_INFO.get(
        class_name,
        {"emoji": "🌸", "common_name": class_name.replace("_", " ").title(), "family": "—", "description": ""},
    )
