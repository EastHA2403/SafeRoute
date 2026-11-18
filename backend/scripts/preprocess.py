"""공공데이터(data/raw) -> data/processed/{nodes,edges,accidents}.csv 전처리.

서버와 분리된 오프라인 스크립트. 실행: python -m scripts.preprocess
TODO: 실제 공공데이터(도로망/표고/사고다발구역) 확보 후 구현.
"""


def main() -> None:
    raise NotImplementedError("실데이터 확보 후 Pandas 전처리 로직을 구현하세요.")


if __name__ == "__main__":
    main()

