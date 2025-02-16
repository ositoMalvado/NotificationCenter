![Visitor Count](https://profile-counter.glitch.me/NotificationCenter/count.svg)


# 🔔 Flet Notification Widget

A customizable and animated notification widget for Flet apps. Display beautiful toast-style notifications with smooth animations, multiple types, and flexible positioning. Perfect for user feedback! 🎉


## Features ✨

- 🎨 **4 Notification Types**: Info, Success, Warning, Error with distinct colors/icons
- 🚀 **Smooth Animations**: Customizable entrance/exit animations
- 📍 **Flexible Positioning**: Show notifications on either side (or both!)
- ⚙️ **Full Customization**: Control sizes, durations, colors, and animations
- ⏳ **Auto-dismiss**: Set timeout duration for each notification
- ✖️ **Manual Close**: Users can dismiss notifications instantly
- 🌈 **Theming Support**: Match your app's color scheme

> Example usage:
```Python
import flet as ft
from NotificationCenter import NotificationCenter, NotificationTypes

def main(page: ft.Page):
    nc = NotificationCenter(alignment=ft.alignment.top_right)
    
    # Add notification
    nc.add_notification(
        content=ft.Text("File saved successfully!", color=ft.Colors.BLACK),
        notification_type=NotificationTypes.SUCCESS.value,
        duration=3000
    )
    
    page.add(nc)

ft.app(main)
```


License 📄
MIT License - Feel free to use and modify in your projects! ❤️

Made with 🚀 by SkeletoR
