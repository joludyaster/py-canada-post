from importlib.metadata import version
from cyclopts import App
from .rating import rating_app

def version_callback() -> str:
    """
    Function to get a version of the wrapper.

    Returns
    -------
    str
        Version of the wrapper.
    """
    return version('py_canada_post')

app = App(
    name="py-canada-post",
    help="Python wrapper to interact with Canada Post API.",
    version_format="rich",
    version_flags=["--version", "-V"],
    version=version_callback,
    help_format="rich",
)
app.command(rating_app)

if __name__ == "__main__":
    app()
