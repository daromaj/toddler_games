#!/usr/bin/env python3
"""
Generate AI images for toddler games using Google Gemini/Imagen API.
Includes automatic background removal and optimization.
"""

import google.generativeai as genai
import os
import sys
import json
import argparse
from PIL import Image
from pathlib import Path
import io
import time
import base64

try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    print("Warning: rembg not available. Background removal will be skipped.")
    print("Install with: pip install rembg")


def configure_gemini():
    """Configure Gemini API with error handling."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        sys.exit(1)

    genai.configure(api_key=api_key)
    print("✓ Gemini API configured")


def generate_image(prompt, model_name="imagen-3.0-generate-001"):
    """
    Generate an image using Google's AI API.

    This function tries multiple approaches to generate images as the API
    has been evolving.

    Args:
        prompt: Text description of the image to generate
        model_name: Model to use for generation

    Returns:
        PIL Image object or None on failure
    """
    try:
        print(f"  Generating: {prompt[:60]}...")

        # Method 1: Try using generate_images from genai module directly
        try:
            response = genai.generate_images(
                model=model_name,
                prompt=prompt,
                number_of_images=1
            )

            if response and hasattr(response, 'images') and response.images:
                # Extract image bytes
                img_data = response.images[0]

                # Handle different response formats
                if hasattr(img_data, '_image_bytes'):
                    image_bytes = img_data._image_bytes
                elif hasattr(img_data, 'data'):
                    image_bytes = img_data.data
                else:
                    # Try to get image data directly
                    image_bytes = img_data

                image = Image.open(io.BytesIO(image_bytes))
                print(f"  ✓ Generated {image.size[0]}x{image.size[1]} image")
                return image

        except AttributeError as e:
            print(f"  ⚠ Method 1 failed: {e}")

        # Method 2: Try using ImageGenerationModel
        try:
            print(f"  Trying ImageGenerationModel...")
            model = genai.ImageGenerationModel(model_name)
            result = model.generate_images(prompt=prompt)

            if result:
                if hasattr(result, 'images'):
                    img_bytes = result.images[0]._image_bytes
                else:
                    img_bytes = result[0]._image_bytes

                image = Image.open(io.BytesIO(img_bytes))
                print(f"  ✓ Generated {image.size[0]}x{image.size[1]} image")
                return image

        except (AttributeError, TypeError) as e:
            print(f"  ⚠ Method 2 failed: {e}")

        # Method 3: Try text-to-image with GenerativeModel asking for base64
        try:
            print(f"  Trying text-based generation request...")

            text_model = genai.GenerativeModel('gemini-2.0-flash-exp')

            # Ask the model to describe how to generate the image
            # This is a workaround - we'll use another service if this doesn't work
            enhanced_prompt = f"""I need to generate an image with these specifications:
{prompt}

Please provide a very detailed, comprehensive description suitable for an AI image generator,
including: style, colors, composition, lighting, and specific visual details.
Make it very specific and detailed for best results."""

            response = text_model.generate_content(enhanced_prompt)

            # This won't actually generate an image, but gives us enhanced prompt
            # We'll need to use a different service
            print(f"  ℹ️  Text model response received (but can't generate images)")
            print(f"  ✗ Gemini text models cannot generate images directly")
            return None

        except Exception as e:
            print(f"  ⚠ Method 3 failed: {e}")

        print(f"  ✗ All generation methods failed")
        print(f"  ℹ️  The Google GenAI API structure may have changed.")
        print(f"  ℹ️  You may need to:")
        print(f"     1. Use Vertex AI instead of the genai library")
        print(f"     2. Use a different image generation service (DALL-E, Stable Diffusion)")
        print(f"     3. Check Google AI Studio for the latest API documentation")

        return None

    except Exception as e:
        print(f"  ✗ Error generating image: {e}")
        print(f"  ℹ️  Error type: {type(e).__name__}")
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


def generate_category(category_data, output_dir, delay=2):
    """
    Generate all images for a category.

    Args:
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
        image = generate_image(item['prompt'])

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
    parser.add_argument(
        '--model',
        type=str,
        default='imagen-3.0-generate-001',
        help='Model name to use for generation'
    )

    args = parser.parse_args()

    print("🎨 AI Image Generator for Toddler Games")
    print("=" * 60)
    print(f"Model: {args.model}")
    print("=" * 60)

    # Configure API
    configure_gemini()

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
        generate_category(category_data, output_dir, delay=args.delay)

    print("=" * 60)
    print("Image generation process completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
