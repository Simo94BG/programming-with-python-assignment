from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, Span

def plot_train_vs_chosen_ideal(df_train, df_ideal, df_mapping, visualisation_path):

    x_col = df_train["x"]
    mapping = dict(zip(df_mapping["train_function"], df_mapping["ideal_function"]))

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

        p.title.text_font_size = "20pt"
        p.title.align = "center"
        p.title.text_font_style = "bold"

        p.line(
            x="x_col"
            ,y="y_train"
            ,source=source
            ,line_width=2
            ,color="black"
            ,legend_label="Train"
        )

        p.line(
            x="x_col"
            ,y="y_ideal"
            ,source=source
            ,line_width=2
            ,color="blue"
            ,legend_label="Ideal"
        )

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

        p.scatter(
            x="x_col"
            ,y="deviation"
            ,source=source
            ,size=8
            ,color="black"
            ,alpha=0.6
            ,legend_label="Deviation"
        )

        hover = HoverTool(tooltips=[
            ("x", "@x_col{0.0}")
            , ("Deviation", "@deviation{0.000}")
        ])
        p.add_tools(hover)

        p.legend.click_policy = "hide"

        save(p)

def plot_test_vs_chosen_ideal(df_test_mapped, visualisation_path, mapped_only = False):

    output_file(f"{visualisation_path}test_vs_chosen_ideal.html")

    if mapped_only:
        df_test_mapped = df_test_mapped[df_test_mapped["ideal_function"].notna()]
        output_file(f"{visualisation_path}test_vs_chosen_ideal_mapped_only.html")

    source = ColumnDataSource(df_test_mapped)

    p = figure(
        title="Test vs Chosen Ideal"
        ,x_axis_label="x"
        ,y_axis_label="y"
        ,tools="pan, wheel_zoom, box_zoom, reset, save"
        ,sizing_mode="stretch_both"
    )

    p.scatter(
        x="x_test"
        ,y="y_test"
        ,source=source
        ,size=8
        ,color="black"
        ,alpha=0.6
        ,legend_label="Test"
    )

    p.scatter(
        x="x_test"
        ,y="y_ideal"
        ,source=source
        ,size=8
        ,color="blue"
        ,alpha=0.6
        ,legend_label="Ideal"
    )

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