# Visualization-Stim

Stim 回路の情報表示（qubits / detectors / observables）と、Stim の回路図を SVG として出力し、SVG→PDF（＋任意でPNG）に変換するための最小ユーティリティです。

## 要件

- Python **3.11 以上**（推奨：3.11）
- macOS / Linux（PNG出力は環境により追加依存あり）

## インストール

```bash
python3.11 -m venv .venv
source .venv/bin/activate

python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
