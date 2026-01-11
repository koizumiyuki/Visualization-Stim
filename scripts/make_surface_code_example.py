from __future__ import annotations

from pathlib import Path
import stim


def generate_surface_code_examples(distance: int = 3, rounds: int = 5, out_dir: str = "examples") -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    names = [
        "surface_code:rotated_memory_z",
        "surface_code:rotated_memory_x",
    ]

    for name in names:
        try:
            c = stim.Circuit.generated(name, distance=distance, rounds=rounds)
        except Exception as e:
            # 名前が違う/Stimのバージョン差がある場合に備えてヒントを出す
            raise RuntimeError(
                f"Failed to generate circuit with name={name}.\n"
                f"Error: {e}\n\n"
                f"Try printing available info:\n"
                f"python -c \"import stim; print(stim.Circuit.generated.__doc__)\""
            )

        fname = f"{name.replace(':','_')}_d{distance}_r{rounds}.stim"
        (out / fname).write_text(str(c), encoding="utf-8")
        print(f"Wrote: {out / fname}")


if __name__ == "__main__":
    generate_surface_code_examples(distance=3, rounds=5)
