# Visualization-Stim

Stim 回路の情報表示（qubits / detectors / observables）と、Stim の回路図を SVG として出力し、SVG→PDFに変換するための最小ユーティリティです。

## 要件

- Python **3.11 以上**（推奨：3.11）
- macOS / Linux（PNG出力は環境により追加依存あり）

## インストール
このレポジトリを git clone したのち，リポジトリ直下で以下を実行する

```bash
python3.11 -m venv .venv
source .venv/bin/activate

python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
```


## Dependencies

| Package   | Tested version |
| --------- | -------------- |
| Python    | 3.11.7         |
| stim      | 1.15.0         |
| svglib    | 1.6.0          |
| reportlab | 4.4.7          |

Exact pins are in *requirements.txt*.

## 使用例
参照したい.stimを可視化スクリプトに渡す．具体的には，以下をターミナル等で実行する．

### 回路情報生成
```bash
PYTHONPATH=./src python scripts/read_circuit_info.py examples/surface_code_rotated_memory_z_d3_r5.stim
```

### 図の出力（SVG→白背景→PDF）
```bash
PYTHONPATH=./src python scripts/export_diagram.py examples/surface_code_rotated_m
```

### 出力結果
export_diagram.py writes the following files under the output directory (e.g., out/):
- <stem>.svg
- <stem>_white.svg
- <stem>_white.pdf
