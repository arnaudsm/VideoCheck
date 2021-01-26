"""Console script for videocheck."""
import sys
import click
from videocheck.main import videocheck


@click.command()
@click.argument('paths', type=click.Path(exists=True), nargs=-1)
@click.option('--output', '-o', type=click.Path(dir_okay=False), default='./videochecked.csv', help='Output file path (csv file)')
@click.option('--extensions', '-e', default="avi,mkv,mp4,wmv,mpg", help='Video extensions to scan')
@click.option('--forbidden-hours', '-f', help='Forbidden hours (useful for multi-day scans), example: 18-23 to forbid scanning between 18h and 23h')
@click.option('--threads', '-t', default=4, help='CPU threads for FFmpeg')
@click.option('--delete', '-d', is_flag=True, default=False, help='Delete corrupt files after scanning')
def main(paths, output, extensions, delete, forbidden_hours, threads):
    """Automated tool to check consistency of your video library."""
    extensions = extensions.split(",")

    if forbidden_hours:
        try:
            forbidden_hours = list(map(int, forbidden_hours.split("-")))
            assert len(forbidden_hours) == 2
            assert forbidden_hours[0] in range(0, 24)
            assert forbidden_hours[1] in range(0, 24)
            assert forbidden_hours[1] >= forbidden_hours[0]
        except Exception:
            click.echo(
                "Forbidden hours are badly formatted. Please provide a 0-24 format.")

    if len(paths) == 0:
        paths = (".")

    videocheck(paths, output, extensions, delete, forbidden_hours, threads)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
