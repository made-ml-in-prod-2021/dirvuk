from dataclasses import dataclass, field


@dataclass()
class ModelParams:
    model_type: str = field(default='RandomForestClassifier')
    criterion: str = field(default='entropy')
    max_depth: int = field(default=2)
    min_samples_leaf: int = field(default=5)
    min_samples_split: int = field(default=17)
    n_estimators: int = field(default=19)
    n_jobs: int = field(default=-1)
