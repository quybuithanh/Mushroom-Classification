import pandas as pd
from sklearn.preprocessing import LabelEncoder

COLUMN_NAMES = [
    "poisonous",
    "cap_shape",
    "cap_surface",
    "cap_color",
    "bruises",
    "odor",
    "gill_attachment",
    "gill_spacing",
    "gill_size",
    "gill_color",
    "stalk_shape",
    "stalk_root",
    "stalk_surface_above_ring",
    "stalk_surface_below_ring",
    "stalk_color_above_ring",
    "stalk_color_below_ring",
    "veil_type",
    "veil_color",
    "ring_number",
    "ring_type",
    "spore_print_color",
    "population",
    "habitat"
]


def load_data(file_path):
    df = pd.read_csv(file_path, header=None)
    df.columns = COLUMN_NAMES
    return df


def clean_data(df):
    mode_value = df["stalk_root"].mode()[0]
    df["stalk_root"] = df["stalk_root"].replace("?", mode_value)
    return df


def encode_data(df):
    encoders = {}
    for column in df.columns:
        encoder = LabelEncoder()
        df[column] = encoder.fit_transform(df[column])
        encoders[column] = encoder

    return df, encoders


def split_features_target(df):
    X = df.drop("poisonous", axis=1)
    y = df["poisonous"]
    return X, y