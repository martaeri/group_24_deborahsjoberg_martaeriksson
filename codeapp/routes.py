# pylint: disable=cyclic-import

# File that contains all the routes of the application.
# This is equivalent to the "controller" part in a model-view-controller architecture.
# In the final project, you will need to modify this file to implement your project.

# built-in imports
import io

# external imports
from flask import Blueprint, jsonify, render_template
from flask.wrappers import Response as FlaskResponse
from matplotlib.figure import Figure
from werkzeug.wrappers.response import Response as WerkzeugResponse

# internal imports
from codeapp.models import Movie
from codeapp.utils import calculate_statistics, get_data_list, prepare_figure

# define the response type
Response = str | FlaskResponse | WerkzeugResponse

bp = Blueprint("bp", __name__, url_prefix="/")


################################### web page routes ####################################


@bp.get("/")  # root route
def home() -> Response:
    dataset: list[Movie] = get_data_list()
    counter: dict[int, float] = calculate_statistics(dataset)
    return render_template("home.html", counter=counter)


@bp.get("/image")
def image() -> FlaskResponse:
    # gets dataset
    dataset: list[Movie] = get_data_list()

    # get the statistics that is supposed to be shown
    counter: dict[int, float] = calculate_statistics(dataset)

    # creating the plot
    fig = Figure()
    ax = fig.gca()
    ax.bar(
        list(sorted(counter.keys())),
        [counter[x] for x in sorted(counter.keys())],
        color="gray",
        alpha=0.5,
        zorder=2,
    )
    ax.plot(
        list(sorted(counter.keys())),
        [counter[x] for x in sorted(counter.keys())],
        marker="x",
        color="#25a848",
        zorder=3,
    )
    ax.grid(ls=":", zorder=1)
    ax.set_xlabel("Year")
    ax.set_ylabel("Highest score of the year")

    # Set y-axis limits and ticks
    ax.set_ylim(7, 10.5)  # Set y-axis limits from 7 to 10.5
    ax.set_yticks([i / 10 for i in range(70, 106, 2)])

    # Set x-axis tick labels to display the year for each column
    ax.set_xticks(list(sorted(counter.keys())))  # Set x-axis ticks to years
    ax.set_xticklabels([str(year) for year in sorted(counter.keys())], rotation=45)

    fig.tight_layout()

    ################ START -  THIS PART MUST NOT BE CHANGED BY STUDENTS ################
    # create a string buffer to hold the final code for the plot
    output = io.StringIO()
    fig.savefig(output, format="svg")
    # output.seek(0)
    final_figure = prepare_figure(output.getvalue())
    return FlaskResponse(final_figure, mimetype="image/svg+xml")


@bp.get("/about")
def about() -> Response:
    return render_template("about.html")


################################## web service routes ##################################


@bp.get("/json-dataset")
def get_json_dataset() -> Response:
    # gets dataset
    dataset: list[Movie] = get_data_list()

    # render the page
    return jsonify(dataset)


@bp.get("/json-stats")
def get_json_stats() -> Response:
    # gets dataset
    dataset: list[Movie] = get_data_list()

    # get the statistics that is supposed to be shown
    counter: dict[int, float] = calculate_statistics(dataset)

    # render the page
    return jsonify(counter)
