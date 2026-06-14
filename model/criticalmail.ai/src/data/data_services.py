import pandas as pd
import spacy

nlp = spacy.load('en_core_web_sm')


class Data_Services:
    def __init__(self, data: pd.DataFrame = []):
        self.data = data

    def load_data(self, data_path: str) -> pd.DataFrame:
        df = pd.read_csv(data_path)
        self.data = df
        return df

    def get_shape(self):
        return self.data.shape()

    def merge_target_vals(self) -> pd.DataFrame:
        # Merging target classes High and Medium as High itself,
        # to reduce complexity
        self.data["email_criticality"] = self.data["email_criticality"].map(
            {"low": 0, "medium": 1, "high": 1}
        )

        return self.data

    def tokenize_text(self, text: str = '') -> list[str]:
        if text != '':
            doc = nlp(text)

            token = [
                token.lemma_.lower()
                for token in doc
                if not token.is_stop
                and not token.is_punct
                and not token.is_space
            ]

            return token
