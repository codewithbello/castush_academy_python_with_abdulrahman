"""
Link:
    https://flet.dev/docs/

Installation:
    pip install flet


To run in then terminal (press Ctrl + J):
    flet run Project-4-Flet-App_1.py
    or
    flet run --web Project-4-Flet-App_1.py

To Cancle:
    Ctrl + C
"""

import flet as ft


def main(page: ft.Page):
    page.title = "Flet Counter Example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
   
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT,
                               width=100)
    
    def minus_click(e):
        if int(txt_number.value) > 0:
            txt_number.value = str(int(txt_number.value) - 1)
            page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
           controls= [
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
               txt_number,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )






ft.app(main)