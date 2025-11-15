# AI Image Generation for Toddler Games

This directory contains scripts for generating AI images to enrich the toddler games using Image Router API.

## Overview

The games are enhanced with AI-generated images instead of emojis and SVG graphics. Images are generated using Image Router API (supporting multiple AI models like Flux, DALL-E, Stable Diffusion, etc.) with automatic background removal.

## Files

- `generate_images.py` - Main image generation script
- `prompts.json` - Image prompts for all game assets
- `requirements.txt` - Python dependencies

## Setup

### Local Generation

1. Install dependencies:
```bash
pip install -r scripts/requirements.txt
```

2. Set your API key:
```bash
export IMAGE_ROUTER_API_KEY="your-api-key-here"
```

3. Generate images:
```bash
# Generate all images (default model: black-forest-labs/FLUX-1-schnell:free)
python scripts/generate_images.py --category all

# Generate specific category
python scripts/generate_images.py --category animals

# Custom delay between API calls
python scripts/generate_images.py --category food --delay 3

# Specify a different model
python scripts/generate_images.py --category shapes --model "dall-e-3"
```

### GitHub Actions

Images can be generated automatically using GitHub Actions:

1. Add `IMAGE_ROUTER_API_KEY` to repository secrets:
   - Go to Settings → Secrets and variables → Actions
   - Add new secret: `IMAGE_ROUTER_API_KEY`

2. Run workflow:
   - Go to Actions tab
   - Select "Generate AI Game Images"
   - Click "Run workflow"
   - Choose category, delay, and model
   - Click "Run workflow"

3. Generated images will be committed automatically

## Categories

- **animals**: Cute animals for the feeding game (rabbit, dog, cat, bear, elephant, monkey)
- **food**: Food items for feeding game (carrot, lettuce, fish, honey, etc.)
- **shapes**: Geometric shapes (circle, square, triangle, star, heart, pentagon)
- **balloons**: Colorful balloons for balloon popping game
- **backgrounds**: Background images for various games
- **all**: Generate all categories

## Image Specifications

- **API**: Image Router (supports multiple models)
- **Default Model**: black-forest-labs/FLUX-1-schnell:free (can be changed with --model flag)
- **Available Models**: FLUX-1-schnell (free), dall-e-3, stable-diffusion-3, and more
- **Format**: PNG and WebP (dual format for compatibility)
- **Background**: Transparent (removed automatically using rembg)
- **Style**: Sticker-like, toddler-friendly cartoon style
- **Size**: Optimized (max 1024px dimension)
- **Location**: `/images/{category}/{filename}.{ext}`

## Adding New Prompts

Edit `prompts.json` and add new items:

```json
{
  "category_name": {
    "name": "Display Name",
    "items": [
      {
        "name": "Item Name",
        "filename": "output-filename",
        "prompt": "generate a small image of... - sticker like but without borders - on green screen like background..."
      }
    ]
  }
}
```

## Best Practices

1. **Review Generated Images**: Always review AI-generated images for appropriateness (toddler audience)
2. **Consistency**: Use consistent prompt style for visual coherence
3. **Rate Limiting**: Use appropriate delays (2-3 seconds) to avoid API limits
4. **Manual Selection**: Generate multiple variations if needed and select the best
5. **Commit Review**: Review images before committing to repository

## Costs

- Image Router: Pay-as-you-go pricing (check current rates at imagerouter.io)
- Different models have different costs (Flux Pro, DALL-E 3, etc.)
- Expected usage: ~50-70 images total for all games

## Troubleshooting

**Error: IMAGE_ROUTER_API_KEY not set**
- Set environment variable: `export IMAGE_ROUTER_API_KEY="your-key"`

**Error: rembg not available**
- Install: `pip install rembg`
- Background removal will be skipped if not available

**API Rate Limits**
- Increase `--delay` parameter
- Generate categories separately instead of "all"

**Image Quality Issues**
- Adjust prompts in `prompts.json`
- Regenerate by deleting existing images

## License

Generated images are subject to Image Router's terms of service and the underlying AI model's licensing terms. Verify licensing for your use case.
