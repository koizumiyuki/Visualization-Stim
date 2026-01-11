# from __future__ import annotations

import sys
from pathlib import Path
import stim


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/read_circuit_info.py <circuit.stim>")
        sys.exit(2)

    path = Path(sys.argv[1])
    circuit = stim.Circuit.from_file(str(path))

    dem = circuit.detector_error_model()
    print(f"qubits: {circuit.num_qubits} detectors: {dem.num_detectors} observables: {dem.num_observables}")


if __name__ == "__main__":
    main()
