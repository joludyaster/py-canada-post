from cyclopts import App
from .commands.get_rates import get_rates
from .commands.discover_services import discover_services

rating_app = App(
    name="rating",
    help="Command to contain all rating-related commands (e.g. get_rates, discover_services etc.)."
)

rating_app.command(get_rates)
rating_app.command(discover_services)
