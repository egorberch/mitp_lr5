"""Задание №9 (средней сложности): Цветная панель."""

import random
import tkinter as tk
from tkinter import colorchooser, ttk


class ColorPanelApp:
    """Графическое приложение с интерактивной цветной панелью."""

    DEFAULT_COLOR = "#3498DB"

    PRESETS = [
        ("Красный", "#E74C3C"),
        ("Зеленый", "#2ECC71"),
        ("Синий", "#3498DB"),
        ("Оранжевый", "#E67E22"),
        ("Фиолетовый", "#9B59B6"),
        ("Бирюзовый", "#1ABC9C"),
    ]

    def __init__(self, root: tk.Tk) -> None:
        """Инициализирует элементы окна цветной панели."""
        self.root = root
        self.root.title("Цветная панель")
        self.root.geometry("460x480")
        self.root.minsize(400, 420)

        self.current_color = self.DEFAULT_COLOR

        self._build_ui()
        self.set_color(self.DEFAULT_COLOR, "Исходный синий")

    def _build_ui(self) -> None:
        """Строит визуальные компоненты окна."""
        container = ttk.Frame(self.root, padding="15")
        container.pack(fill=tk.BOTH, expand=True)

        header = ttk.Label(
            container,
            text="Интерактивная панель смены цвета",
            font=("Arial", 12, "bold"),
        )
        header.pack(pady=(0, 10))

        self.panel = tk.Frame(
            container,
            bg=self.current_color,
            relief=tk.RIDGE,
            bd=3,
        )
        self.panel.pack(fill=tk.BOTH, expand=True, pady=10)

        self.color_title = tk.Label(
            self.panel,
            text="",
            font=("Arial", 14, "bold"),
            bg=self.current_color,
        )
        self.color_title.pack(expand=True, pady=(20, 2))

        self.color_hex = tk.Label(
            self.panel,
            text="",
            font=("Courier New", 12),
            bg=self.current_color,
        )
        self.color_hex.pack(expand=True, pady=(0, 20))

        presets_frame = ttk.LabelFrame(
            container, text="Быстрые цвета", padding="8"
        )
        presets_frame.pack(fill=tk.X, pady=6)

        for idx, (name, hex_val) in enumerate(self.PRESETS):
            self._create_preset_button(presets_frame, name, hex_val, idx)

        actions_frame = ttk.Frame(container)
        actions_frame.pack(fill=tk.X, pady=(6, 0))
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)
        actions_frame.columnconfigure(2, weight=1)

        random_btn = ttk.Button(
            actions_frame,
            text="Случайный цвет",
            command=self._on_random_color,
        )
        random_btn.grid(row=0, column=0, sticky="nsew", padx=2)

        picker_btn = ttk.Button(
            actions_frame,
            text="Палитра...",
            command=self._on_choose_color,
        )
        picker_btn.grid(row=0, column=1, sticky="nsew", padx=2)

        reset_btn = ttk.Button(
            actions_frame,
            text="Сброс",
            command=lambda: self.set_color(
                self.DEFAULT_COLOR, "Исходный синий"
            ),
        )
        reset_btn.grid(row=0, column=2, sticky="nsew", padx=2)

    def _create_preset_button(
        self, parent: ttk.LabelFrame, name: str, hex_val: str, idx: int
    ) -> None:
        """Создает кнопку цветового пресета."""
        btn = ttk.Button(
            parent,
            text=name,
            command=lambda: self.set_color(hex_val, name),
        )
        btn.grid(
            row=idx // 3,
            column=idx % 3,
            sticky="nsew",
            padx=3,
            pady=3,
        )
        parent.columnconfigure(idx % 3, weight=1)

    def set_color(self, hex_code: str, name: str = "") -> None:
        """Устанавливает цвет панели и настраивает контрастный текст."""
        self.current_color = hex_code.upper()
        contrast_fg = self._get_contrast_color(self.current_color)

        self.panel.config(bg=self.current_color)
        display_name = name if name else "Выбранный цвет"
        self.color_title.config(
            text=display_name,
            bg=self.current_color,
            fg=contrast_fg,
        )
        self.color_hex.config(
            text=f"HEX: {self.current_color}",
            bg=self.current_color,
            fg=contrast_fg,
        )

    def _on_random_color(self) -> None:
        """Генерирует и применяет случайный оттенок."""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        hex_color = f"#{r:02X}{g:02X}{b:02X}"
        self.set_color(hex_color, "Случайный цвет")

    def _on_choose_color(self) -> None:
        """Открывает стандартный диалог выбора цвета."""
        chosen = colorchooser.askcolor(
            color=self.current_color,
            title="Выберите желаемый цвет",
        )
        if chosen and chosen[1]:
            self.set_color(chosen[1], "Пользовательский цвет")

    @staticmethod
    def _get_contrast_color(hex_code: str) -> str:
        """Вычисляет контрастный цвет текста (черный или белый)."""
        cleaned = hex_code.lstrip("#")
        if len(cleaned) != 6:
            return "#FFFFFF"
        r = int(cleaned[0:2], 16)
        g = int(cleaned[2:4], 16)
        b = int(cleaned[4:6], 16)
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        return "#000000" if luminance > 140 else "#FFFFFF"


def main() -> None:
    """Точка входа в программу цветной панели."""
    root = tk.Tk()
    ColorPanelApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
