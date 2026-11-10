import unittest
from io import BytesIO

from PIL import Image

from enhancer import _scale_to_target_long_side, enhance_image_bytes


class EnhancerTests(unittest.TestCase):
    def test_scale_keeps_aspect_ratio(self):
        self.assertEqual(_scale_to_target_long_side(200, 100, 1000), (1000, 500))

    def test_scale_does_not_downsize(self):
        self.assertEqual(_scale_to_target_long_side(4000, 2000, 3840), (4000, 2000))

    def test_enhance_returns_valid_jpeg(self):
        image = Image.new("RGB", (64, 64), color=(120, 100, 200))
        src = BytesIO()
        image.save(src, format="PNG")

        enhanced = enhance_image_bytes(src.getvalue(), target_long_side=256)
        out = Image.open(BytesIO(enhanced))

        self.assertEqual(out.format, "JPEG")
        self.assertEqual(max(out.size), 256)


if __name__ == "__main__":
    unittest.main()
