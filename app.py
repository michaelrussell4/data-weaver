"""Data-Weaver: A Dash app offering AI chat ✨ features and document search engine 🔎"""

# pylint: disable=W0212,C0301


import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, html, Input, Output, State, callback, _dash_renderer
from utils.app_helper import chroma_df, COLOR_PALETTE

_dash_renderer._set_react_version("18.2.0")


def create_message(message, icon, icon_right=False):
    icon_comp = DashIconify(
        icon=icon,
        width=30,
        className=f"text-indigo-500 text-3xl z-20 m{"l" if icon_right else "r"}-2 bg-white",
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
        className=f"mt-6 flex justify-{"end" if icon_right else "start"}",
        children=children,
    )


def create_weaver_message(message):
    return create_message(message, "mdi:robot-outline")


def create_user_message(message):
    return create_message(message, "mdi:account", True)


EXT_COLOR_MAP = {}


def make_ext_button(ext):
    """
    Creates a button for a file extension with a unique color.

    Args:
        ext (str): The file extension.

    Returns:
        dmc.Button: A styled button with a unique color for the extension.
    """
    # Assign a color to the extension if not already assigned
    if ext not in EXT_COLOR_MAP:
        EXT_COLOR_MAP[ext] = next(COLOR_PALETTE)

    # Create the button with the assigned color
    return dmc.Button(
        ext,
        id={"type": "ext-button", "index": ext},
        radius="xl",
        className=f"text-center text-white {EXT_COLOR_MAP[ext]}",
    )


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
                                                    html.Div("hi") for _ in range(100)
                                                ],  # Large content
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
