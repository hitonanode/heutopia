from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class GoogleSheetsExporterConfig:
    gcp_sa_path: str
    sheet_key: str


@dataclass(frozen=True)
class OptunaConfig:
    num_trials: int = 0


@dataclass(frozen=True)
class HeutopiaConfig:
    # 並列実行数
    num_process: int

    # 最大実行ケース数
    num_case_limit: int

    # 順位表テストケース数
    scoreboard_testcases: int

    # 入力データディレクトリ
    dataset_dir: str

    print_columns: list[str]

    optuna: OptunaConfig | None = None

    google_sheets: GoogleSheetsExporterConfig | None = None
