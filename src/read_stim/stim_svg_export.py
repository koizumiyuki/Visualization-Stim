# from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import stim
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

# renderPM は PNG 変換に必要だが、環境によって Cairo が無いと import 時点で落ちる。
try:
    from reportlab.graphics import renderPM  # type: ignore
except Exception:
    renderPM = None


def save_circuit_svg(circuit: stim.Circuit, path: str | Path = "circuit.svg", diagram_type: str = "timeline-svg") -> Path:
    """
    Export a Stim circuit diagram as SVG.

    diagram_type examples:
      - "timeline-svg"
      - "timeslice-svg"
      - "detslice-svg"
      - "detslice-with-ops-svg"
    """
    path = Path(path)
    svg = circuit.diagram(diagram_type)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(str(svg), encoding="utf-8")
    return path


def save_circuit_timeline_svg(circuit: stim.Circuit, path: str | Path = "circuit.svg") -> Path:
    return save_circuit_svg(circuit, path, "timeline-svg")


def save_circuit_timeslice_svg(circuit: stim.Circuit, path: str | Path = "circuit.svg") -> Path:
    return save_circuit_svg(circuit, path, "timeslice-svg")


def save_circuit_detslice_svg(circuit: stim.Circuit, path: str | Path = "circuit.svg") -> Path:
    return save_circuit_svg(circuit, path, "detslice-svg")


def save_circuit_detslice_with_ops_svg(circuit: stim.Circuit, path: str | Path = "circuit.svg") -> Path:
    return save_circuit_svg(circuit, path, "detslice-with-ops-svg")


def add_white_bg_rect(in_path: str | Path, out_path: str | Path) -> Path:
    """
    Insert a white background rectangle right after the <svg ...> tag.
    Useful because some viewers render SVG with transparent background.
    """
    in_path = Path(in_path)
    out_path = Path(out_path)

    svg = in_path.read_text(encoding="utf-8")
    insert_str = '<rect width="100%" height="100%" fill="white"/>\n'

    svg_pos = svg.find("<svg")
    if svg_pos == -1:
        raise ValueError("No <svg> tag found in file")

    gt_pos = svg.find(">", svg_pos)
    if gt_pos == -1:
        raise ValueError("Malformed <svg> tag")

    new_svg = svg[: gt_pos + 1] + "\n  " + insert_str + svg[gt_pos + 1 :]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(new_svg, encoding="utf-8")
    return out_path


def convert_svg_to_pdf(svg_path: str | Path, pdf_path: Optional[str | Path] = None) -> Path:
    """
    Convert SVG -> PDF using svglib + reportlab (renderPDF).
    This does NOT require Cairo.
    """
    svg_path = Path(svg_path)
    if pdf_path is None:
        pdf_path = svg_path.with_suffix(".pdf")
    pdf_path = Path(pdf_path)

    drawing = svg2rlg(str(svg_path))
    if drawing is None:
        raise ValueError(f"svg2rlg failed to load: {svg_path}")

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    renderPDF.drawToFile(drawing, str(pdf_path))
    return pdf_path


def convert_svg_to_pdf_and_optional_png(
    svg_path: str | Path,
    pdf_path: Optional[str | Path] = None,
    png_path: Optional[str | Path] = None,
    *,
    png_dpi: int = 300,
) -> Tuple[Path, Optional[Path]]:
    """
    Convert SVG -> PDF always, and -> PNG only if renderPM is available.
    If Cairo is missing, PNG is skipped (returns None for png_path).
    """
    svg_path = Path(svg_path)
    if pdf_path is None:
        pdf_path = svg_path.with_suffix(".pdf")
    if png_path is None:
        png_path = svg_path.with_suffix(".png")

    pdf_path = Path(pdf_path)
    png_path = Path(png_path)

    pdf = convert_svg_to_pdf(svg_path, pdf_path)

    if renderPM is None:
        return pdf, None

    drawing2 = svg2rlg(str(svg_path))
    if drawing2 is None:
        raise ValueError(f"svg2rlg failed to load (2nd pass): {svg_path}")

    png_path.parent.mkdir(parents=True, exist_ok=True)
    renderPM.drawToFile(drawing2, str(png_path), fmt="PNG", dpi=png_dpi)  # type: ignore
    return pdf, png_path
