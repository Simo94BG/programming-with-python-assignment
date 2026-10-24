import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool

def plot_train_vs_chosen_ideal(df_train, df_ideal, df_mapping, visualisation_path):

    x = df_train["x"]

    mapping = dict(zip(df_mapping["train_function"], df_mapping["ideal_function"]))

    for train_col, ideal_col, in mapping.items():
        plt.figure(figsize=(10, 5))

        # Plot training function
        plt.plot(x, df_train[train_col], label=f"Training: {train_col}", linewidth=2)

        # Plot ideal function
        plt.plot(x, df_ideal[ideal_col], label=f"Ideal: {ideal_col}", linestyle="--")

        plt.title(f"{train_col} vs {ideal_col}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(f"{visualisation_path}{train_col}_vs_{ideal_col}.png", dpi=300)
        #plt.show()
        plt.close()

def plot_test_vs_chosen_ideal(df_test_mapped, visualisation_path, mapped_only = False):

    file_name = "test_vs_chosen_ideal"

    if mapped_only:
        df_test_mapped = df_test_mapped[df_test_mapped["ideal_function"].notna()]
        file_name = "test_vs_chosen_ideal_mapped_only"

    ideal_functions = sorted(df_test_mapped["ideal_function"].dropna().unique().tolist())
    ideal_function_colours = ["Red", "Blue", "Green", "Yellow"]
    ideal_functions_dict = dict(zip(ideal_functions, ideal_function_colours))

    x = df_test_mapped["x_test"]
    plt.figure(figsize=(12, 8))
    plt.scatter(x, df_test_mapped["y_test"], label="Test", color="Black")

    #plt.scatter(x, df_test_mapped["y_ideal"], label="Mapped Ideal")

    for ideal_function, ideal_colour in ideal_functions_dict.items():
        df_selected_values = df_test_mapped[df_test_mapped["ideal_function"] == ideal_function]
        plt.scatter(df_selected_values["x_test"], df_selected_values["y_ideal"], label=ideal_function, color=ideal_colour)

    plt.title("Test vs Chosen Ideal")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"{visualisation_path}{file_name}.png", dpi=300)
    plt.close()

def plot_test_vs_chosen_ideal_interactive(df_test_mapped, visualisation_path, mapped_only = False):

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
        ("x", "@x_test")
        ,("Test", "@y_test")
        ,("Ideal", "@y_ideal")
        ,("Deviation", "@deviation")
        ,("Ideal Function", "@ideal_function")
    ])
    p.add_tools(hover)

    p.legend.click_policy = "hide"

    save(p)