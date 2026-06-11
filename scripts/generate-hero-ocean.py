"""Generate seamless hero ocean loops while keeping architecture static.

Requires Pillow and NumPy. Frames are written under .astro/ and encoded with
the project's installed ffmpeg binary.
"""

from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
FRAME_ROOT = ROOT / ".astro" / "hero-ocean-frames"
OUTPUT = ROOT / "public" / "videos" / "hero"
FPS = 24
DURATION = 6
FRAME_COUNT = FPS * DURATION


SCENES = {
    "desktop": {
        "source": ROOT / "public/images/empreendimentos/salvador-220/05.jpg",
        "size": (1280, 720),
        # Open water left of the building plus the distant coastal water.
        "water": [
            [(0.0, 0.535), (0.49, 0.535), (0.49, 0.645), (0.30, 0.72), (0.0, 0.86)],
            [(0.48, 0.535), (1.0, 0.535), (1.0, 0.84), (0.68, 0.75), (0.53, 0.67)],
        ],
        "foam": [
            [(0.62, 0.59), (1.0, 0.60), (1.0, 0.80), (0.72, 0.71)],
        ],
        "strength": 1.0,
    },
    "mobile": {
        "source": ROOT / "public/images/empreendimentos/salvador-220/01.jpg",
        "size": (960, 540),
        # Water follows the rocky coastline without touching the building.
        "water": [
            [(0.45, 0.535), (1.0, 0.535), (1.0, 1.0), (0.0, 1.0), (0.0, 0.90), (0.28, 0.82)],
        ],
        "foam": [
            [(0.0, 0.78), (0.55, 0.67), (0.72, 0.72), (0.62, 0.83), (0.0, 0.98)],
        ],
        "strength": 1.35,
    },
}


def polygon_mask(size: tuple[int, int], polygons: list[list[tuple[float, float]]], blur: int) -> Image.Image:
    width, height = size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    for polygon in polygons:
        draw.polygon([(round(x * width), round(y * height)) for x, y in polygon], fill=255)
    return mask.filter(ImageFilter.GaussianBlur(blur))


def animated_water(image: Image.Image, phase: float, strength: float) -> Image.Image:
    """Shift narrow water strips with seamless sine motion."""
    width, height = image.size
    source = np.asarray(image)
    result = np.empty_like(source)
    vertical = round(math.sin(phase * 2.0) * strength)
    y_indices = np.clip(np.arange(height) - vertical, 0, height - 1)
    source = source[y_indices]
    x_indices = np.arange(width)

    for y in range(height):
        dx = round(
            strength
            * (
                2.4 * math.sin(phase + y * 0.060)
                + 1.3 * math.sin(phase * 2.0 - y * 0.027)
            )
        )
        result[y] = source[y, np.clip(x_indices - dx, 0, width - 1)]
    return Image.fromarray(result)


def foam_layer(image: Image.Image, foam_mask: Image.Image, phase: float, strength: float) -> Image.Image:
    """Extract existing bright foam and give it a subtle advancing pulse."""
    rgb = np.asarray(image).astype(np.int16)
    bright = rgb.mean(axis=2)
    saturation = rgb.max(axis=2) - rgb.min(axis=2)
    foam = np.clip((bright - 145) * 3 - saturation * 1.2, 0, 150).astype(np.uint8)
    foam_image = Image.fromarray(foam, "L")
    foam_image = ImageChops.multiply(foam_image, foam_mask)
    foam_image = foam_image.filter(ImageFilter.GaussianBlur(1.2))

    advance = round((math.sin(phase) * 2.5 + math.sin(phase * 2.0) * 1.2) * strength)
    opacity = 0.72 + 0.20 * math.sin(phase - 0.6)
    foam_image = ImageChops.offset(foam_image, advance, -advance)
    foam_image = ImageEnhance.Brightness(foam_image).enhance(opacity)

    white = Image.new("RGB", image.size, (235, 246, 248))
    return Image.composite(white, Image.new("RGB", image.size), foam_image)


def generate_scene(name: str, config: dict) -> Path:
    frame_dir = FRAME_ROOT / name
    if frame_dir.exists():
        shutil.rmtree(frame_dir)
    frame_dir.mkdir(parents=True)

    image = Image.open(config["source"]).convert("RGB").resize(config["size"], Image.Resampling.LANCZOS)
    water_mask = polygon_mask(config["size"], config["water"], blur=9)
    foam_mask = polygon_mask(config["size"], config["foam"], blur=7)

    for index in range(FRAME_COUNT):
        phase = 2 * math.pi * index / FRAME_COUNT
        water = animated_water(image, phase, config["strength"])
        frame = Image.composite(water, image, water_mask)

        foam = foam_layer(image, foam_mask, phase, config["strength"])
        foam_alpha = foam.convert("L").point(lambda value: min(105, value))
        frame = Image.composite(foam, frame, foam_alpha)
        frame.save(frame_dir / f"{index:04d}.jpg", quality=88, optimize=True)

    return frame_dir


def encode(frame_dir: Path, name: str, width: int) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    input_pattern = str(frame_dir / "%04d.jpg")

    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(FPS), "-i", input_pattern,
            "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "24",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(OUTPUT / f"ocean-{name}.mp4"),
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-framerate", str(FPS), "-i", input_pattern,
            "-an", "-c:v", "libvpx-vp9", "-crf", "34", "-b:v", "0",
            "-row-mt", "1", "-deadline", "good", "-cpu-used", "2",
            str(OUTPUT / f"ocean-{name}.webm"),
        ],
        check=True,
    )
    print(f"Generated {name} loop at {width}px")


def main() -> None:
    for name, config in SCENES.items():
        frames = generate_scene(name, config)
        encode(frames, name, config["size"][0])


if __name__ == "__main__":
    main()
