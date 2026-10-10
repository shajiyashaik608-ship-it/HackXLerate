import re
from datetime import date, datetime
from typing import List, Dict, Any, Optional, Tuple
from app.core.logging import logger

SUPPORTED_TARGET_TESTS = {
    "TSH": {
        "canonical_name": "TSH",
        "aliases": ["tsh", "thyroid stimulating hormone", "ultra sensitive tsh", "s. tsh"],
        "default_unit": "mIU/L",
        "explanation": "Thyroid Stimulating Hormone regulates metabolic rate and ovulatory timing. Borderline elevations are common and warrant clinical review."
    },
    "Fasting Insulin": {
        "canonical_name": "Fasting Insulin",
        "aliases": ["fasting insulin", "serum insulin", "insulin fasting", "s. insulin"],
        "default_unit": "uIU/mL",
        "explanation": "Measures baseline insulin secretion. Elevated fasting levels can reflect cellular insulin resistance, a cornerstone of PCOS."
    },
    "LH": {
        "canonical_name": "LH",
        "aliases": ["lh", "luteinizing hormone", "s. lh"],
        "default_unit": "mIU/mL",
        "explanation": "Luteinizing Hormone signals the ovary to trigger ovulation. Ratios relative to FSH provide helpful clinical context."
    },
    "FSH": {
        "canonical_name": "FSH",
        "aliases": ["fsh", "follicle stimulating hormone", "s. fsh"],
        "default_unit": "mIU/mL",
        "explanation": "Follicle Stimulating Hormone fosters the maturation of ovarian follicles prior to egg release."
    },
    "Total Testosterone": {
        "canonical_name": "Total Testosterone",
        "aliases": ["total testosterone", "serum testosterone", "testosterone total", "s. testosterone"],
        "default_unit": "ng/dL",
        "explanation": "Primary androgen in female physiology. Elevated androgen levels may contribute to hirsutism, cystic acne, or cycle delay."
    },
    "HbA1c": {
        "canonical_name": "HbA1c",
        "aliases": ["hba1c", "glycated hemoglobin", "glycosylated hemoglobin", "a1c"],
        "default_unit": "%",
        "explanation": "Reflects weighted average blood glucose over roughly 90 days, assessing glycemic stability."
    },
    "Fasting Blood Sugar": {
        "canonical_name": "Fasting Blood Sugar",
        "aliases": ["fasting blood sugar", "fasting glucose", "fbs", "fasting plasma glucose"],
        "default_unit": "mg/dL",
        "explanation": "Morning fasting blood sugar screens for impaired fasting glucose and informs nutritional guidance."
    }
}


class ExtractionService:
    """
    Analyzes raw OCR or PDF text to identify target biomarkers, values,
    extracted lab reference intervals, and test dates without fabrication.
    """

    def extract_test_date(self, text: str) -> Optional[date]:
        """Attempts to locate document collection or reporting date."""
        date_patterns = [
            r"\b(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})\b",  # DD/MM/YYYY or MM/DD/YYYY
            r"\b(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})\b",  # YYYY-MM-DD
            r"\b(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]+(\d{4})\b"
        ]

        for pat in date_patterns:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                groups = match.groups()
                try:
                    if len(groups) == 3:
                        if len(groups[0]) == 4:  # YYYY-MM-DD
                            return date(int(groups[0]), int(groups[1]), int(groups[2]))
                        elif groups[1].isdigit():  # DD-MM-YYYY
                            # Assume DD-MM-YYYY in Indian laboratory convention
                            day, month, year = int(groups[0]), int(groups[1]), int(groups[2])
                            if month > 12 and day <= 12:
                                day, month = month, day
                            return date(year, month, day)
                except ValueError:
                    continue
        return None

    def extract_biomarkers(
        self,
        pages_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Parses pages to discover target analytes, values, units, and laboratory reference ranges.
        """
        results: List[Dict[str, Any]] = []
        seen_canonical: set = set()

        for page in pages_data:
            page_num = page.get("page_number", 1)
            page_text = page.get("text", "")
            lines = page_text.splitlines()

            for line_idx, line in enumerate(lines):
                line_lower = line.lower()

                for key, meta in SUPPORTED_TARGET_TESTS.items():
                    canonical = meta["canonical_name"]
                    if canonical in seen_canonical:
                        continue

                    # Check if line matches test alias
                    alias_match = any(re.search(rf"\b{re.escape(alias)}\b", line_lower) for alias in meta["aliases"])
                    if not alias_match:
                        continue

                    # Search within line or neighboring lines for value & range
                    search_chunk = " ".join(lines[max(0, line_idx - 1): min(len(lines), line_idx + 3)])

                    extracted = self._parse_analyte_data(search_chunk, meta)
                    if extracted:
                        extracted["source_page"] = page_num
                        extracted["test_date"] = self.extract_test_date(page_text)
                        results.append(extracted)
                        seen_canonical.add(canonical)

        return results

    def _parse_analyte_data(self, chunk: str, meta: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        canonical = meta["canonical_name"]

        # 1. Locate observed numeric value
        # Patterns like: "TSH: 4.8", "TSH 4.8 mIU/L", "TSH - 4.8"
        value_pattern = rf"(?i)(?:{'|'.join(meta['aliases'])})[^\d\n\r]{{0,30}}?(\d+(?:\.\d+)?)"
        match_val = re.search(value_pattern, chunk)

        if not match_val:
            # Try looser number following label
            loose_pattern = r"(\d+(?:\.\d+)?)"
            matches = list(re.finditer(loose_pattern, chunk))
            if not matches:
                return None
            num_str = matches[0].group(1)
        else:
            num_str = match_val.group(1)

        try:
            numeric_value = float(num_str)
        except ValueError:
            return None

        # 2. Extract unit if present
        unit_pattern = r"\b(mIU/L|uIU/mL|mIU/mL|ng/dL|mg/dL|%|pmol/L|pg/mL|nmol/L)\b"
        unit_match = re.search(unit_pattern, chunk, re.IGNORECASE)
        unit = unit_match.group(1) if unit_match else meta["default_unit"]

        # 3. Extract laboratory reference range from text
        # Patterns: "0.4 - 4.5", "0.4 to 4.5", "Ref: 0.40 - 4.20"
        range_pattern = r"(?:ref(?:erence)?|range|normal)?\s*[:=\-]?\s*(\d+(?:\.\d+)?)\s*(?:-|to|–)\s*(\d+(?:\.\d+)?)"
        range_match = re.search(range_pattern, chunk, re.IGNORECASE)

        ref_lower: Optional[float] = None
        ref_upper: Optional[float] = None
        ref_text: Optional[str] = None
        confidence = 0.80

        if range_match:
            try:
                r1 = float(range_match.group(1))
                r2 = float(range_match.group(2))
                if r1 < r2:
                    ref_lower, ref_upper = r1, r2
                    ref_text = f"{ref_lower} - {ref_upper} {unit}"
                    confidence = 0.95
            except ValueError:
                pass

        # 4. Determine status based exclusively on extracted reference range
        status = "normal"
        if ref_lower is not None and ref_upper is not None:
            if numeric_value < ref_lower:
                status = "low"
            elif numeric_value > ref_upper:
                status = "elevated"
            else:
                status = "normal"
        else:
            status = "needs_review"
            confidence = min(confidence, 0.70)

        return {
            "test_name": canonical,
            "observed_value": num_str,
            "numeric_value": numeric_value,
            "unit": unit,
            "reference_range_lower": ref_lower,
            "reference_range_upper": ref_upper,
            "reference_range_text": ref_text,
            "status": status,
            "extraction_confidence": confidence,
            "plain_explanation": meta["explanation"],
            "is_user_corrected": False
        }


extraction_service = ExtractionService()
