"""Main module."""

from tqdm import tqdm
import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
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
        errors = videochecked.errors.dropna().shape[0]
        correct = total - errors

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
        files = list(videochecked[~videochecked.errors.isnull()].file)

        for file in tqdm(files):
            Path(file).unlink(missing_ok=False)

    files = []
    for path in paths:
        for extension in extensions:
            files += Path(path).rglob("*."+extension)

    if len(files) == 0:
        print("🚨 No file detected. Provide a path with video files, or add new extensions using --extensions")

    if Path(output_file).is_file():
        videochecked = pd.read_csv(output_file, index_col=None)
        files = [file for file in files if str(
            file.absolute()) in videochecked.file]
    else:
        videochecked = pd.DataFrame(columns=["file", "errors"])

    if len(files) == 0:
        report()
        return

    print("🏁", len(files), "files to check")

    for file in tqdm(files):
        if forbidden_hours:
            check_time()
        print(file.absolute(), end="")

        errors = os.popen(
            'ffmpeg -loglevel error -threads {threads} -i "{file}" -f null - 2>&1'.format(
                file=file,
                threads=threads,
            )
        ).read().strip()

        print(
            "\r",
            "✅" if len(errors) == 0 else "❌",
            " ",
            file.absolute(),
            sep=""
        )

        videochecked = videochecked.append({
            "file": str(file.absolute()),
            "errors": errors
        }, ignore_index=True)
        videochecked.to_csv(output_file, index=None)

    report()
