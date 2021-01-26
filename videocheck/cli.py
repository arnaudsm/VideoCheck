"""Console script for videocheck."""
import sys
import click
from videocheck.main import videocheck


@click.command()
@click.argument('paths', type=click.Path(exists=True), nargs=-1)
@click.option('--output', '-o', type=click.Path(dir_okay=False), default='./videochecked.csv', help='help')
@click.option('--extensions', '-e', default="avi,mkv,mp4,wmv,mpg", help='help')
@click.option('--forbidden-hours', '-f', help='help')
@click.option('--threads', '-t', default=4, help='help')
@click.option('--delete', '-d', is_flag=True, default=False, help='help')
def main(paths, output, extensions, delete, forbidden_hours, threads):
    """Console script for videocheck."""
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
