"""

Installation:
    pip install "psycopg[binary]" psycopg2-binary asyncpg python-dotenv

Rescources:
    https://neon.com/docs/guides/python
"""

import flet as ft
import psycopg
from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv()

# Neon DB connection string (replace with your actual credentials)
NEON_DB_URL = os.getenv("NEON_DB_URL")

# Connect to Neon
conn = psycopg.connect(NEON_DB_URL)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS BMI_RECORDS (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    weight FLOAT NOT NULL,
    height FLOAT NOT NULL,
    bmi FLOAT NOT NULL
)
""")
conn.commit()

def main(page: ft.Page):
    page.title = "BMI Calculator"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    title = ft.Text("BMI Calculator", size=30, weight=ft.FontWeight.BOLD)
    name_field = ft.TextField(label="Name", width=200)
    weight_field = ft.TextField(label="Weight (kg)", width=200)
    height_field = ft.TextField(label="Height (cm)", width=200)
    result = ft.Text(size=20, weight=ft.FontWeight.BOLD)
   
    # Data Table
    records_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Weight (kg)"), numeric=True),
            ft.DataColumn(ft.Text("Height (cm)"), numeric=True),
            ft.DataColumn(ft.Text("BMI"), numeric=True),
        ],
        rows=[]
    )

    def calculate_bmi(e):
        try:
            name = name_field.value.strip()
            w = float(weight_field.value)
            h = float(height_field.value) / 100  # convert cm to meters
            bmi = w / (h * h)
            result.value = f"{name} your BMI is: {bmi:.2f}"

            # Insert into database
            if name and w > 0 and h > 0:
                cur.execute(
                    "INSERT INTO BMI_RECORDS (name, weight, height, bmi) VALUES (%s, %s, %s, %s)", 
                    (name, w, h*100, bmi)
                )
                conn.commit()

        except ValueError:
            result.value = "Please enter valid numbers for weight and height."
        page.update()

    def clear_textfields(e):
        name_field.value = ""
        weight_field.value = ""
        height_field.value = ""
        result.value = ""
        page.update()
    
    def fetch_records(e):
        # Clear existing rows
        records_table.rows.clear()
        
        # Execute query and fetch all records
        cur.execute("SELECT name, weight, height, bmi FROM BMI_RECORDS ORDER BY id DESC")
        db_records = cur.fetchall()
        
        # Add each record as a DataRow to the DataTable
        for record in db_records:
            name, weight, height, bmi = record
            records_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(ft.Text(f"{weight:.1f}")),
                        ft.DataCell(ft.Text(f"{height:.1f}")),
                        ft.DataCell(ft.Text(f"{bmi:.2f}")),
                    ],
                )
            )
        page.update()

    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        title,
                        name_field,
                        weight_field,
                        height_field,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton("Calculate BMI", on_click=calculate_bmi),
                                ft.OutlinedButton("Clear", on_click=clear_textfields),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        result,
                        ft.FilledButton(text="Show Records", on_click=fetch_records),
                        records_table,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )   

ft.app(main)