import pandas as pd
from os.path import dirname, abspath

src_dir = f"{abspath(dirname(__file__))}"
jargon_df = pd.read_csv(f"{src_dir}/jargon_list.csv")
