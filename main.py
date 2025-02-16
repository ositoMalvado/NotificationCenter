import flet as ft
from NotificationCenter import (
    NotificationCenter,
    NotificationStyle,
    NotificationTypes,
)
import random


def main(page: ft.Page):
    noti_style_1 = NotificationStyle(
        in_duration=500,
        out_duration=1000,
        in_scale=0.3,
        in_opacity=0.5,
        in_offset=ft.Offset(-2, 0),
        in_offset_curve=ft.AnimationCurve.BOUNCE_OUT,
        out_scale=0.3,
        out_offset=ft.Offset(0, -4),
    )

    noti_style_2 = NotificationStyle(
        in_duration=100,
        out_duration=500,
        in_scale=2,
        in_opacity=0.5,
        width=250,
        height=120,
        in_offset=ft.Offset(0, -2),
        in_offset_curve=ft.AnimationCurve.FAST_OUT_SLOWIN,
        out_scale=1.5,
        out_offset=ft.Offset(0, -4),
    )

    notification_center_1 = NotificationCenter(notification_style=noti_style_1)
    notification_center_2 = NotificationCenter(
        notification_style=noti_style_2, alignment=ft.alignment.top_right
    )
    ran_words = ["Hello World", "Bye Hell", "Superman < Goku!", "👽 i'm anal ien"]
    noti_types = [
        NotificationTypes.INFO,
        NotificationTypes.SUCCESS,
        NotificationTypes.WARNING,
        NotificationTypes.ERROR,
    ]

    def add_notification(e):
        if e.control.data == "left":
            notification_center_1.add_notification(
                ft.Text(random.choice(ran_words), color=ft.Colors.BLACK),
                random.choice(noti_types).value,
            )
        elif e.control.data == "right":
            notification_center_2.add_notification(
                ft.Text(random.choice(ran_words), color=ft.Colors.BLACK),
                random.choice(noti_types).value,
            )
        else:
            notification_center_1.add_notification(
                ft.Text(random.choice(ran_words), color=ft.Colors.BLACK),
                random.choice(noti_types).value,
            )
            notification_center_2.add_notification(
                ft.Text(random.choice(ran_words), color=ft.Colors.BLACK),
                random.choice(noti_types).value,
            )

    page.floating_action_button = ft.FloatingActionButton(
        content=ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Button("Left", data="left", on_click=add_notification),
                ft.Button("Right", data="right", on_click=add_notification),
            ],
        ),
        width=200,
        on_click=add_notification,
        data="both",
    )

    page.add(
        ft.SafeArea(
            ft.Stack(
                [notification_center_1, notification_center_2],
                expand=True,
            ),
            expand=True,
        )
    )


ft.app(main, view=ft.AppView.WEB_BROWSER)
