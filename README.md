# HEutopia: Heuristic contests optimization tools

短期の AtCoder Heuristic Contest で効率的に実験・パラメータ調整を進めるための Python スクリプト等のテンプレートです。

## 想定ディレクトリ構成

```
./
├── Makefile
├── README.md
├── main.cpp             # AtCoder 提出用 C++ 実装コード、`-DBENCHMARK` つきでコンパイルするとスコアを最初に標準出力する
├── constants.py
├── external_solver.py
├── run.py
├── train.py
├── inputs
│   ├── 0000.txt
│   ├── 0001.txt
│   ├── ...
├── resultHHMMSS_****
│   ├── 0000.txt
│   ├── 0001.txt
│   ├── ...
└── trainHHMMSS_****
    ├── 0000.txt
    ├── 0001.txt
    ├── ...
```

## はじめにやること

### パッケージのインストール

```bash
pyenv install 3.10.2
pyenv local 3.10.2
poetry install
```

### システムパラメータの設定

- `constants.py` を開き、全てのパラメータを適切な値に設定し直す。
- `run.py` を開き、`NUM_CASE_LIMIT` の値を設定し直す。
- （ハイパーパラメータ学習を行う場合）`train.py` を開き、`NUM_CASES_LIMIT` および `NUM_TRIALS` の値を設定し直す。

## ローカルテストケースの全実行

```bash
make run
```

## Optuna によるパラメータチューニングの実行

```bash
make train
```

## オートフォーマッタをかける

```bash
make format
```
