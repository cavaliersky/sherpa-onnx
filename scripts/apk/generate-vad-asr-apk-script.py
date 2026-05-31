#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
from pathlib import Path

import jinja2


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--total",
        type=int,
        default=1,
        help="Number of runners",
    )
    parser.add_argument(
        "--index",
        type=int,
        default=0,
        help="Index of the current runner",
    )
    return parser.parse_args()


@dataclass
class Model:
    model_name: str
    idx: int
    lang: str
    lang2: str
    short_name: str = ""
    cmd: str = ""
    rule_fsts: str = ""
    use_hr: bool = False


def get_models():
    models = [
        Model(
            model_name="sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17",
            idx=15,
            lang="zh_en_ko_ja_yue",
            lang2="中英粤日韩",
            short_name="sense_voice",
            use_hr=True,
            cmd="""
            pushd $model_name
            rm -rfv test_wavs
            rm -fv *.py
            ls -lh
            popd
            """,
        ),
    ]
    return models


def main():
    args = get_args()
    
    all_model_list = get_models()

    d = dict()
    d["model_list"] = all_model_list

    filename_list = [
        "./build-apk-vad-asr.sh",
    ]
    for filename in filename_list:
        environment = jinja2.Environment()
        if not Path(f"{filename}.in").is_file():
            print(f"skip {filename}")
            continue

        with open(f"{filename}.in") as f:
            s = f.read()
        template = environment.from_string(s)

        s = template.render(**d)
        
        with open(filename, "w") as f:
            print(s, file=f)


if __name__ == "__main__":
    main()
