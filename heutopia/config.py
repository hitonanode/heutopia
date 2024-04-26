from pydantic.dataclasses import Field, dataclass


@dataclass(frozen=True)
class GoogleSheetsExporterConfig:
    gcp_sa_path: str
    sheet_key: str


@dataclass(frozen=True)
class RunnerConfig:
    run_comand: str = "cat {INPUT_FILE} | {SOLVER_CMD} 2> {SOLVER_OUTPUT}"


@dataclass(frozen=True)
class OptunaConfig:
    num_trials: int = 20
    sqlite_db_path: str = "train.db"


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

    print_columns: list[str] = Field(default_factory=lambda: ["score"])

    runner: RunnerConfig = RunnerConfig()

    optuna: OptunaConfig = OptunaConfig()

    google_sheets: GoogleSheetsExporterConfig | None = None
