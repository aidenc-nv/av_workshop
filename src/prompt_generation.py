from dataclasses import dataclass
from typing import Optional, List


# --- Configuration dictionaries from your table --- #

ENV_LIGHTING = {
    "sunrise": "bathed in warm morning light, with long shadows and an orange–pink glow along the eastern sky",
    "sunset": "lit by warm evening light, with long shadows and an orange–pink glow along the western sky",
    "twilight": "covered in cool blue twilight, with low ambient light and softly diffused backgrounds",
    "mid-morning": "under clear daylight, with balanced shadows and crisp textures",
    "afternoon": "under neutral daylight, with natural shadows and bright overall exposure",
    "zenith": "under harsh overhead midday light, with very short shadows and strong contrast",
    "golden hour": "in soft warm golden-hour light, with elongated shadows and enhanced sense of depth",
    "blue hour": "in deep blue hour tones, with low light and gentle ambient illumination",
    "night": "at night, with low light, high contrast, and strong glow from vehicle headlights and streetlamps",
}

WEATHER = {
    "clear_sky": "The sky is clear with high visibility, distinct shadows, and a soft light-blue gradient toward the horizon.",
    "overcast": "The sky is overcast, creating flat, diffuse lighting with a gray–white canopy and reduced shadow contrast.",
    "snow_falling": "Snow is actively falling, with visible streaks and a cold white balance that slightly desaturates the scene.",
    "raining": "Rain is falling, with visible streaks, a subtle motion blur in the drops, and a damp atmosphere throughout the scene.",
    "fog": "A layer of fog introduces depth-based haze, softening distant structures and partially obscuring objects farther from the camera.",
    None: ""  # allows omitting weather if desired
}

ROAD_SURFACE = {
    "dry_road": "The road surface is clean, dry asphalt with clearly visible lane markings and consistent reflectance.",
    "snow_on_ground": "The ground is covered with snow, showing tire tracks, compacted patches, and small snow piles pushed toward the edges.",
    "sand_on_ground": "The ground is covered in light tan sand with a granular texture, subtle unevenness, and a faint dust haze near fast-moving vehicles.",
    "puddles": "The road is dotted with puddles that create mirror-like reflections of vehicles, traffic lights, and nearby buildings, with occasional ripples from passing tires.",
    "wooden": "The entire road surface is made of wide wooden planks, with visible grain, seams between boards, and subtle tonal variation under the light.",
    None: ""
}


@dataclass
class SceneConfig:
    base_scene: str
    env_lighting: Optional[str] = None      # keys from ENV_LIGHTING
    weather: Optional[str] = None           # keys from WEATHER
    road_surface: Optional[str] = None      # keys from ROAD_SURFACE
    extra_tags: Optional[List[str]] = None  # optional: for downstream use (e.g., metadata)


def generate_prompt(config: SceneConfig) -> str:
    """
    Generate a natural language prompt from a SceneConfig.

    - base_scene: core description of layout/objects (e.g., 'a bustling urban intersection...')
    - env_lighting: one of ENV_LIGHTING keys, or None
    - weather: one of WEATHER keys, or None
    - road_surface: one of ROAD_SURFACE keys, or None
    """

    parts = []

    # 1) Start with base scene
    parts.append(config.base_scene.strip())

    # 2) Environment lighting sentence (if any)
    if config.env_lighting:
        lighting_desc = ENV_LIGHTING.get(config.env_lighting)
        if lighting_desc:
            parts.append(f"The scene is {lighting_desc}.")

    # 3) Weather conditions (if any)
    if config.weather in WEATHER:
        weather_desc = WEATHER[config.weather]
        if weather_desc:
            parts.append(weather_desc)

    # 4) Road surface details (if any)
    if config.road_surface in ROAD_SURFACE:
        surface_desc = ROAD_SURFACE[config.road_surface]
        if surface_desc:
            parts.append(surface_desc)

    # 5) Optional: add a closing sentence emphasizing coherence
    parts.append("All visual elements should be consistent with these conditions and lighting cues.")

    # Join into single prompt
    prompt = " ".join(part.strip() for part in parts if part and part.strip())
    return prompt


# --- Example usage --- #
if __name__ == "__main__":
    # Example base scene (you can plug your intersection description here)
    base_scene = (
        "The video depicts a bustling urban intersection with modern buildings, "
        "traffic lights, and multiple vehicles (including a red car in the foreground, "
        "a black SUV turning right, and several other cars in various colors) "
        "navigating the crossing."
    )

    config = SceneConfig(
        base_scene=base_scene,
        env_lighting="sunrise",     # try: "night", "golden hour", etc.
        weather="fog",              # try: "clear_sky", "raining", None, etc.
        road_surface="wooden",      # try: "dry_road", "puddles", "snow_on_ground", etc.
        extra_tags=["urban", "traffic", "multivehicle"]
    )

    prompt = generate_prompt(config)
    print(prompt)