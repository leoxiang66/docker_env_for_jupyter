import reflex as rx
from .components.sidebar import sidebar
from rxconfig import config
import time
from itchat_helper import ICHelper

ith = ICHelper()


class State(rx.State):
    """The app state."""

    qrcode_generated: bool = False
    chatrooms: list[str] = []
    target_nickname: str = "Undefined Target"
    textinput: str = ""

    def update_textinput(self,string:str):
        self.textinput = string

    def login(self):
        ith.login(
            new_thread=True,
            picDir="assets/qrcode.png",
            # login_callback=self.loginComplete,
        )
        time.sleep(2)
        self.qrcode_generated = True

    def loginComplete(self):
        print("登录成功")

    def update_chatrooms(self):
        chatrooms= [x.get_nickname() for x in ith.get_chatrooms()]
        self.chatrooms = chatrooms
        self.update_target(chatrooms[0])

    def update_nickname(self, name: str):
        self.target_nickname = name



    def update_target(self, name: str):
        self.update_nickname(name=name)

        
    def handle_submit(self):
        # 在这里处理提交的文本
        ith.send_chatroom_msg(self.textinput,self.target_nickname)
        print(f"Submitted: {self.textinput}")
        



def index() -> rx.Component:
    return rx.hstack(
        rx.container(
            rx.color_mode.button(position="top-right"),
            rx.vstack(
                rx.vstack(
                    rx.button(
                        "扫码登录",
                        on_click=State.login,
                        color_scheme="grass",
                    ),
                    rx.button(
                        "跳转到app",
                        on_click=rx.redirect("/app"),
                        color_scheme="grass",
                    ),
                    rx.cond(
                        State.qrcode_generated,
                        rx.image(src="qrcode.png", width="200px", height="200px"),
                        rx.box(),
                    ),
                ),
                spacing="5",
                justify="center",
                min_height="85vh",
            ),
            rx.logo(),
        ),
    )


def app_page() -> rx.Component:
    return rx.hstack(
        sidebar(State.chatrooms, State.update_chatrooms, State.update_target),
        rx.container(
            rx.vstack(
                rx.text(f'Target: {State.target_nickname}'),
                rx.spacer(),
                rx.hstack(
                    rx.text_area(
                        on_change= State.set_textinput
                        ),
                    rx.button("submit", on_click=State.handle_submit),
                ),
                rx.spacer(),
                align="center",
            ),
            padding="2rem",
            width="100%",
            height="100vh",
        ),
    )





app = rx.App()
app.add_page(index)
app.add_page(app_page, route="/app")
