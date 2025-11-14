#!/usr/bin/env python3
"""
Generate AI images for toddler games using Google Gemini API.
Includes automatic background removal and optimization.
"""

from google import genai
import os
import sys
import json
import argparse
from PIL import Image
from pathlib import Path
import time

try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    print("Warning: rembg not available. Background removal will be skipped.")
    print("Install with: pip install rembg")


def create_client():
    """Create and configure Gemini API client with error handling."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    print("✓ Gemini API configured")
    return client


def generate_image(client, prompt, model_name="gemini-2.5-flash-image"):
    """
    Generate an image using Gemini API.

    Args:
        client: Gemini API client
        prompt: Text description of the image to generate
        model_name: Gemini model to use for image generation
                   (default: gemini-2.5-flash-image - current stable model)

    Returns:
        PIL Image object or None on failure
    """
    try:
        print(f"  Generating: {prompt[:60]}...")

        response = client.models.generate_content(
            model=model_name,
            contents=[prompt],
        )

        # Extract image from response
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                print(f"  ✓ Generated {image.size[0]}x{image.size[1]} image")
                return image
            elif part.text is not None:
                print(f"  ⚠ Received text response: {part.text[:60]}...")

        print(f"  ✗ No image data in response")
        return None

    except Exception as e:
        print(f"  ✗ Error generating image: {e}")
        return None


def remove_background(image):
    """
    Remove background from image using rembg.

    Args:
        image: PIL Image object

    Returns:
        PIL Image with transparent background
    """
    if not REMBG_AVAILABLE:
        print("  ⚠ Skipping background removal (rembg not installed)")
        return image

    try:
        print("  Removing background...")

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Remove background
        output = remove(img_byte_arr)

        # Convert back to PIL Image
        result = Image.open(io.BytesIO(output))
        print("  ✓ Background removed")
        return result

    except Exception as e:
        print(f"  ✗ Error removing background: {e}")
        return image


def optimize_image(image, max_size=1024):
    """
    Optimize image size while maintaining quality.

    Args:
        image: PIL Image object
        max_size: Maximum dimension (width or height)

    Returns:
        Optimized PIL Image
    """
    width, height = image.size

    # Resize if too large
    if width > max_size or height > max_size:
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))

        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"  ✓ Resized to {new_width}x{new_height}")

    return image


def save_image(image, filepath, formats=['png', 'webp']):
    """
    Save image in multiple formats.

    Args:
        image: PIL Image object
        filepath: Path without extension
        formats: List of formats to save
    """
    path = Path(filepath)

    for fmt in formats:
        output_path = path.with_suffix(f'.{fmt}')

        if fmt == 'webp':
            image.save(output_path, 'WEBP', quality=90, method=6)
        elif fmt == 'png':
            image.save(output_path, 'PNG', optimize=True)

        file_size = output_path.stat().st_size / 1024
        print(f"  ✓ Saved {output_path.name} ({file_size:.1f}KB)")


def load_prompts(prompts_file):
    """Load prompts from JSON file."""
    try:
        with open(prompts_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading prompts: {e}")
        sys.exit(1)


def generate_category(client, category_data, output_dir, delay=2):
    """
    Generate all images for a category.

    Args:
        client: Gemini API client
        category_data: Dictionary with prompts and filenames
        output_dir: Output directory path
        delay: Delay between API calls (seconds)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    total = len(category_data.get('items', []))
    print(f"\n{'='*60}")
    print(f"Generating {total} images for: {category_data.get('name', 'Unknown')}")
    print(f"Output: {output_path}")
    print(f"{'='*60}\n")

    success_count = 0
    skip_count = 0
    fail_count = 0

    for idx, item in enumerate(category_data.get('items', []), 1):
        print(f"[{idx}/{total}] {item['name']}")

        output_file = output_path / item['filename']

        # Check if already exists (skip regeneration)
        if output_file.with_suffix('.png').exists():
            print(f"  ⚠ File exists, skipping (delete to regenerate)")
            skip_count += 1
            continue

        # Generate image
        image = generate_image(client, item['prompt'])

        if image:
            # Remove background
            image = remove_background(image)

            # Optimize
            image = optimize_image(image)

            # Save in multiple formats
            save_image(image, str(output_file), formats=['png', 'webp'])

            success_count += 1

            # Rate limiting delay
            if idx < total:
                print(f"  ⏳ Waiting {delay}s before next generation...")
                time.sleep(delay)
        else:
            fail_count += 1

        print()

    print(f"{'='*60}")
    print(f"✓ Completed {category_data.get('name', 'category')}")
    print(f"  Success: {success_count}, Skipped: {skip_count}, Failed: {fail_count}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Generate AI images for toddler games'
    )
    parser.add_argument(
        '--category',
        type=str,
        default='all',
        help='Category to generate (all, animals, food, shapes, balloons, backgrounds)'
    )
    parser.add_argument(
        '--prompts',
        type=str,
        default='scripts/prompts.json',
        help='Path to prompts JSON file'
    )
    parser.add_argument(
        '--delay',
        type=int,
        default=2,
        help='Delay between API calls in seconds'
    )

    args = parser.parse_args()

    print("🎨 AI Image Generator for Toddler Games")
    print("=" * 60)
    print("Model: gemini-2.5-flash-image")
    print("=" * 60)

    # Create API client
    client = create_client()

    # Load prompts
    prompts = load_prompts(args.prompts)

    # Determine which categories to generate
    if args.category == 'all':
        categories = prompts.keys()
    else:
        if args.category not in prompts:
            print(f"Error: Category '{args.category}' not found in prompts")
            print(f"Available: {', '.join(prompts.keys())}")
            sys.exit(1)
        categories = [args.category]

    # Generate images for each category
    for category in categories:
        category_data = prompts[category]
        output_dir = f"images/{category}"
        generate_category(client, category_data, output_dir, delay=args.delay)

    print("=" * 60)
    print("✓ All images generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
