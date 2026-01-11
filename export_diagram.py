from __future__ import annotations

import sys
from pathlib import Path
import stim

from read_stim.stim_svg_export import (
    save_circuit_timeslice_svg,
    add_white_bg_rect,
    convert_svg_to_pdf_and_optional_png,
)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/export_diagram.py <circuit.stim> [out_dir]")
        sys.exit(2)

    circuit_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path("out")
    out_dir.mkdir(parents=True, exist_ok=True)

    c = stim.Circuit.from_file(str(circuit_path))

    svg_path = out_dir / (circuit_path.stem + ".svg")
    svg_white_path = out_dir / (circuit_path.stem + "_white.svg")

    save_circuit_timeslice_svg(c, svg_path)
    add_white_bg_rect(svg_path, svg_white_path)

    pdf_path, png_path = convert_svg_to_pdf_and_optional_png(svg_white_path)

    print(f"Wrote: {svg_path}")
    print(f"Wrote: {svg_white_path}")
    print(f"Wrote: {pdf_path}")
    if png_path is None:
        print("PNG: skipped (renderPM unavailable; Cairo may be missing)")
    else:
        print(f"Wrote: {png_path}")


if __name__ == "__main__":
    main()
