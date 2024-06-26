configuration = {
    "title": "Saper",

    "test_mode": False,

    "fullscreen": False,
    "resizable_x": False,
    "resizable_y": False,

    "font_family": ["Arial", "Bauhaus 93"],

    "colors": {
        "tile": "#2c6cab",
        "tile_flagged": "#2cab5b",
        "tile_mine": "#b80000",
        "tile_revealed": "#adb5be",

        "tile_zero": "#adb5be",
        "tile_one": "#4c48bd",
        "tile_two": "#b8852c",
        "tile_three": "#1d5231",
        "tile_four": "#2c93b8",
        "tile_five": "#662cb8",
        "tile_six": "#b85d2c",
        "tile_seven": "#2c9eb8",
        "tile_eight": "#b12cb8",
    },

    "difficulty": {
        0: {
            "rows": 9,
            "cols": 9,
            "mines": 10,
        },
        1: {
            "rows": 16,
            "cols": 16,
            "mines": 40,
        },
        2: {
            "rows": 20,
            "cols": 24,
            "mines": 99,
        }
    }
}
