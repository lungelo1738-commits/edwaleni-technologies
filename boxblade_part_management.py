# ============================================================
# BOXBLADE PART MANAGEMENT SYSTEM V2
# DATABASE + SERIALS + QR + BRAND MARK + LOGGING
# PRODUCTION-READY | GITHUB READY
# ============================================================

import os
import sys
import uuid
import json
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import qrcode
from PIL import Image, ImageDraw

try:
    import cairosvg
    CAIRO_AVAILABLE = True
except (ImportError, OSError):
    CAIRO_AVAILABLE = False

# ============================================================
# LOGGING SETUP
# ============================================================
log_level = logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler("boxblade_management.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# CONFIGURATION
# ============================================================
class Config:
    """Configuration management for the part system."""
    
    BASE_DIR = Path(__file__).resolve().parent
    OUTPUT_DIR = BASE_DIR / "OUTPUT"
    QR_DIR = OUTPUT_DIR / "QRCODES"
    BRAND_DIR = OUTPUT_DIR / "BRAND"
    REPORTS_DIR = OUTPUT_DIR / "REPORTS"
    
    DATABASE_FILE = "boxblade_parts_database.csv"
    DATABASE_XLSX = "boxblade_parts_database.xlsx"
    REPORT_JSON = "parts_manifest.json"
    
    BRAND = "EDW"
    LOGO_SVG = BASE_DIR / "wider_logo.svg"
    LOGO_PNG = BRAND_DIR / "brand_logo.png"
    
    MODELS = ["BB1200", "BB1500", "BB1800", "BB2100", "BB2400"]
    
    PARTS = {
        "Scarifier Teeth": "EDW013-1.1",
        "Scarifier Pin":   "EDW013-1.2",
        "Scarifier Leg":   "EDW013-1.3",
        "Blade":           "EDW013-1.4"
    }
    
    QR_CONFIG = {
        "version": 2,
        "error_correction": qrcode.constants.ERROR_CORRECT_H,
        "box_size": 10,
        "border": 4
    }
    
    LOGO_SIZE = (300, 300)

# ============================================================
# DIRECTORY & LOGO INITIALIZATION
# ============================================================
def setup_directories() -> None:
    """Create all required directories."""
    for directory in [Config.QR_DIR, Config.BRAND_DIR, Config.REPORTS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"[OK] Directory ready: {directory.name}/")

def setup_logo() -> tuple[Image.Image, bool]:
    """Load or generate logo (gracefully handle missing Cairo). Returns (image, is_original_svg)."""
    is_original_svg = False
    
    if not Config.LOGO_PNG.exists():
        if Config.LOGO_SVG.exists() and CAIRO_AVAILABLE:
            logger.info(f"Converting SVG to PNG: {Config.LOGO_SVG.name}")
            cairosvg.svg2png(
                url=str(Config.LOGO_SVG),
                write_to=str(Config.LOGO_PNG),
                output_width=Config.LOGO_SIZE[0],
                output_height=Config.LOGO_SIZE[1]
            )
            logger.info(f"[OK] Logo created: {Config.LOGO_PNG.name}")
            is_original_svg = True
        elif Config.LOGO_SVG.exists():
            logger.warning(f"[WARN] Cairo not available, using placeholder")
            _create_placeholder_logo()
        else:
            logger.warning(f"[WARN] Logo file not found, creating placeholder...")
            _create_placeholder_logo()
    else:
        # Check if SVG source exists for metadata
        is_original_svg = Config.LOGO_SVG.exists()
    
    logo = Image.open(Config.LOGO_PNG).convert("RGBA")
    logger.info(f"[OK] Logo loaded: {Config.LOGO_PNG.name}")
    return logo, is_original_svg

def _create_placeholder_logo() -> None:
    """Create a simple placeholder logo if SVG is unavailable."""
    logo = Image.new("RGBA", Config.LOGO_SIZE, (240, 240, 240, 255))
    draw = ImageDraw.Draw(logo)
    
    # Draw a simple circle with "EDW" text
    margin = 30
    draw.ellipse(
        [margin, margin, Config.LOGO_SIZE[0]-margin, Config.LOGO_SIZE[1]-margin],
        outline=(0, 102, 204),
        width=3
    )
    
    # Add text (approximate centering)
    text = "EDW"
    draw.text((100, 115), text, fill=(0, 102, 204))
    
    logo.save(Config.LOGO_PNG)
    logger.info(f"[OK] Placeholder logo created: {Config.LOGO_PNG.name}")

# ============================================================
# SERIAL NUMBER GENERATOR
# ============================================================
class SerialGenerator:
    """Custom serial number generator with persistence."""
    
    def __init__(self, prefix: str, width: int, persistent: bool = True, file_path: str = None):
        self.prefix = prefix
        self.width = width
        self.persistent = persistent
        self.file_path = file_path
        self.counter = self._load_counter() if persistent else 0
    
    def _load_counter(self) -> int:
        """Load counter from file if persistent."""
        if self.file_path and os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    return int(f.read().strip())
            except Exception:
                return 0
        return 0
    
    def _save_counter(self) -> None:
        """Save counter to file if persistent."""
        if self.persistent and self.file_path:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w") as f:
                f.write(str(self.counter))
    
    def __call__(self) -> str:
        """Generate next serial number."""
        self.counter += 1
        self._save_counter()
        return f"{self.prefix}{str(self.counter).zfill(self.width)}"

def setup_serial_generator() -> SerialGenerator:
    """Initialize the serial number generator."""
    registry_file = Config.OUTPUT_DIR / "serial_registry.txt"
    generator = SerialGenerator(
        prefix=Config.BRAND,
        width=6,
        persistent=True,
        file_path=str(registry_file)
    )
    logger.info(f"[OK] Serial generator ready (prefix: {Config.BRAND})")
    return generator

# ============================================================
# QR CODE GENERATION
# ============================================================
def generate_qr_code(
    payload: str,
    serial: str,
    logo: Image.Image
) -> Image.Image:
    """Generate branded QR code with embedded logo."""
    qr = qrcode.QRCode(**Config.QR_CONFIG)
    qr.add_data(payload)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    
    # Embed logo in center
    qr_w, qr_h = qr_img.size
    logo_size = qr_w // 4
    logo_resized = logo.resize((logo_size, logo_size))
    pos = ((qr_w - logo_size) // 2, (qr_h - logo_size) // 2)
    qr_img.paste(logo_resized, pos, mask=logo_resized)
    
    return qr_img

# ============================================================
# PART GENERATION ENGINE
# ============================================================
def generate_parts(
    serial_gen: SerialGenerator,
    logo: Image.Image,
    logo_svg_available: bool
) -> tuple[List[Dict], int]:
    """Generate all parts with QR codes."""
    records = []
    count = 0
    
    total_parts = len(Config.MODELS) * len(Config.PARTS)
    logger.info(f"Generating {total_parts} parts...")
    
    for model in Config.MODELS:
        for part_name, part_number in Config.PARTS.items():
            count += 1
            
            serial_number = serial_gen()
            part_id = str(uuid.uuid4())
            created_at = datetime.now().isoformat()
            
            # QR payload
            qr_payload = (
                f"BRAND: {Config.BRAND}\n"
                f"MODEL: {model}\n"
                f"PART NAME: {part_name}\n"
                f"PART NUMBER: {part_number}\n"
                f"SERIAL NUMBER: {serial_number}\n"
                f"PART ID: {part_id}\n"
                f"CREATED AT: {created_at}"
            )
            
            # Generate QR code
            qr_img = generate_qr_code(qr_payload, serial_number, logo)
            qr_path = Config.QR_DIR / f"{serial_number}.png"
            qr_img.save(qr_path)
            
            # Database record with logo details
            record = {
                "part_id": part_id,
                "brand": Config.BRAND,
                "model": model,
                "part_name": part_name,
                "part_number": part_number,
                "serial_number": serial_number,
                "qr_code_file": qr_path.name,
                "qr_code_path": str(qr_path),
                "logo_svg_file": str(Config.LOGO_SVG.name) if logo_svg_available else "placeholder",
                "logo_svg_path": str(Config.LOGO_SVG) if logo_svg_available else "N/A",
                "logo_png_path": str(Config.LOGO_PNG),
                "created_at": created_at
            }
            records.append(record)
            
            logger.debug(f"  [{count:2d}/{total_parts}] {model} | {part_name} | {serial_number}")
    
    return records, count

# ============================================================
# DATABASE & REPORTING
# ============================================================
def save_database(records: List[Dict]) -> Path:
    """Save parts to CSV and Excel database."""
    df = pd.DataFrame(records)
    db_path = Config.OUTPUT_DIR / Config.DATABASE_FILE
    df.to_csv(db_path, index=False)

    xlsx_path = Config.OUTPUT_DIR / Config.DATABASE_XLSX
    try:
        df.to_excel(xlsx_path, index=False)
        logger.info(f"[OK] Database saved: {db_path.name} ({len(records)} records) and {xlsx_path.name}")
    except Exception as e:
        logger.warning(f"[WARN] Failed to save Excel database: {e}")
        logger.info(f"[OK] CSV Database saved: {db_path.name} ({len(records)} records)")

    return db_path


from typing import Optional, Tuple

def save_serial_registry(records: Optional[List[Dict]] = None) -> Tuple[Path, int]:
    """Save a serial registry mapping serial_number to part_id, part_number, model, and description as CSV and Excel.

    If `records` is None, try to read the persistent database (CSV or Excel) and build the registry from it so
    the registry contains data for all parts in the database, not only the current run.
    Returns (csv_path, number_of_records)
    """
    # If no records provided, attempt to read from the persistent database
    if records is None:
        db_csv = Config.OUTPUT_DIR / Config.DATABASE_FILE
        db_xlsx = Config.OUTPUT_DIR / Config.DATABASE_XLSX
        if db_csv.exists():
            try:
                df_db = pd.read_csv(db_csv)
            except Exception as e:
                logger.error(f"[ERROR] Failed to read database CSV: {e}")
                df_db = pd.DataFrame()
        elif db_xlsx.exists():
            try:
                df_db = pd.read_excel(db_xlsx)
            except Exception as e:
                logger.error(f"[ERROR] Failed to read database Excel: {e}")
                df_db = pd.DataFrame()
        else:
            logger.warning("[WARN] No existing database found to build serial registry from.")
            df_db = pd.DataFrame()

        # Convert dataframe rows to list of dicts for uniform processing
        records = df_db.to_dict(orient="records")

    rows = []
    for r in records:
        rows.append({
            "serial_number": r.get("serial_number"),
            "part_id": r.get("part_id"),
            "part_number": r.get("part_number"),
            "model": r.get("model"),
            "description": (r.get("part_name") or r.get("description") or "").strip(),
            "qr_code_path": r.get("qr_code_path"),
            "created_at": r.get("created_at")
        })

    df = pd.DataFrame(rows)

    # Deduplicate by serial_number if present
    if "serial_number" in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=["serial_number"]).reset_index(drop=True)
        after = len(df)
        if after != before:
            logger.info(f"[OK] Removed {before-after} duplicate serial entries when building registry.")

    csv_path = Config.OUTPUT_DIR / "serial_registry.csv"
    df.to_csv(csv_path, index=False)

    xlsx_path = Config.OUTPUT_DIR / "serial_registry.xlsx"
    try:
        df.to_excel(xlsx_path, index=False)
        logger.info(f"[OK] Serial registry saved: {csv_path.name} and {xlsx_path.name} ({len(df)} records)")
    except Exception as e:
        logger.warning(f"[WARN] Failed to save serial registry Excel: {e}")
        logger.info(f"[OK] Serial registry saved: {csv_path.name} ({len(df)} records)")

    return csv_path, len(df)

def save_manifest(records: List[Dict]) -> Path:
    """Save parts manifest as JSON for easy reference."""
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "total_parts": len(records),
        "brand": Config.BRAND,
        "logo_svg": str(Config.LOGO_SVG),
        "logo_png": str(Config.LOGO_PNG),
        "models": Config.MODELS,
        "parts": Config.PARTS,
        "records": records
    }
    
    manifest_path = Config.REPORTS_DIR / Config.REPORT_JSON
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    logger.info(f"[OK] Manifest saved: {manifest_path.name}")
    return manifest_path

def print_summary(record_count: int, part_count: int) -> None:
    """Print completion summary."""
    print("\n" + "="*60)
    print("[SUCCESS] PART MANAGEMENT SYSTEM COMPLETE")
    print("="*60)
    print(f"  Parts Generated:     {record_count}")
    print(f"  Iterations:          {part_count}")
    print(f"  Models:              {len(Config.MODELS)}")
    print(f"  Part Types:          {len(Config.PARTS)}")
    print(f"  Brand:               {Config.BRAND}")
    print("-"*60)
    print(f"  Database (CSV):      OUTPUT/{Config.DATABASE_FILE}")
    print(f"  Database (Excel):    OUTPUT/{Config.DATABASE_XLSX}")
    print(f"  Serial Registry:     OUTPUT/serial_registry.csv")
    print(f"  Serial Registry (Excel): OUTPUT/serial_registry.xlsx")
    print(f"  QR Codes:            OUTPUT/QRCODES/")
    print(f"  Manifest:            OUTPUT/REPORTS/{Config.REPORT_JSON}")
    print(f"  Brand Assets:        OUTPUT/BRAND/")
    print(f"  Activity Log:        boxblade_management.log")
    print("="*60 + "\n")

# ============================================================
# MAIN EXECUTION
# ============================================================
def main() -> None:
    """Main execution flow."""
    try:
        logger.info("="*60)
        logger.info("BOXBLADE PART MANAGEMENT SYSTEM v2.0")
        logger.info("="*60)
        
        # Setup
        setup_directories()
        logo, logo_svg_available = setup_logo()
        serial_gen = setup_serial_generator()
        
        # Generate
        records, part_count = generate_parts(serial_gen, logo, logo_svg_available)
        
        # Save
        save_database(records)
        save_manifest(records)
        # Build serial registry from the full persistent database so it includes all parts
        save_serial_registry()

        # Summary
        print_summary(len(records), part_count)
        logger.info("[SUCCESS] System completed successfully")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"[ERROR] System error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
