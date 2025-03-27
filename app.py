from shiny import App, render, ui, reactive
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shiny
import pkg_resources

# Display package versions to show which versions are being used
pd_version = pd.__version__
np_version = np.__version__
mpl_version = plt.matplotlib.__version__
shiny_version = shiny.__version__
pulumi_version = pkg_resources.get_distribution("pulumi").version

# Use layout_sidebar with sidebar instead of panel_sidebar
app_ui = ui.page_fluid(
    ui.tags.h1("Package Version Demo"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.h3("Controls"),
            ui.input_slider("rows", "Number of rows", min=5, max=20, value=10),
            ui.input_slider("cols", "Number of columns", min=2, max=10, value=5),
            ui.input_select(
                "operation",
                "DataFrame operation",
                choices=["Mean", "Sum", "Min", "Max", "Std"],
                selected="Mean"
            ),
            ui.h4("Package Versions:"),
            ui.tags.ul(
                ui.tags.li(f"Shiny: {shiny_version}"),
                ui.tags.li(f"Pandas: {pd_version}"),
                ui.tags.li(f"NumPy: {np_version}"),
                ui.tags.li(f"Matplotlib: {mpl_version}"),
                ui.tags.li(f"Pulumi: {pulumi_version}")
            ),
            # Set open="open" to force the sidebar to always be expanded
            open="open"
        ),
        # Content after the sidebar is the main content (no need for panel_main)
        ui.card(
            ui.card_header("Random DataFrame"),
            ui.output_data_frame("df")
        ),
        ui.card(
            ui.card_header("Summary"),
            ui.output_text("summary"),
            ui.output_plot("plot")
        )
    )
)

def server(input, output, session):
    
    # Create a reactive calculation for the dataframe that can be reused
    @reactive.calc
    def generate_df():
        data = np.random.randn(input.rows(), input.cols())
        return pd.DataFrame(
            data, 
            columns=[f"Column {i+1}" for i in range(input.cols())],
            index=[f"Row {i+1}" for i in range(input.rows())]
        )
    
    @output
    @render.data_frame
    def df():
        return generate_df()
    
    @output
    @render.text
    def summary():
        dataframe = generate_df()
        operation = input.operation()
        
        if operation == "Mean":
            result = dataframe.mean()
        elif operation == "Sum":
            result = dataframe.sum()
        elif operation == "Min":
            result = dataframe.min()
        elif operation == "Max":
            result = dataframe.max()
        elif operation == "Std":
            result = dataframe.std()
            
        return f"Applied operation: {operation}\n{result}"
    
    @output
    @render.plot
    def plot():
        dataframe = generate_df()
        operation = input.operation().lower()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if operation == "mean":
            dataframe.mean().plot(kind='bar', ax=ax)
        elif operation == "sum":
            dataframe.sum().plot(kind='bar', ax=ax)
        elif operation == "min":
            dataframe.min().plot(kind='bar', ax=ax)
        elif operation == "max":
            dataframe.max().plot(kind='bar', ax=ax)
        elif operation == "std":
            dataframe.std().plot(kind='bar', ax=ax)
            
        ax.set_title(f"{operation.capitalize()} by Column")
        ax.set_ylabel(operation.capitalize())
        ax.set_xlabel("Columns")
        
        return fig

app = App(app_ui, server)
