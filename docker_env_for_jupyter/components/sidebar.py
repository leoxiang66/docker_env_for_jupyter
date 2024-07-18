import reflex as rx

def sidebar_item(
    text: str, icon: str, on_click: callable = None
) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
                "cursor": "pointer",
            },
        ),
        on_click=lambda : on_click(text),
        width="100%",
    )


def sidebar_items(names:rx.Var,update_target) -> rx.Component:
    return rx.foreach(names, lambda name: sidebar_item(name, "mail",update_target))


def sidebar(names:list[str], update_chateroom:callable, update_target:callable) -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    rx.heading(
                        "网页工具箱", size="7", weight="bold"
                    ),
                    rx.icon_button(
                        "refresh-cw",
                        on_click=lambda: update_chateroom(),
                        variant="ghost",
                        color_scheme="cyan",
             
                    ),
                    align="center",
                    justify="space-between",
                    padding_x="0.5rem",
                    width="100%",
                ),
                sidebar_items(names,update_target),
                spacing="5",
                padding_x="1em",
                padding_y="1.5em",
                bg=rx.color("accent", 3),
                align="start",
                height="100vh",
                width="16em",
            ),
        ),
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(
                    rx.icon("align-justify", size=30)
                ),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(
                                    rx.icon("x", size=30)
                                ),
                                width="100%",
                            ),
                            sidebar_items(names,update_target),
                            spacing="5",
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="1.5em",
                        bg=rx.color("accent", 2),
                    ),
                    width="100%",
                ),
                direction="left",
            ),
            padding="1em",
        ),
    )