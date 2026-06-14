import pytest
import pandas as pd

from src.data.data_services import Data_Services
from pandas.testing import assert_frame_equal


def test_data_loading_success():
    data_serv = Data_Services()

    data = data_serv.load_data("data/raw/dataset.csv")

    assert not data.empty


def test_data_loading_failed():
    data_serv = Data_Services()

    with pytest.raises(FileNotFoundError):
        data_serv.load_data("invalid.csv")


def test_merge_target_vals():
    # Setup
    input_df = pd.DataFrame({
        "email_criticality": ["low", "medium", "high"]
    })

    processor = Data_Services()
    processor.data = input_df

    # Expected
    expected_df = pd.DataFrame({
        "email_criticality": [0, 1, 1]
    })

    result_df = processor.merge_target_vals()

    assert_frame_equal(result_df, expected_df)
