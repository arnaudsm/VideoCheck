"""Main module."""

from tqdm import tqdm
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
from time import sleep


def videocheck(
        paths=("."),
        output_file="videochecked.csv",
        extensions=["avi", "mkv", "mp4", "wmv", "mpg"],
        delete=False,
        forbidden_hours=None,
        threads=4,
):
    def check_time():
        now = datetime.now()

        if now.hour >= forbidden_hours[0] and now.hour <= forbidden_hours[1]:
            future = datetime(now.year, now.month, now.day,
                              forbidden_hours[1], 0)
            print("⏰ Forbidden hour. Sleeping until",
                  forbidden_hours[1], ":00")
            sleep((future-now).total_seconds())

    def report():
        total = videochecked.shape[0]
        errors = videochecked[videochecked.errors.str.len() > 0].shape[0]

        print("#"*30)
        print("SCAN DONE")
        print("{errors}/{total} faulty videos detected".format(
            errors=errors, total=total,
        ), "✅" if errors == 0 else "🚨", "\n")

        print("Report file available:", output_file)

        if delete:
            delete_files()
        else:
            print("Tip: Use --delete to delete them")

        print("OVER ✅")

    def delete_files():
        print("#"*30)
        print("DELETING")
        files = list(videochecked[videochecked.errors.str.len() > 0].file)

        for file in tqdm(files):
            Path(file).unlink(missing_ok=False)

    files = []
    for path in paths:
        for extension in extensions:
            files += Path(path).rglob("*."+extension)

    if len(files) == 0:
        print("🚨 No file detected. Provide a path with video files, or add new extensions using --extensions")
        return

    if Path(output_file).is_file():
        videochecked = pd.read_csv(output_file, index_col=0, dtype={'corrupted': "bool"})
    else:
        videochecked = pd.DataFrame(columns=["errors", "corrupted"], index=["file"]).dropna()

    files = [str(file.absolute()) for file in files if str(file.absolute()) not in videochecked.index]
    videochecked = videochecked.append(pd.DataFrame(index=files))
    files = videochecked[videochecked.corrupted.isnull()].index

    if len(files) == 0:
        report()
        return

    print("🏁", len(files), "files to check")
    pbar = tqdm(
        files,
        total=videochecked.shape[0],
        initial=videochecked.shape[0]-len(files)
    )
    for file in pbar:
        if forbidden_hours:
            check_time()
        pbar.set_description(file)
        errors = os.popen(
            'ffmpeg -loglevel error -threads {threads} -i "{file}" -f null - 2>&1'.format(
                file=file,
                threads=threads,
            )
        ).read().strip()
        corrupted = len(errors) > 0
        videochecked.loc[file] = pd.Series({
            "errors": errors,
            "corrupted": corrupted,
        })
        pbar.set_postfix(errors=videochecked[videochecked.errors.str.len() > 0].shape[0])
        videochecked.to_csv(output_file, index="file")
    report()
