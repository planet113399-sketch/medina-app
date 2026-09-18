import os
import json
import flet as ft

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

def main(page: ft.Page):
    page.title = "Мединский курс (Часть 1)"
    page.scroll = "auto"
    page.padding = 20

    # Создаем встроенный аудиоузел для мобильных устройств
    audio_player = ft.Audio(autoplay=True)
    page.overlay.append(audio_player)

    lesson_title = ft.Text(size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
    content_column = ft.Column(spacing=20)

    def play_sound(lesson_id, s_idx, i_idx):
        audio_path = os.path.join(AUDIO_DIR, f"lesson_{lesson_id}", f"{lesson_id}_{s_idx}_{i_idx}.mp3")
        if os.path.exists(audio_path):
            audio_player.src = audio_path
            audio_player.update()

    def load_lesson(lesson_num):
        file_path = os.path.join(DATA_DIR, f"lesson_{lesson_num}.json")
        content_column.controls.clear()

        if not os.path.exists(file_path):
            lesson_title.value = f"Урок {lesson_num}"
            content_column.controls.append(ft.Text("Файл этого урока пока не создан."))
            page.update()
            return

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        lesson_id = data.get("lesson_id", lesson_num)
        lesson_title.value = f"Урок {lesson_id}  |  {data.get('title', '')}"

        # 1. БЛОК: ТАБЛИЦА ПРАВИЛ И ГРАММАТИКИ
        rules = data.get("rules_table", [])
        if rules:
            rows = []
            for r in rules:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(r.get("rule", ""), weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(r.get("description", ""))),
                            ft.DataCell(ft.Text(r.get("example", ""), size=16, color=ft.Colors.BLUE_800)),
                        ]
                    )
                )

            border_side = ft.BorderSide(1, ft.Colors.BLUE_200)
            rules_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Правило", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Пояснение", weight=ft.FontWeight.BOLD)),
                    ft.DataColumn(ft.Text("Пример", weight=ft.FontWeight.BOLD)),
                ],
                rows=rows,
                border=ft.Border(top=border_side, bottom=border_side, left=border_side, right=border_side),
                border_radius=8,
            )

            content_column.controls.append(
                ft.Column([
                    ft.Text("📌 Грамматика урока", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                    rules_table
                ])
            )

        # 2. БЛОК: СЛОВАРЬ (НОВЫЕ СЛОВА)
        vocab = data.get("vocabulary", [])
        if vocab:
            vocab_chips = []
            green_border = ft.BorderSide(1, ft.Colors.GREEN_200)
            for item in vocab:
                vocab_chips.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(item.get("arabic", ""), size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_900),
                            ft.Text(item.get("ru", ""), size=14, color=ft.Colors.GREY_800)
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.GREEN_50,
                        padding=10,
                        border_radius=8,
                        border=ft.Border(top=green_border, bottom=green_border, left=green_border, right=green_border),
                        width=160
                    )
                )

            content_column.controls.append(
                ft.Column([
                    ft.Text("📚 Новые слова", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_900),
                    ft.Row(vocab_chips, wrap=True, spacing=10)
                ])
            )

        # 3. БЛОК: ФРАЗЫ И ОЗВУЧКА
        sections = data.get("sections", [])
        if sections:
            content_column.controls.append(
                ft.Text("🔊 Практика и аудио", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_900)
            )

            for s_idx, sec in enumerate(sections):
                for i_idx, item in enumerate(sec.get("items", [])):
                    card = ft.Card(
                        elevation=2,
                        content=ft.Container(
                            padding=15,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text(item.get("arabic", ""), size=22, weight=ft.FontWeight.BOLD),
                                            ft.Text(item.get("ru", ""), size=16, color=ft.Colors.GREY_800),
                                        ],
                                        expand=True
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.PLAY_ARROW,
                                        icon_size=32,
                                        icon_color=ft.Colors.BLUE_600,
                                        on_click=lambda e, l=lesson_id, s=s_idx, i=i_idx: play_sound(l, s, i)
                                    )
                                ]
                            )
                        )
                    )
                    content_column.controls.append(card)

        page.update()

    # Кнопки выбора уроков (с 1 по 11)
    nav_buttons = []
    for i in range(1, 12):
        nav_buttons.append(
            ft.ElevatedButton(f"Урок {i}", on_click=lambda e, num=i: load_lesson(num))
        )

    page.add(
        ft.Column([
            ft.Row(nav_buttons, alignment=ft.MainAxisAlignment.CENTER, wrap=True),
            ft.Divider(height=20),
            lesson_title,
            content_column
        ])
    )

    load_lesson(1)

ft.app(target=main)