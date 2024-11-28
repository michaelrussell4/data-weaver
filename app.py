"""Data-Weaver: A Dash app offering AI chat ✨ features and document search engine 🔎"""

# pylint: disable=W0212,C0301


import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, html, Input, Output, State, callback, _dash_renderer
from utils.app_helper import (
    chroma_df,
    make_ext_button,
    make_file_display,
    create_weaver_message,
    create_user_message,
)


_dash_renderer._set_react_version("18.2.0")

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=dmc.styles.ALL + ["assets/tailwind.min.css"])

app.layout = dmc.MantineProvider(
    children=[
        # Main
        html.Div(
            className="flex flex-col h-screen w-screen divide-y divide-indigo-200 overflow-hidden absolute",
            children=[
                # Header
                html.Div(
                    className="header flex space-x-2 items-center justify-end pr-8 m-0 w-full",
                    style={"minHeight": "4rem"},
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
                    className="flex-grow flex flex-col overflow-hidden",
                    children=[
                        # Search and Chat Headers
                        html.Div(
                            className="hidden md:flex md:flex-col md:grid md:grid-cols-2 gap-4 p-4 text-xl",
                            children=[
                                html.Div(
                                    className="flex justify-center items-center gap-2",
                                    children=[
                                        html.Div(
                                            className="flex items-center gap-1",
                                            children=[
                                                html.Span("Search"),
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
                                html.Div(
                                    className="flex justify-center items-center gap-2",
                                    children=[
                                        html.Div(
                                            className="flex items-center gap-1",
                                            children=[
                                                html.Span("Chat with"),
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
                        # Main Content
                        html.Div(
                            className="flex-grow flex flex-col grid grid-cols-1 md:grid-cols-2 gap-4 p-4 h-full overflow-hidden",
                            children=[
                                # Left Column
                                html.Div(
                                    className="flex flex-col gap-4 max-h-full overflow-y-auto",
                                    children=[
                                        html.Div(
                                            className="w-full flex flex-col gap-4",
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
                                                html.Div(
                                                    className="grid grid-flow-row grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 2xl:grid-cols-10 gap-2",
                                                    children=[
                                                        make_ext_button(ext)
                                                        for ext in chroma_df.ext.unique()
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="flex-grow overflow-y-auto",  # Scrolling for content
                                            children=[
                                                *[
                                                    html.Div(
                                                        className="grid grid-flow-row grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 2xl:grid-cols-10 gap-4",
                                                        children=[
                                                            make_file_display(file)
                                                            for file in chroma_df.source.unique()
                                                        ],
                                                    )
                                                ],
                                            ],
                                        ),
                                    ],
                                ),
                                # Right Column
                                html.Div(
                                    className="flex flex-col gap-4 max-h-full overflow-y-auto",
                                    children=[
                                        # Chat Card
                                        html.Div(
                                            className="flex-grow border border-gray-200 shadow-sm rounded-lg p-4 h-full max-h-full overflow-y-auto",
                                            children=[
                                                create_weaver_message(
                                                    "Hi, I'm Weaver. Ask me anything! anything! anything! anything! anything!anything!anything! anything! anything! anything!"
                                                ),
                                                create_user_message(
                                                    "hey do you know anything? anything? anything? anything? anything?anything?anything? anything? anything? anything?"
                                                ),
                                                create_user_message(
                                                    "hey do you know anything? anything? anything? anything? anything?anything?anything? anything? anything? anything?"
                                                ),
                                                create_user_message(
                                                    "hey do you know anything? anything? anything? anything? anything?anything?anything? anything? anything? anything?"
                                                ),
                                                create_weaver_message(
                                                    "Hi, I'm Weaver. Ask me anything! anything! anything! anything! anything!anything!anything! anything! anything! anything!"
                                                ),
                                                create_user_message(
                                                    "hey do you know anything? anything? anything? anything? anything?anything?anything? anything? anything? anything?"
                                                ),
                                                create_weaver_message(
                                                    "Hi, I'm Weaver. Ask me anything! anything! anything! anything! anything!anything!anything! anything! anything! anything!"
                                                ),
                                                create_user_message(
                                                    "hey do you know anything? anything? anything? anything? anything?anything?anything? anything? anything? anything?"
                                                ),
                                                create_weaver_message(
                                                    "Hi, I'm Weaver. Ask me anything! anything! anything! anything! anything!anything!anything! anything! anything! anything!"
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
