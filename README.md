# HEutopia: Heuristic contests optimization tools

短期の AtCoder Heuristic Contest で効率的に実験・パラメータ調整を進めるための Python スクリプト等のテンプレートです。

## 想定ディレクトリ構成

```
./
├── Makefile
├── README.md
├── common.hpp
├── config.yaml
├── expander.py
├── external_solver.py
├── json_dumper.hpp
├── main.cpp
├── poetry.lock
├── pyproject.toml
├── run.py
├── sample_input
│   └── 0001.in
└── train.py
```

## はじめにやること

### パッケージのインストール

```bash
pyenv install 3.10.9
pyenv local 3.10.9
poetry env use 3.10.9
poetry install
```

### システムパラメータの設定

`config.yaml` に基本的な設定が集約されている。

## ローカルテストケースの全実行

```bash
make run
```

## Optuna によるパラメータチューニングの実行

```bash
make train
```

## C++ コードにオートフォーマッタをかける

```bash
make format
```

## Python スクリプトにオートフォーマッタをかける

```bash
make pyformat
```
