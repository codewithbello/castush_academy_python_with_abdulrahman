import flet as ft

def main(page: ft.Page):
    page.title = "BMI Calculator"

    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    title = ft.Text("BMI Calculator", size=30, weight=ft.FontWeight.BOLD)
    name = ft.TextField(value=" ", label="Name", width=200)
    weight = ft.TextField(value=" ", label="Weight (kg)", width=200)
    height = ft.TextField(value=" ", label="Height (cm)", width=200)
    result = ft.Text(value=" ", size=20, weight=ft.FontWeight.BOLD)

    def calculate_bmi(e):
        try:
            w = float(weight.value)
            h = float(height.value) / 100  # convert cm to meters
            bmi = w / (h * h)
            result.value = f"{name.value} your BMI is: {bmi:.2f}"
        except ValueError:
            result.value = "Please enter valid numbers for weight and height."
        page.update()

    page.add(
       ft.Row(
           controls=[
                ft.Column(
            controls=[
                title,
                name,
                weight,
                height,
                ft.ElevatedButton("Calculate BMI", on_click=calculate_bmi),
                result
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
    )
           ],
           alignment=ft.MainAxisAlignment.CENTER,
       )
    )
   
   


ft.app(main)