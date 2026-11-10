from io import BytesIO

from PIL import Image, ImageEnhance, ImageFilter, ImageOps, UnidentifiedImageError


def _scale_to_target_long_side(width: int, height: int, target_long_side: int) -> tuple[int, int]:
    long_side = max(width, height)
    if long_side <= 0:
        raise ValueError("Invalid image dimensions.")

    if long_side >= target_long_side:
        return width, height

    ratio = target_long_side / long_side
    return int(width * ratio), int(height * ratio)


def enhance_image_bytes(image_bytes: bytes, target_long_side: int = 3840) -> bytes:
    if not image_bytes:
        raise ValueError("Uploaded image is empty.")

    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except UnidentifiedImageError as exc:
        raise ValueError("Uploaded file is not a valid image.") from exc

    image = ImageOps.exif_transpose(image)
    image = image.filter(ImageFilter.MedianFilter(size=3))
    image = ImageOps.autocontrast(image, cutoff=1)
    image = ImageEnhance.Color(image).enhance(1.03)

    new_size = _scale_to_target_long_side(image.width, image.height, target_long_side)
    if new_size != image.size:
        image = image.resize(new_size, Image.Resampling.LANCZOS)

    image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=125, threshold=2))

    output = BytesIO()
    image.save(output, format="JPEG", quality=95, optimize=True)
    return output.getvalue()
