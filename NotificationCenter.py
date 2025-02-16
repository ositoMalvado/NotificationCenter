import flet as ft
import asyncio
from dataclasses import dataclass, field
from enum import Enum


class NotificationTypes(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

    def __str__(self):
        return self.value


@dataclass
class NotificationStyle:
    height: int = 70
    width: int = 200
    spacing: int = 10
    border_radius: int = 5
    padding: int = 10
    in_duration: int = 666
    position_animation: ft.AnimationCurve = field(
        default_factory=lambda: ft.AnimationCurve.FAST_OUT_SLOWIN
    )
    in_offset: ft.Offset = field(default_factory=lambda: ft.Offset(0, 0))  # Corregido
    in_offset_curve: ft.AnimationCurve = field(
        default_factory=lambda: ft.AnimationCurve.FAST_OUT_SLOWIN
    )
    out_offset_curve: ft.AnimationCurve = field(
        default_factory=lambda: ft.AnimationCurve.FAST_OUT_SLOWIN
    )
    in_opacity: float = 0.0
    in_opacity_curve: ft.AnimationCurve = field(
        default_factory=lambda: ft.AnimationCurve.FAST_OUT_SLOWIN
    )
    out_opacity_curve: ft.AnimationCurve = field(
        default_factory=lambda: ft.AnimationCurve.FAST_OUT_SLOWIN
    )
    in_scale: float = 0.2
    in_scale_curve: ft.AnimationCurve = field(
        default_factory=lambda: ft.AnimationCurve.FAST_OUT_SLOWIN
    )
    out_scale_curve: ft.AnimationCurve = field(
        default_factory=lambda: ft.AnimationCurve.FAST_OUT_SLOWIN
    )
    out_duration: int = 500
    out_offset: ft.Offset = field(default_factory=lambda: ft.Offset(0, 0))
    out_opacity: float = 0.0
    out_scale: float = 1.2
    bgcolors: dict = field(
        default_factory=lambda: {
            "info": ft.Colors.BLUE_100,
            "success": ft.Colors.GREEN_ACCENT_100,
            "warning": ft.Colors.AMBER_100,
            "error": ft.Colors.RED_ACCENT_100,
        }
    )

    icons: dict = field(
        default_factory=lambda: {
            "info": ft.Icons.INFO_OUTLINE,
            "success": ft.Icons.CHECK_CIRCLE_OUTLINE,
            "warning": ft.Icons.WARNING_AMBER_ROUNDED,
            "error": ft.Icons.ERROR_OUTLINE,
        }
    )

    icon_colors: dict = field(
        default_factory=lambda: {
            "info": ft.Colors.BLUE_900,
            "success": ft.Colors.GREEN_900,
            "warning": ft.Colors.AMBER_900,
            "error": ft.Colors.RED_900,
        }
    )

    text_colors: dict = field(
        default_factory=lambda: {
            "info": ft.Colors.BLUE_900,
            "success": ft.Colors.GREEN_900,
            "warning": ft.Colors.AMBER_900,
            "error": ft.Colors.RED_900,
        }
    )

    def get_bgcolor(self, notification_type: str) -> str:
        return self.bgcolors.get(notification_type, ft.Colors.PRIMARY_CONTAINER)

    def get_icon(self, notification_type: str) -> str:
        return self.icons.get(notification_type, ft.Icons.NOTIFICATIONS_NONE)

    def get_icon_color(self, notification_type: str) -> str:
        return self.icon_colors.get(notification_type, ft.Colors.PRIMARY)

    def get_text_color(self, notification_type: str) -> str:
        return self.text_colors.get(notification_type, ft.Colors.PRIMARY)


class NotificationBanner(ft.Container):
    def __init__(
        self,
        index: int,
        remove_cb,
        content: ft.Control,
        notification_type: str,
        duration: int = 0,
        notification_style: NotificationStyle = NotificationStyle(),
    ):
        super().__init__()
        self.index = index
        self.notification_style = notification_style
        self.width = self.notification_style.width
        self.height = self.notification_style.height
        self.spacing = self.notification_style.spacing
        self.remove_cb = remove_cb
        self.notification_type = notification_type
        self.duration = duration
        self.bgcolor = self.notification_style.get_bgcolor(notification_type)
        self.border_radius = self.notification_style.border_radius
        self.opacity = self.notification_style.in_opacity
        self.scale = self.notification_style.in_scale
        self.padding = self.notification_style.padding
        self.content = ft.Column(
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    expand=True,
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                self.notification_style.get_icon(
                                    self.notification_type
                                ),
                                color=self.notification_style.get_icon_color(
                                    self.notification_type
                                ),
                            ),
                            ft.Container(expand=True, content=content),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color=self.notification_style.get_icon_color(
                                    self.notification_type
                                ),
                                on_click=self.destroy,
                            ),
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ),
            ],
            spacing=0,
        )
        self.top = self._calculate_position()
        self.offset = self.notification_style.in_offset
        self.animate_offset = ft.Animation(
            self.notification_style.in_duration,
            self.notification_style.in_offset_curve,
        )
        self.animate_opacity = ft.Animation(
            self.notification_style.in_duration,
            self.notification_style.in_opacity_curve,
        )
        self.animate_scale = ft.Animation(
            self.notification_style.in_duration,
            self.notification_style.in_scale_curve,
        )

        self.animate_position = ft.Animation(
            self.notification_style.in_duration,
            self.notification_style.position_animation,
        )

    def did_mount(self):
        self._is_mounted = True
        self.update()
        self.page.run_task(self._animate_enter)
        if self.duration > 0:
            self.page.run_task(self._delayed_remove)
        return super().did_mount()

    def will_unmount(self):
        self._is_mounted = False
        return super().will_unmount()

    def _calculate_position(self):
        return self.index * (self.height + self.spacing)

    async def _animate_enter(self):
        await asyncio.sleep(0.1)
        self.opacity = 1
        self.scale = 1
        self.offset = ft.Offset(0, 0)
        self.update()

    def update_position(self, new_index):
        self.index = new_index
        self.top = self._calculate_position()
        self.update()

    def destroy(self, e):
        self.disable = True

        self.update()
        self.page.run_task(self._animate_exit)

        async def remove_wrapper():
            await self._delayed_remove(self.notification_style.in_duration / 1000)

        self.page.run_task(remove_wrapper)

    async def _delayed_remove(self, delay: float = None):
        if delay is None:
            delay = self.duration / 1000
        await asyncio.sleep(delay)
        if self.page:
            self.page.run_task(self._animate_exit)
        await asyncio.sleep(self.notification_style.out_duration / 1000)
        if self._is_mounted:
            self.remove_cb(self)

    async def _animate_exit(self):
        self.animate_offset.duration = self.notification_style.out_duration
        self.animate_opacity.duration = self.notification_style.out_duration
        self.animate_scale.duration = self.notification_style.out_duration
        self.animate_offset.curve = self.notification_style.out_offset_curve
        self.animate_opacity.curve = self.notification_style.out_opacity_curve
        self.animate_scale.curve = self.notification_style.out_scale_curve
        self.offset = self.notification_style.out_offset
        self.opacity = self.notification_style.out_opacity
        self.scale = self.notification_style.out_scale
        self.update()


class NotificationCenter(ft.Stack):
    def __init__(
        self,
        alignment: ft.alignment = ft.alignment.top_left,
        notification_style: NotificationStyle = None,
    ):
        super().__init__()
        self.notification_style = (
            notification_style if notification_style else NotificationStyle()
        )
        self.notifications = []
        self.notification_width = self.notification_style.width
        self.notification_height = self.notification_style.height
        self.spacing = self.notification_style.spacing
        self.expand = True
        self.alignment = alignment

    def add_notification(
        self,
        content: ft.Control = ft.Container,
        notification_type: str = "info",
        duration: int = 4000,
        notification_style: NotificationStyle = None,
    ):
        new_notification = NotificationBanner(
            index=len(self.notifications),
            remove_cb=self._remove_notification,
            content=content,
            duration=duration,
            notification_type=notification_type,
            notification_style=notification_style
            if notification_style
            else self.notification_style,  # Cambio clave aquí,
        )
        self.notifications.append(new_notification)
        self.controls = self.notifications
        self.update()
        self._rearrange_notifications()

    def _remove_notification(self, notification):
        if notification in self.controls:
            self.controls.remove(notification)
        if notification in self.notifications:
            self.notifications.remove(notification)
        self._rearrange_notifications()
        self.update()

    def _rearrange_notifications(self):
        for new_index, notification in enumerate(self.controls):
            notification.update_position(new_index)
