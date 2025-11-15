#!/usr/bin/env python3
"""
Generate AI images for toddler games using Image Router API.
Includes automatic background removal and optimization.
"""

import requests
import os
import sys
import json
import argparse
from PIL import Image
from pathlib import Path
import time
import io
from base64 import b64decode

try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    print("Warning: rembg not available. Background removal will be skipped.")
    print("Install with: pip install rembg")


def get_api_key():
    """Get Image Router API key from environment with error handling."""
    api_key = os.environ.get("IMAGE_ROUTER_API_KEY")
    if not api_key:
        print("Error: IMAGE_ROUTER_API_KEY environment variable not set")
        sys.exit(1)

    print("✓ Image Router API configured")
    return api_key


def generate_image(api_key, prompt, model_name="black-forest-labs/FLUX-1-schnell:free"):
    """
    Generate an image using Image Router API.

    Args:
        api_key: Image Router API key
        prompt: Text description of the image to generate
        model_name: Model to use for image generation
                   (default: black-forest-labs/FLUX-1-schnell:free)

    Returns:
        PIL Image object or None on failure
    """
    try:
        print(f"  Generating: {prompt[:60]}...")

        url = "https://api.imagerouter.io/v1/openai/images/generations"
        payload = {
            "prompt": prompt,
            "model": model_name,
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        response_data = response.json()

        # Extract image from OpenAI-compatible response format
        if "data" in response_data and len(response_data["data"]) > 0:
            image_data = response_data["data"][0]

            # Handle base64 encoded image
            if "b64_json" in image_data:
                image_bytes = b64decode(image_data["b64_json"])
                image = Image.open(io.BytesIO(image_bytes))
                print(f"  ✓ Generated {image.size[0]}x{image.size[1]} image")
                return image

            # Handle URL response
            elif "url" in image_data:
                image_url = image_data["url"]
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                image = Image.open(io.BytesIO(image_response.content))
                print(f"  ✓ Generated {image.size[0]}x{image.size[1]} image")
                return image

        print(f"  ✗ No image data in response")
        return None

    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error generating image: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                print(f"  Response: {e.response.json()}")
            except:
                print(f"  Response: {e.response.text}")
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


def generate_category(api_key, category_data, output_dir, delay=2, model_name="black-forest-labs/FLUX-1-schnell:free"):
    """
    Generate all images for a category.

    Args:
        api_key: Image Router API key
        category_data: Dictionary with prompts and filenames
        output_dir: Output directory path
        delay: Delay between API calls (seconds)
        model_name: Model to use for image generation
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
        image = generate_image(api_key, item['prompt'], model_name)

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
        description='Generate AI images for toddler games using Image Router'
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
    parser.add_argument(
        '--model',
        type=str,
        default='black-forest-labs/FLUX-1-schnell:free',
        help='Image generation model to use (default: black-forest-labs/FLUX-1-schnell:free)'
    )

    args = parser.parse_args()

    print("🎨 AI Image Generator for Toddler Games")
    print("=" * 60)
    print(f"Model: {args.model}")
    print("=" * 60)

    # Get API key
    api_key = get_api_key()

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
        generate_category(api_key, category_data, output_dir, delay=args.delay, model_name=args.model)

    print("=" * 60)
    print("✓ All images generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
