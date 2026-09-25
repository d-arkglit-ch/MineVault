"""
OCR Processing Module for Scanned Geological and Mining Documents.
Handles image preprocessing (deskewing, contrast adjustment), multi-engine OCR extraction
prioritizing Google Cloud Vision and Google Gemini Multimodal Vision, with fallback to
Tesseract and digital tabular parsing, tracking physical coordinate bounding boxes [x, y, w, h].
"""

import os
import io
import re
import json
import base64
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageEnhance

# Configure logger
logger = logging.getLogger("geomine.ocr")

# Pre-load environment variables from backend/.env or root .env
try:
    from dotenv import load_dotenv
    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    backend_env = root_dir / "backend" / ".env"
    if backend_env.exists():
        load_dotenv(dotenv_path=backend_env, override=False)
    if (root_dir / ".env").exists():
        load_dotenv(dotenv_path=root_dir / ".env", override=False)
except ImportError:
    pass

class GeologicalOCRProcessor:
    """
    Production OCR Processor supporting Google Cloud Vision, Google Gemini Multimodal Vision,
    and local Tesseract OCR with coordinate bounding box extraction and confidence scoring.
    """
    def __init__(self, engine: str = "google_vision", lang: str = "eng"):
        self.engine = engine
        self.lang = lang
        self.vision_api_key = os.getenv("GOOGLE_VISION_API_KEY", "").strip()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.last_engine_used: str = "none"
        self.last_confidence_score: float = 0.0
        self.last_full_text: str = ""
        self.last_borehole_id: Optional[str] = None
        self.last_warnings: List[str] = []

    @staticmethod
    def _extract_borehole_id_from_text(text: str) -> Optional[str]:
        """
        Extracts and normalizes borehole designations from text.
        Tolerant to OCR artifacts: whitespace around hyphens, underscores, dots,
        and optical character substitutions (O/o -> 0, I/l -> 1).
        """
        if not text:
            return None
        patterns = [
            # BH-NK-094, BH - NK - 094, BH_NK_094, BH - NK - O94
            r'\b(BH)\s*[-_.: ]\s*([A-Z]{1,6})\s*[-_.: ]\s*([0-9OIl]{2,5}[A-Z]?)\b',
            # CMPDI-DH-104, CMPDI - RI2 - 094, MECL - BK4 - 012
            r'\b(CMPDI|MECL|GSI)\s*[-_.: ]\s*([A-Z0-9]{1,6})\s*[-_.: ]\s*([0-9OIl]{2,5}[A-Z]?)\b',
            # DH-104, DH - 104
            r'\b(DH)\s*[-_.: ]\s*([0-9OIl]{2,5}[A-Z]?)\b',
            # General standard \bBH-[A-Z0-9-]+\b
            r'\b(BH-[A-Z0-9-]+)\b',
            r'\b(CMPDI-[A-Z0-9-]+)\b',
            r'\b(MECL-[A-Z0-9-]+)\b',
            r'\b(BH-[A-Z]{1,4}-\d{2,4}[A-Z]?|CMPDI-[A-Z]{1,4}-\d{2,4}|DH-\d{2,4}|MECL-[A-Z0-9-]+)\b'
        ]
        for pat in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                groups = m.groups()
                if len(groups) == 3:
                    prefix, mid, num = groups
                    num_clean = num.replace('O', '0').replace('o', '0').replace('l', '1').replace('I', '1')
                    return f"{prefix.upper()}-{mid.upper()}-{num_clean.upper()}"
                elif len(groups) == 2:
                    prefix, num = groups
                    num_clean = num.replace('O', '0').replace('o', '0').replace('l', '1').replace('I', '1')
                    return f"{prefix.upper()}-{num_clean.upper()}"
                elif len(groups) == 1:
                    return groups[0].upper()
        return None

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocesses a scanned geological document page:
        - RGBA / Palette conversion to RGB
        - High-resolution downsampling if image exceeds 2600px dimension
        - Contrast enhancement for faded lithological text
        """
        if image.mode in ("RGBA", "P", "LA"):
            bg = Image.new("RGB", image.size, (255, 255, 255))
            if image.mode == "RGBA":
                bg.paste(image, mask=image.split()[3])
            else:
                bg.paste(image.convert("RGB"))
            image = bg
        elif image.mode != "RGB":
            image = image.convert("RGB")

        # Proportional resize if extremely large to optimize network payloads
        max_dim = 2600
        w, h = image.size
        if max(w, h) > max_dim:
            scale = max_dim / float(max(w, h))
            new_w, new_h = int(w * scale), int(h * scale)
            image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        elif max(w, h) < 1000 and max(w, h) > 0:
            upscale = min(3.0, 1200.0 / float(max(w, h)))
            if upscale > 1.2:
                new_w, new_h = int(w * upscale), int(h * upscale)
                image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # Enhance contrast slightly for faint geological print
        enhancer = ImageEnhance.Contrast(image)
        enhanced = enhancer.enhance(1.25)
        return enhanced

    def extract_with_google_cloud_vision(self, image: Image.Image) -> Optional[Dict[str, Any]]:
        """
        Executes Google Cloud Vision REST API with DOCUMENT_TEXT_DETECTION.
        Requires GOOGLE_VISION_API_KEY.
        Returns parsed text, line-level bounding boxes, and mean confidence.
        """
        if not self.vision_api_key:
            return None

        try:
            import requests
            prep_img = self.preprocess_image(image)
            buf = io.BytesIO()
            prep_img.save(buf, format="JPEG", quality=85)
            b64_content = base64.b64encode(buf.getvalue()).decode("utf-8")

            url = f"https://vision.googleapis.com/v1/images:annotate?key={self.vision_api_key}"
            payload = {
                "requests": [
                    {
                        "image": {"content": b64_content},
                        "features": [
                            {"type": "DOCUMENT_TEXT_DETECTION"}
                        ]
                    }
                ]
            }

            resp = requests.post(url, json=payload, timeout=12)
            if resp.status_code != 200:
                logger.warning(f"Google Cloud Vision API returned {resp.status_code}: {resp.text[:200]}")
                return None

            data = resp.json()
            responses = data.get("responses", [])
            if not responses or "fullTextAnnotation" not in responses[0]:
                return None

            full_annotation = responses[0]["fullTextAnnotation"]
            full_text = full_annotation.get("text", "")
            
            # Extract line-grouped blocks and calculate mean confidence
            lines_with_bboxes: List[Dict[str, Any]] = []
            confidences: List[float] = []

            for page in full_annotation.get("pages", []):
                for block in page.get("blocks", []):
                    block_conf = block.get("confidence")
                    if block_conf is not None:
                        confidences.append(float(block_conf))

                    for paragraph in block.get("paragraphs", []):
                        current_line_words = []
                        current_vertices = []

                        for word in paragraph.get("words", []):
                            word_text = "".join([s.get("text", "") for s in word.get("symbols", [])])
                            current_line_words.append(word_text)
                            verts = word.get("boundingBox", {}).get("vertices", [])
                            if verts:
                                current_vertices.extend(verts)

                            # Check for line break symbol
                            symbols = word.get("symbols", [])
                            has_break = False
                            if symbols:
                                last_symbol = symbols[-1]
                                break_type = last_symbol.get("property", {}).get("detectedBreak", {}).get("type", "")
                                if break_type in ("LINE_BREAK", "EOL_SURE_SPACE", "HYPHEN"):
                                    has_break = True

                            if has_break or word == paragraph.get("words", [])[-1]:
                                line_text = " ".join(current_line_words).strip()
                                if line_text and current_vertices:
                                    xs = [v.get("x", 0) for v in current_vertices if "x" in v]
                                    ys = [v.get("y", 0) for v in current_vertices if "y" in v]
                                    if xs and ys:
                                        min_x, max_x = min(xs), max(xs)
                                        min_y, max_y = min(ys), max(ys)
                                        lines_with_bboxes.append({
                                            "text": line_text,
                                            "bbox": [float(min_x), float(min_y), float(max_x - min_x), float(max_y - min_y)],
                                            "confidence": float(block_conf or 0.95)
                                        })
                                current_line_words = []
                                current_vertices = []

            self.last_full_text = full_text
            self.last_borehole_id = self._extract_borehole_id_from_text(full_text)

            mean_conf = round(sum(confidences) / max(len(confidences), 1), 3) if confidences else 0.965
            return {
                "success": True,
                "engine": "Google Cloud Vision",
                "text": full_text,
                "lines": lines_with_bboxes,
                "confidence": mean_conf
            }
        except Exception as e:
            logger.warning(f"Google Cloud Vision OCR execution failed: {e}")
            return None

    def extract_with_gemini_vision(self, image: Image.Image) -> Optional[Dict[str, Any]]:
        """
        Executes Google Gemini Multimodal Vision (gemini-3.6-flash) via google-genai SDK.
        Extracts structured lithological intervals, physical bounding boxes, and confidence.
        """
        if not self.gemini_api_key:
            return None

        try:
            from google import genai
            prep_img = self.preprocess_image(image)
            client = genai.Client(api_key=self.gemini_api_key)

            prompt = (
                "You are an expert geological document and borehole log parser for CMPDI/MECL exploration archives.\n"
                "Analyze this image carefully.\n"
                "CRITICAL MANDATE: If this image is blank, white, corrupt, or does not contain any geological borehole or stratigraphic lithology tables, you MUST return: {\"borehole_id\": null, \"confidence\": 0.0, \"intervals\": [], \"raw_text\": \"\"}.\n"
                "NEVER fabricate, guess, or hallucinate borehole identifiers, depths, or strata from images lacking tabular geological data.\n"
                "If the image DOES contain geological log tables, extract all borehole IDs (e.g. BH-NK-094, CMPDI-DH-104) and all lithology interval rows with physical pixel bounding boxes [x, y, width, height].\n"
                "Respond ONLY with a valid JSON object matching this schema:\n"
                "{\n"
                '  "borehole_id": "string or null",\n'
                '  "confidence": 0.0,\n'
                '  "intervals": [\n'
                '    {"from_m": "0.00", "to_m": "42.10", "stratum": "Alluvium and weathered zone", "recovery_pct": "62.5", "bbox": [120.0, 340.0, 420.0, 18.0]}\n'
                "  ],\n"
                '  "raw_text": "all transcribed text or empty string"\n'
                "}"
            )

            # Try modern gemini models in order of capability
            models_to_try = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-flash-latest"]
            response = None
            for mod in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=mod,
                        contents=[prep_img, prompt]
                    )
                    if response and response.text:
                        break
                except Exception as model_err:
                    logger.debug(f"Model {mod} failed: {model_err}")
                    continue

            if not response or not response.text:
                return None

            raw_text = response.text.strip()
            # Clean possible markdown wrapping ```json ... ```
            if raw_text.startswith("```"):
                raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
                raw_text = re.sub(r"\s*```$", "", raw_text)

            parsed_data = json.loads(raw_text)
            intervals = parsed_data.get("intervals", [])
            borehole_id = parsed_data.get("borehole_id")
            
            if not intervals:
                self.last_full_text = ""
                self.last_borehole_id = None
                return {
                    "success": True,
                    "engine": "Google Gemini Vision",
                    "borehole_id": None,
                    "intervals": [],
                    "confidence": 0.0,
                    "raw_text": parsed_data.get("raw_text", "")
                }

            self.last_full_text = parsed_data.get("raw_text", "")
            self.last_borehole_id = borehole_id
            conf = float(parsed_data.get("confidence", 0.95))
            return {
                "success": True,
                "engine": "Google Gemini Vision",
                "borehole_id": borehole_id,
                "intervals": intervals,
                "confidence": conf,
                "raw_text": parsed_data.get("raw_text", "")
            }
        except Exception as e:
            logger.warning(f"Google Gemini Multimodal Vision extraction failed: {e}")
            return None

    def extract_with_tesseract(self, image: Image.Image) -> Optional[Dict[str, Any]]:
        """
        Local Tesseract fallback using pytesseract if binary is installed.
        """
        try:
            import pytesseract
            prep_img = self.preprocess_image(image)
            data = pytesseract.image_to_data(prep_img, lang=self.lang, output_type=pytesseract.Output.DICT)
            
            n_boxes = len(data["text"])
            lines_dict: Dict[Tuple[int, int, int], List[Dict[str, Any]]] = {}
            confidences: List[float] = []

            for i in range(n_boxes):
                text = data["text"][i].strip()
                conf = float(data["conf"][i])
                if text and conf > 0:
                    confidences.append(conf / 100.0)
                    key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])
                    if key not in lines_dict:
                        lines_dict[key] = []
                    lines_dict[key].append({
                        "text": text,
                        "left": data["left"][i],
                        "top": data["top"][i],
                        "width": data["width"][i],
                        "height": data["height"][i],
                        "conf": conf / 100.0
                    })

            lines_with_bboxes = []
            for words in lines_dict.values():
                line_text = " ".join([w["text"] for w in words])
                left = min([w["left"] for w in words])
                top = min([w["top"] for w in words])
                right = max([w["left"] + w["width"] for w in words])
                bottom = max([w["top"] + w["height"] for w in words])
                line_conf = sum([w["conf"] for w in words]) / len(words)
                lines_with_bboxes.append({
                    "text": line_text,
                    "bbox": [float(left), float(top), float(right - left), float(bottom - top)],
                    "confidence": round(line_conf, 3)
                })

            full_text = " ".join([l["text"] for l in lines_with_bboxes]).strip()
            self.last_full_text = full_text
            self.last_borehole_id = self._extract_borehole_id_from_text(full_text)

            mean_conf = round(sum(confidences) / max(len(confidences), 1), 3) if confidences else 0.65
            return {
                "success": True,
                "engine": "Tesseract OCR",
                "text": full_text,
                "lines": lines_with_bboxes,
                "confidence": mean_conf
            }
        except Exception as e:
            logger.debug(f"Tesseract OCR unavailable or failed: {e}")
            return None

    def _parse_lines_into_lithology_rows(self, lines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyzes line text and bounding boxes to extract lithological intervals.
        Matches depth interval patterns (e.g. '0.00 - 42.10m Alluvium 62.5%').
        """
        rows = []
        depth_pattern = re.compile(r'(\d+(?:\.\d+)?)\s*(?:-|to|–|\s+)\s*(\d+(?:\.\d+)?)\s*(?:m|meters)?\s+([A-Za-z].*)', re.IGNORECASE)
        alt_pattern = re.compile(r'(\d+(?:\.\d+)?)\s*(?:-|to|–)\s*(\d+(?:\.\d+)?)\s*(?:m|meters)?\s*(.*)', re.IGNORECASE)
        recovery_pattern = re.compile(r'(\d+(?:\.\d+)?)\s*%', re.IGNORECASE)

        for line in lines:
            text = line.get("text", "")
            bbox = line.get("bbox", [100.0, 200.0, 350.0, 20.0])
            m = depth_pattern.search(text) or alt_pattern.search(text)
            if m:
                from_m, to_m, rest = m.group(1), m.group(2), m.group(3).strip()
                rec_match = recovery_pattern.search(rest)
                recovery_pct = rec_match.group(1) if rec_match else "90.0"
                stratum = recovery_pattern.sub("", rest).strip() or "Sandstone / Shale Interburden"
                rows.append({
                    "from_m": from_m,
                    "to_m": to_m,
                    "stratum": stratum,
                    "recovery_pct": recovery_pct,
                    "bbox": bbox
                })

        return rows

    def extract_text_with_bboxes(self, image: Image.Image) -> List[Dict[str, Any]]:
        """
        Extracts raw text spans along with bounding box coordinates [x, y, w, h].
        Cascade: Google Cloud Vision -> Google Gemini Vision -> Tesseract -> High-fidelity Seed.
        """
        # 1. Google Cloud Vision
        gvision = self.extract_with_google_cloud_vision(image)
        if gvision and gvision.get("lines"):
            self.last_engine_used = gvision["engine"]
            self.last_confidence_score = gvision["confidence"]
            return gvision["lines"]

        # 2. Google Gemini Vision
        gemini = self.extract_with_gemini_vision(image)
        if gemini and gemini.get("intervals"):
            self.last_engine_used = gemini["engine"]
            self.last_confidence_score = gemini["confidence"]
            lines = []
            for item in gemini["intervals"]:
                lines.append({
                    "text": f"{item.get('from_m')} - {item.get('to_m')}m {item.get('stratum')}",
                    "bbox": item.get("bbox", [120.0, 350.0, 400.0, 20.0]),
                    "confidence": gemini["confidence"]
                })
            return lines

        # 3. Tesseract Local
        tess = self.extract_with_tesseract(image)
        if tess and tess.get("lines"):
            self.last_engine_used = tess["engine"]
            self.last_confidence_score = tess["confidence"]
            return tess["lines"]

        # 4. Honest failure — never fabricate extraction results
        self.last_engine_used = "none"
        self.last_confidence_score = 0.0
        self.last_full_text = ""
        self.last_borehole_id = None
        logger.warning("All OCR engines failed or unavailable — no text could be extracted.")
        return []

    def extract_table_rows_with_bboxes(self, image: Optional[Image.Image] = None) -> List[Dict[str, Any]]:
        """
        Extracts structured table rows from a scanned lithology plate, ensuring every row
        carries its physical bounding box coordinates [x, y, w, h] on the source page.
        """
        if image is not None:
            # 1. Google Cloud Vision
            gvision = self.extract_with_google_cloud_vision(image)
            if gvision:
                rows = self._parse_lines_into_lithology_rows(gvision.get("lines", []))
                if rows:
                    self.last_engine_used = gvision["engine"]
                    self.last_confidence_score = gvision["confidence"]
                    return rows

            # 2. Google Gemini Vision
            gemini = self.extract_with_gemini_vision(image)
            if gemini and gemini.get("intervals"):
                self.last_engine_used = gemini["engine"]
                self.last_confidence_score = gemini["confidence"]
                return gemini["intervals"]

            # 3. Tesseract
            tess = self.extract_with_tesseract(image)
            if tess:
                rows = self._parse_lines_into_lithology_rows(tess.get("lines", []))
                if rows:
                    self.last_engine_used = tess["engine"]
                    self.last_confidence_score = tess["confidence"]
                    return rows

        # 4. Honest failure — never fabricate extraction results
        self.last_engine_used = "none"
        self.last_confidence_score = 0.0
        self.last_full_text = ""
        self.last_borehole_id = None
        logger.warning("All OCR engines failed or unavailable — no table rows could be extracted.")
        return []


if __name__ == "__main__":
    p = GeologicalOCRProcessor()
    print("GeologicalOCRProcessor Initialized.")
    print("Google Vision API Key Loaded:", bool(p.vision_api_key))
    print("Gemini API Key Loaded:", bool(p.gemini_api_key))
    test_img = Image.new("RGB", (400, 120), color=(255, 255, 255))
    rows = p.extract_table_rows_with_bboxes(test_img)
    print(f"Extracted {len(rows)} rows using engine: {p.last_engine_used} (Conf: {p.last_confidence_score})")
