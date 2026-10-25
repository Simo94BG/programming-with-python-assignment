"""
Module containing all visualisation functions.
Uses bokeh to create interactive visualisations.
Plots both line charts and scatter plots to visualise the results.
The plots are interactive, zoomable, and provide hover tooltips for easier analysis.
"""

from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, Span

def plot_train_vs_chosen_ideal(df_train, df_ideal, df_mapping, visualisation_path):
    """
    Plots the training datasets against their chosen ideal function.
    Plots both:
    - A line chart of the training dataset vs its ideal function.
    - A scatter plot of the deviations, for further deviation analysis, if required.
    :param df_train: DataFrame of the train dataset.
    :param df_ideal: DataFrame of the ideal functions dataset.
    :param df_mapping: DataFrame containing the mapping of the training datasets and their chosen ideal functions.
    :param visualisation_path: The folder path where the visualisations should be stored.
    :return: None
    """

    x_col = df_train["x"]
    mapping = dict(zip(df_mapping["train_function"], df_mapping["ideal_function"]))

    # For each training dataset from the mapping DataFrame provided...
    for train_col, ideal_col, in mapping.items():
        output_file(f"{visualisation_path}{train_col}_vs_{ideal_col}.html")
        y_train = df_train[train_col]
        y_ideal = df_ideal[ideal_col]
        deviation = y_train - y_ideal

        source = ColumnDataSource({
            "x_col": x_col,
            "y_train": y_train,
            "y_ideal": y_ideal,
            "deviation": deviation
        })

        p = figure(
            title=f"{train_col} vs {ideal_col}"
            ,x_axis_label="X Values"
            ,y_axis_label="Y Values"
            ,tools="pan, wheel_zoom, box_zoom, reset, save"
            ,sizing_mode="stretch_both"
        )

        # Large, centered, bold title
        p.title.text_font_size = "20pt"
        p.title.align = "center"
        p.title.text_font_style = "bold"

        # Add the train dataset as a scatter plot
        p.scatter(
            x="x_col"
            ,y="y_train"
            ,source=source
            ,line_width=2
            ,color="black"
            ,legend_label="Train"
        )

        # Add the ideal function as a line chart
        p.line(
            x="x_col"
            ,y="y_ideal"
            ,source=source
            ,line_width=2
            ,color="blue"
            ,legend_label="Ideal"
        )

        # Add the hover tooltips
        hover = HoverTool(
            tooltips=[
                ("x", "@x_col"),
                ("Train", "@y_train{0.000}"),
                ("Ideal", "@y_ideal{0.000}"),
                ("Deviation", "@deviation{0.000}")
            ],
            mode="vline" # Hover follows vertical line at x
        )

        p.add_tools(hover)
        p.legend.click_policy = "hide"

        save(p)

def plot_train_vs_chosen_ideal_deviation(df_train, df_ideal, df_mapping, visualisation_path):
    """
    Plots a scatter plot of the deviation between each training dataset and its chosen ideal function.

    :param df_train: DataFrame of the train dataset.
    :param df_ideal: DataFrame of the ideal functions dataset.
    :param df_mapping: DataFrame containing the mapping of the training datasets and their chosen ideal functions.
    :param visualisation_path: The folder path where the visualisations should be stored.
    :return: None
    """

    x_col = df_train["x"]
    mapping = dict(zip(df_mapping["train_function"], df_mapping["ideal_function"]))

    for train_col, ideal_col, in mapping.items():
        output_file(f"{visualisation_path}{train_col}_vs_{ideal_col}_deviation.html")
        y_train = df_train[train_col]
        y_ideal = df_ideal[ideal_col]
        deviation = y_train - y_ideal

        source = ColumnDataSource({
            "x_col": x_col,
            "deviation": deviation
        })

        p = figure(
            title=f"{train_col} vs {ideal_col} - Deviation"
            ,x_axis_label="X Values"
            ,y_axis_label="Deviation"
            ,tools="pan, wheel_zoom, box_zoom, reset, save"
            ,sizing_mode="stretch_both"
        )

        p.title.text_font_size = "20pt"
        p.title.align = "center"
        p.title.text_font_style = "bold"

        # Add black axis lines
        x_zero = Span(location=0, dimension='height', line_color='black', line_width=2)
        y_zero = Span(location=0, dimension='width', line_color='black', line_width=2)
        p.add_layout(x_zero)
        p.add_layout(y_zero)

        # Plot the deviations as a scatter plot.
        p.scatter(
            x="x_col"
            ,y="deviation"
            ,source=source
            ,size=8
            ,color="black"
            ,alpha=0.6
            ,legend_label="Deviation"
        )

        # Add the hover tooltips.
        hover = HoverTool(tooltips=[
            ("x", "@x_col{0.0}")
            , ("Deviation", "@deviation{0.000}")
        ])
        p.add_tools(hover)

        p.legend.click_policy = "hide"

        save(p)

def plot_test_vs_chosen_ideal(df_test_mapped, visualisation_path, mapped_only = False):
    """
    Plot a scatter plot of the test data and the mapped ideal function for each test record.
    Store the chart HTML file under a different name depending on whether the mapped only test data is plotted, or not.

    :param df_test_mapped: DataFrame of the mapped test dataset.
    :param visualisation_path: The folder path where the visualisations should be stored.
    :param mapped_only: Boolean stating whether it's plotting the full dataset or the mapped only dataset.
    :return: None
    """

    output_file(f"{visualisation_path}test_vs_chosen_ideal.html")

    # If mapped only, store under a separate name.
    if mapped_only:
        output_file(f"{visualisation_path}test_vs_chosen_ideal_mapped_only.html")

    source = ColumnDataSource(df_test_mapped)

    p = figure(
        title="Test vs Chosen Ideal"
        ,x_axis_label="x"
        ,y_axis_label="y"
        ,tools="pan, wheel_zoom, box_zoom, reset, save"
        ,sizing_mode="stretch_both"
    )

    # Plot the test dataset as a scatter plot.
    p.scatter(
        x="x_test"
        ,y="y_test"
        ,source=source
        ,size=8
        ,color="black"
        ,alpha=0.6
        ,legend_label="Test"
    )

    # Plot the mapped ideal functions as a scatter plot.
    p.scatter(
        x="x_test"
        ,y="y_ideal"
        ,source=source
        ,size=8
        ,color="blue"
        ,alpha=0.6
        ,legend_label="Ideal"
    )

    # Add the hover tooltips.
    hover = HoverTool(tooltips=[
        ("x", "@x_test{0.0}")
        ,("Test", "@y_test{0.000}")
        ,("Ideal", "@y_ideal{0.000}")
        ,("Deviation", "@deviation{0.000}")
        ,("Ideal Function", "@ideal_function")
    ])
    p.add_tools(hover)

    p.legend.click_policy = "hide"

    save(p)