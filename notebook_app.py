"""Задание №5 (средней сложности): Программа со вкладками (Notebook)."""

import sys
import tkinter as tk
from tkinter import messagebox, ttk


class NotebookApp:
    """Приложение с многовкладочным интерфейсом на основе ttk.Notebook."""

    def __init__(self, root: tk.Tk) -> None:
        """Инициализирует главное окно и вкладки приложения."""
        self.root = root
        self.root.title("Программа со вкладками (Notebook)")
        self.root.geometry("520x460")
        self.root.minsize(460, 400)

        self._configure_styles()
        self._build_notebook()

    def _configure_styles(self) -> None:
        """Настраивает визуальные стили оформления вкладок."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TNotebook.Tab",
            font=("Arial", 10, "bold"),
            padding=[10, 5],
        )
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        style.configure(
            "Result.TLabel",
            font=("Arial", 11, "bold"),
            foreground="#2980b9",
        )

    def _build_notebook(self) -> None:
        """Создает виджет Notebook и размещает вкладки."""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        greeting_tab = ttk.Frame(notebook, padding="15")
        bmi_tab = ttk.Frame(notebook, padding="15")
        about_tab = ttk.Frame(notebook, padding="15")

        notebook.add(greeting_tab, text="Приветствие")
        notebook.add(bmi_tab, text="Расчет ИМТ")
        notebook.add(about_tab, text="О программе")

        self._init_greeting_tab(greeting_tab)
        self._init_bmi_tab(bmi_tab)
        self._init_about_tab(about_tab)

    def _init_greeting_tab(self, parent: ttk.Frame) -> None:
        """Формирует содержимое вкладки персонализированного приветствия."""
        header = ttk.Label(
            parent,
            text="Персонализированное приветствие",
            style="Header.TLabel",
        )
        header.pack(anchor="w", pady=(0, 15))

        name_frame = ttk.Frame(parent)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="Введите ваше имя:").pack(anchor="w")
        self.name_entry = ttk.Entry(name_frame, font=("Arial", 10))
        self.name_entry.pack(fill=tk.X, pady=3)

        style_frame = ttk.Frame(parent)
        style_frame.pack(fill=tk.X, pady=5)
        ttk.Label(style_frame, text="Форма обращения:").pack(anchor="w")
        self.greeting_combobox = ttk.Combobox(
            style_frame,
            values=["Привет", "Здравствуйте", "Добро пожаловать"],
            state="readonly",
        )
        self.greeting_combobox.current(1)
        self.greeting_combobox.pack(fill=tk.X, pady=3)

        btn = ttk.Button(
            parent,
            text="Сформировать приветствие",
            command=self._on_greet_click,
        )
        btn.pack(pady=12)

        self.greeting_result = ttk.Label(
            parent,
            text="",
            style="Result.TLabel",
            wraplength=460,
        )
        self.greeting_result.pack(pady=10)

    def _on_greet_click(self) -> None:
        """Обрабатывает нажатие кнопки формирования приветствия."""
        name = self.name_entry.get().strip()
        salutation = self.greeting_combobox.get()
        if not name:
            messagebox.showwarning(
                "Предупреждение",
                "Пожалуйста, введите имя для приветствия.",
            )
            return
        msg = f"{salutation}, {name}! Рады вас видеть."
        self.greeting_result.config(text=msg)

    def _init_bmi_tab(self, parent: ttk.Frame) -> None:
        """Формирует содержимое вкладки расчета индекса массы тела."""
        header = ttk.Label(
            parent,
            text="Калькулятор индекса массы тела (ИМТ)",
            style="Header.TLabel",
        )
        header.pack(anchor="w", pady=(0, 15))

        inputs_frame = ttk.Frame(parent)
        inputs_frame.pack(fill=tk.X, pady=5)

        ttk.Label(inputs_frame, text="Рост (см):").grid(
            row=0, column=0, sticky="w", pady=4
        )
        self.height_entry = ttk.Entry(inputs_frame, width=15)
        self.height_entry.grid(row=0, column=1, sticky="w", padx=10, pady=4)

        ttk.Label(inputs_frame, text="Вес (кг):").grid(
            row=1, column=0, sticky="w", pady=4
        )
        self.weight_entry = ttk.Entry(inputs_frame, width=15)
        self.weight_entry.grid(row=1, column=1, sticky="w", padx=10, pady=4)

        calc_btn = ttk.Button(
            parent,
            text="Рассчитать ИМТ",
            command=self._on_calc_bmi,
        )
        calc_btn.pack(pady=12)

        self.bmi_result = ttk.Label(
            parent,
            text="",
            style="Result.TLabel",
        )
        self.bmi_result.pack(pady=6)

        self.bmi_category = ttk.Label(
            parent,
            text="",
            font=("Arial", 10),
        )
        self.bmi_category.pack(pady=2)

    def _on_calc_bmi(self) -> None:
        """Вычисляет ИМТ и категорию массы тела."""
        height_str = self.height_entry.get().strip()
        weight_str = self.weight_entry.get().strip()

        try:
            height_cm = float(height_str)
            weight_kg = float(weight_str)
            if height_cm <= 0 or weight_kg <= 0:
                raise ValueError("Значения должны быть больше 0.")
        except ValueError:
            messagebox.showerror(
                "Ошибка ввода",
                "Укажите корректные числовые значения роста и веса.",
            )
            return

        height_m = height_cm / 100.0
        bmi = weight_kg / (height_m * height_m)

        if bmi < 18.5:
            cat = "Дефицит массы тела"
            color = "#e67e22"
        elif 18.5 <= bmi < 25.0:
            cat = "Нормальная масса тела"
            color = "#27ae60"
        elif 25.0 <= bmi < 30.0:
            cat = "Избыточная масса тела (предожирение)"
            color = "#d35400"
        else:
            cat = "Ожирение"
            color = "#c0392b"

        self.bmi_result.config(text=f"ИМТ: {bmi:.2f}", foreground=color)
        self.bmi_category.config(text=f"Категория: {cat}")

    def _init_about_tab(self, parent: ttk.Frame) -> None:
        """Формирует содержимое вкладки со сведениями о программе."""
        header = ttk.Label(
            parent,
            text="Сведения о проекте",
            style="Header.TLabel",
        )
        header.pack(anchor="w", pady=(0, 15))

        info_text = (
            "Дисциплина: Методы и технологии программирования\n"
            "Лабораторная работа №5: Визуальное программирование на Python\n"
            "Задание: Средняя сложность №5 (Программа со вкладками)\n"
            "Вариант: 3\n"
            "Студент: Берченёв Егор Константинович\n"
            "Группа: 220042-11\n\n"
            f"Версия среды Python: {sys.version.split()[0]}\n"
            "Библиотека GUI: Tkinter / ttk"
        )

        label = ttk.Label(
            parent,
            text=info_text,
            justify=tk.LEFT,
            font=("Arial", 10),
        )
        label.pack(anchor="w", pady=5)

        exit_btn = ttk.Button(
            parent,
            text="Закрыть приложение",
            command=self.root.destroy,
        )
        exit_btn.pack(pady=20)


def main() -> None:
    """Точка входа в приложение с вкладками."""
    root = tk.Tk()
    NotebookApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
