import solara
from solara.website.utils import apidoc

# Simulated data for visualization
years = [f"Year {i+1}" for i in range(10)]  # 10 years
users = [50, 60, 70, 80, 85, 90, 92, 94, 96, 98]  # Users in each year
non_users = [50, 40, 30, 20, 15, 10, 8, 6, 4, 2]  # Non-users in each year

# ECharts configuration
options = {
    "title": {"text": "Users vs Non-Users of Digital Services"},
    "tooltip": {},
    "legend": {"data": ["Users", "Non-Users"]},
    "xAxis": {"type": "category", "data": years},
    "yAxis": {"type": "value"},
    "series": [
        {
            "name": "Users",
            "type": "bar",
            "data": users,
        },
        {
            "name": "Non-Users",
            "type": "bar",
            "data": non_users,
        },
    ],
}

@solara.component
def Page():
    with solara.VBox() as main:
        with solara.Card(" "):
            solara.FigureEcharts(option=options, responsive=True)
    return main

if __doc__ is None:
    __doc__ = ""
__doc__ += apidoc(solara.FigureEcharts.f)  # type: ignore
