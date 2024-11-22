"""Data-Weaver: A Dash app offering AI chat ✨ features and document search engine 🔎"""

import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, html, Input, Output, State, callback, _dash_renderer

_dash_renderer._set_react_version("18.2.0")  # pylint: disable=W0212

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=dmc.styles.ALL)

# Set Mantine Provider for overall theming
app.layout = dmc.MantineProvider(
    children=dmc.Container(
        [
            # Header Section with Title and Icon
            dmc.Container(
                h=70,
                children=dmc.Group(
                    [
                        DashIconify(
                            icon="mdi:robot-outline",
                            width=30,
                            color="violet",
                        ),
                        dmc.Title("Data-Weaver", order=2, style={"color": "violet"}),
                    ],
                    m="xs",
                ),
                style={"padding": "10px 20px", "borderBottom": "1px solid #eaeaea"},
            ),
            # Main Content with Two Panes
            dmc.Grid(
                [
                    # Left Pane for AI Chat
                    dmc.GridCol(
                        dmc.Paper(
                            [
                                dmc.Title("AI Chat", order=4),
                                dmc.Textarea(
                                    id="chat-input",
                                    placeholder="Type your message here...",
                                    style={"width": "100%"},
                                ),
                                dmc.Button(
                                    "Send",
                                    id="send-chat-btn",
                                    color="violet",
                                    style={"marginTop": "10px"},
                                ),
                                dmc.Divider(m="20px 0"),
                                dmc.ScrollArea(
                                    id="chat-output",
                                    style={"height": "400px", "padding": "10px"},
                                ),
                            ],
                            p="md",
                            shadow="sm",
                        ),
                        span=6,
                    ),
                    # Right Pane for Document Search
                    dmc.GridCol(
                        dmc.Paper(
                            [
                                dmc.Title("Document Search", order=4),
                                dmc.TextInput(
                                    id="doc-search-input",
                                    placeholder="Search for documents...",
                                    style={"width": "100%"},
                                ),
                                dmc.Button(
                                    "Search",
                                    id="search-doc-btn",
                                    color="blue",
                                    style={"marginTop": "10px"},
                                ),
                                dmc.Divider(m="20px 0"),
                                dmc.ScrollArea(
                                    id="doc-results",
                                    style={"height": "400px", "padding": "10px"},
                                    children=dmc.Text(
                                        "Results will appear here.",
                                        style={"color": "#888"},
                                    ),
                                ),
                            ],
                            p="md",
                            shadow="sm",
                        ),
                        span=6,
                    ),
                ],
                gutter="lg",
                style={"marginTop": "20px"},
            ),
        ],
        fluid=True,
    )
)


# Example Callbacks
@callback(
    Output("chat-output", "children"),
    Input("send-chat-btn", "n_clicks"),
    State("chat-input", "value"),
    prevent_initial_call=True,
)
def update_chat(n_clicks, message):
    if message:
        return [
            dmc.Text(f"You: {message}", color="blue"),
            dmc.Text(f"AI: This is a response to '{message}'", color="green"),
        ]
    return None


@callback(
    Output("doc-results", "children"),
    Input("search-doc-btn", "n_clicks"),
    State("doc-search-input", "value"),
    prevent_initial_call=True,
)
def update_document_results(n_clicks, query):
    if query:
        return [
            dmc.Text(f"Searching for: {query}"),
            dmc.Text("Result 1: Example document result."),
            dmc.Text("Result 2: Another document match."),
        ]
    return dmc.Text("No query provided.")


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
