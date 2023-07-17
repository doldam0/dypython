from dataclasses import dataclass
from typing import Callable


@dataclass
class MainArguments:
    result_filename: str


def parse_args():
    import argparse
    from typing import cast

    parser = argparse.ArgumentParser()
    parser.add_argument("--result-filename", "-f", type=str)
    return cast(MainArguments, parser.parse_args())


def main(args: MainArguments):
    import pandas as pd

    def get_group_name(group: int) -> str:
        if group == 1:
            return ""
        else:
            return f".{group - 1}"
        
    def get_std_score_func(mean: float, std: float) -> Callable[[float], float]:
        def std_score(x: float) -> float:
            return (x - mean) / (std + 1) * 20 + 100
        return std_score

    df = pd.read_csv(args.result_filename)
    df = df.drop("타임스탬프", axis=1)

    # 행 별 표준점수 계산
    for i in range(len(df)):
        row = df.iloc[i]
        df.iloc[i] = row.apply(get_std_score_func(row.mean(), row.std()))

    scores = {
        group: {
            "logical": df[f"논리 전개{get_group_name(group)}"].mean(),
            "presentation": df[f"발표{get_group_name(group)}"].mean(),
        }
        for group in range(1, 8)
    }

    print(scores)

if __name__ == "__main__":
    main(parse_args())
