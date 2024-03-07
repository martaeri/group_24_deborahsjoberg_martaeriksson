# pylint: disable=cyclic-import

#File that contains all the routes of the application.
#This is equivalent to the "controller" part in a model-view-controller architecture.
#In the final project, you will need to modify this file to implement your project.

# built-in imports
import io

# external imports
from flask import Blueprint, jsonify, render_template
from flask.wrappers import Response as FlaskResponse
from matplotlib.figure import Figure
from werkzeug.wrappers.response import Response as WerkzeugResponse

# internal imports
import codeapp.models as models
from codeapp.utils import calculate_statistics, get_data_list, prepare_figure

# define the response type
Response = str | FlaskResponse | WerkzeugResponse

bp = Blueprint("bp", __name__, url_prefix="/")


################################### web page routes ####################################


@bp.get("/")  # root route
def home() -> Response:
    dataset: list[Movie] = get_data_list()
    counter: dict[int, int] = calculate_statistics(dataset)
    return render_template("home.html", counter=counter)


@bp.get("/image")
def image() -> Response:
    # gets dataset
    dataset: list[Movie] = get_data_list()

    # get the statistics that is supposed to be shown
    counter: dict[int, int] = calculate_statistics(dataset)

    # creating the plot

    fig = Figure()
    fig.gca().bar(
        list(sorted(counter.keys())),
        [counter[x] for x in sorted(counter.keys())],
        color="gray",
        alpha=0.5,
        zorder=2,
    )
    fig.gca().plot(
        list(sorted(counter.keys())),
        [counter[x] for x in sorted(counter.keys())],
        marker="x",
        color="#25a848",
        zorder=3,
    )
    fig.gca().grid(ls=":", zorder=1)
    fig.gca().set_xlabel("Year")
    fig.gca().set_ylabel("Highest score of the year")
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
    # TODO
    pass


@bp.get("/json-stats")
def get_json_stats() -> Response:
    # TODO
    pass
