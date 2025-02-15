#!/usr/bin/env python
import argparse
import logging
import pandas as pd
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="exercise_5", job_type="process_data")
    artifact = run.use_artifact(args.input_artifact)
    df_parquet = pd.read_parquet(artifact.file())
    df_parquet = df_parquet.drop_duplicates().reset_index(drop=True)

    df_parquet['title'].fillna(value='', inplace=True)
    df_parquet['song_name'].fillna(value='', inplace=True)
    df_parquet['text_feature'] = df_parquet['title'] + ' ' + \
        df_parquet['song_name']

    out_path = args.artifact_name
    df_parquet.to_csv(out_path)
    artifact = wandb.Artifact(
        name=args.artifact_name,
        type=args.artifact_type,
        description=args.artifact_description
    )
    artifact.add_file(out_path)
    run.log_artifact(artifact)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess a dataset",
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True,
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        required=True,
    )

    args = parser.parse_args()

    go(args)
