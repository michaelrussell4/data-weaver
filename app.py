"""Data-Weaver: A Dash app offering AI chat ✨ features and document search engine 🔎"""

# pylint: disable=W0212,C0301


import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, html, Input, Output, State, callback, _dash_renderer

_dash_renderer._set_react_version("18.2.0")


def create_message(message, icon, icon_right=False):
    icon_comp = DashIconify(
        icon=icon,
        width=30,
        className="text-indigo-500 text-3xl z-20 mr-2 bg-white",
    )
    msg_comp = html.Div(
        message,
        className=f"bg-{"blue" if icon_right else "gray"}-100 shadow-sm rounded-xl p-4 text-gray-500 z-10",
        style={
            "white-space": "pre-wrap",  # Only break on newlines unless forced
            "word-wrap": "break-word",  # Break words if constrained
            "width": "fit-content",  # Adjust width to fit content
            "max-width": "66.6666%",  # Max width is 2/3 of the parent
        },
    )
    children = [icon_comp, msg_comp]
    if icon_right:
        children = children[::-1]
    return html.Div(
        className=f"flex justify-{"end" if icon_right else "start"}",
        children=children,
    )


def create_weaver_message(message):
    return create_message(message, "mdi:robot-outline")


def create_user_message(message):
    return create_message(message, "mdi:account", True)


# Initialize the Dash app
app = Dash(__name__, external_stylesheets=dmc.styles.ALL + ["assets/tailwind.min.css"])

# Set Mantine Provider for overall theming
app.layout = dmc.MantineProvider(
    children=[
        # Main
        html.Div(
            className="divide-y divide-indigo-200 h-screen",
            children=[
                # Header
                html.Div(
                    className="flex space-x-2 items-center justify-end pr-8 m-0 h-16 w-full",
                    children=[
                        html.Div(
                            className="flex m-0",
                            children=[
                                html.Span(
                                    "Data",
                                    className="text-indigo-800 text-3xl font-black",
                                ),
                                html.Span(
                                    "Weaver",
                                    className="text-indigo-500 text-3xl",
                                ),
                            ],
                        ),
                        DashIconify(
                            icon="mdi:robot-outline",
                            width=30,
                            className="text-indigo-500 text-3xl",
                        ),
                    ],
                ),
                # Body
                html.Div(
                    style={"height": "calc(100vh - 4rem)"},
                    className="flex flex-col",
                    children=[
                        html.Div(
                            className="grid grid-cols-2 gap-4 p-4 text-xl",
                            children=[
                                # Data search header
                                html.Div(
                                    className="flex justify-center items-center gap-2",
                                    children=[
                                        html.Div(
                                            className="flex items-center gap-1",
                                            children=[
                                                html.Span(
                                                    "Search",
                                                ),
                                                html.Span(
                                                    "Data",
                                                    className="text-indigo-500",
                                                ),
                                            ],
                                        ),
                                        DashIconify(
                                            icon="mdi:database-search",
                                            width=30,
                                            className="text-indigo-800",
                                        ),
                                    ],
                                ),
                                # Chat Header
                                html.Div(
                                    className="flex justify-center items-center gap-2",
                                    children=[
                                        html.Div(
                                            className="flex items-center gap-1",
                                            children=[
                                                html.Span(
                                                    "Chat with",
                                                ),
                                                html.Span(
                                                    "Weaver",
                                                    className="text-indigo-500",
                                                ),
                                            ],
                                        ),
                                        DashIconify(
                                            icon="mdi:robot-outline",
                                            width=30,
                                            className="text-indigo-800",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="flex-grow grid grid-cols-2 gap-4",
                            children=[
                                # Left Column
                                html.Div(
                                    className="flex flex-col gap-4 p-4 h-full",
                                    children=[
                                        # Search Input
                                        html.Div(
                                            className="w-full",
                                            children=[
                                                dmc.TextInput(
                                                    size="lg",
                                                    placeholder="Search documents",
                                                    id="doc-search-input",
                                                    rightSection=DashIconify(
                                                        icon="mdi:magnify",
                                                        width=20,
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                # Right Column
                                html.Div(
                                    className="flex flex-col gap-4 p-4 h-full",
                                    children=[
                                        # Chat Card
                                        html.Div(
                                            className="flex-grow flex flex-col justify-end border border-gray-200 shadow-sm rounded-lg p-4",
                                            children=[
                                                create_weaver_message(
                                                    "Hi, I'm Weaver. Ask me anything!"
                                                ),
                                                create_user_message(
                                                    "hey do you know anything?"
                                                ),
                                            ],
                                        ),
                                        # Chat Input
                                        html.Div(
                                            className="w-full",
                                            children=[
                                                dmc.TextInput(
                                                    id="chat-input",
                                                    size="lg",
                                                    placeholder="Chat with Weaver",
                                                ),
                                            ],
                                        ),
                                        # Send Button
                                        dmc.Button(
                                            className="bg-indigo-500 hover:bg-indigo-400 text-white font-bold py-2 px-4 rounded flex items-center justify-center",
                                            id="send-chat-btn",
                                            disabled=True,
                                            children=[
                                                DashIconify(
                                                    icon="mdi:right", className="mr-2"
                                                ),
                                                html.Span("Send"),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    ],
)


@callback(
    Output("send-chat-btn", "disabled"),
    Input("chat-input", "value"),
    prevent_initial_call=True,
)
def update_disabled_for_chat_btn(chat_input):
    return not chat_input


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
