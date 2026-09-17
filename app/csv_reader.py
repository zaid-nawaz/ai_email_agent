import pandas as pd


REQUIRED_COLUMNS = [
    "name",
    "email",
    "company",
    "role",
    "company_description"
]


def read_leads(file_path: str) -> list[dict]:
    df = pd.read_csv(file_path)

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    df = df.fillna("")

    return df.to_dict(orient="records")