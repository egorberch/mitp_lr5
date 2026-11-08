"""Задание №7 (повышенная сложность): GUI для работы с SQLite."""

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Optional, Tuple


class DatabaseManager:
    """Инкапсулирует операции с локальной базой данных SQLite."""

    def __init__(self, db_path: str = "students.db") -> None:
        """Инициализирует подключение к базе данных и создает таблицу."""
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self) -> None:
        """Создает таблицу студентов, если она еще не создана."""
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    group_name TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    grade INTEGER NOT NULL
                )
                """
            )

    def add_record(
        self, full_name: str, group_name: str, subject: str, grade: int
    ) -> Optional[int]:
        """Добавляет новую запись в таблицу."""
        with self.connection:
            cursor = self.connection.execute(
                """
                INSERT INTO students (full_name, group_name, subject, grade)
                VALUES (?, ?, ?, ?)
                """,
                (full_name, group_name, subject, grade),
            )
            return cursor.lastrowid

    def get_all_records(self) -> List[Tuple]:
        """Возвращает все записи из таблицы студентов."""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, full_name, group_name, subject, grade "
            "FROM students ORDER BY id ASC"
        )
        return cursor.fetchall()

    def search_records(self, query: str) -> List[Tuple]:
        """Выполняет поиск записей по ФИО или группе."""
        cursor = self.connection.cursor()
        param = f"%{query}%"
        cursor.execute(
            """
            SELECT id, full_name, group_name, subject, grade
            FROM students
            WHERE full_name LIKE ? OR group_name LIKE ?
            ORDER BY id ASC
            """,
            (param, param),
        )
        return cursor.fetchall()

    def update_record(
        self,
        record_id: int,
        full_name: str,
        group_name: str,
        subject: str,
        grade: int,
    ) -> None:
        """Обновляет существующую запись в таблице."""
        with self.connection:
            self.connection.execute(
                """
                UPDATE students
                SET full_name = ?, group_name = ?, subject = ?, grade = ?
                WHERE id = ?
                """,
                (full_name, group_name, subject, grade, record_id),
            )

    def delete_record(self, record_id: int) -> None:
        """Удаляет запись по ее первичному ключу."""
        with self.connection:
            self.connection.execute(
                "DELETE FROM students WHERE id = ?",
                (record_id,),
            )

    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        self.connection.close()


class SQLiteApp:
    """Графический интерфейс для управления записями в SQLite."""

    def __init__(self, root: tk.Tk, db_path: str = "students.db") -> None:
        """Инициализирует графическое приложение и загружает данные."""
        self.root = root
        self.root.title("Управление базой данных SQLite")
        self.root.geometry("760x540")
        self.root.minsize(680, 480)

        self.db = DatabaseManager(db_path)
        self.selected_id: Optional[int] = None

        self._configure_styles()
        self._build_ui()
        self.load_records()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _configure_styles(self) -> None:
        """Настраивает визуальные стили элементов управления."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=24)

    def _build_ui(self) -> None:
        """Строит пользовательский интерфейс приложения."""
        main_frame = ttk.Frame(self.root, padding="12")
        main_frame.pack(fill=tk.BOTH, expand=True)

        search_frame = ttk.LabelFrame(main_frame, text="Поиск", padding="8")
        search_frame.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(search_frame, text="ФИО / группа:").pack(
            side=tk.LEFT, padx=5
        )
        self.search_entry = ttk.Entry(search_frame, width=28)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", lambda _: self._on_search())

        ttk.Button(
            search_frame, text="Найти", command=self._on_search
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            search_frame, text="Сбросить", command=self._on_reset_search
        ).pack(side=tk.LEFT, padx=4)

        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=4)

        columns = ("id", "full_name", "group_name", "subject", "grade")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("full_name", text="ФИО студента")
        self.tree.heading("group_name", text="Группа")
        self.tree.heading("subject", text="Дисциплина")
        self.tree.heading("grade", text="Оценка")

        self.tree.column("id", width=45, anchor="center")
        self.tree.column("full_name", width=220, anchor="w")
        self.tree.column("group_name", width=110, anchor="center")
        self.tree.column("subject", width=240, anchor="w")
        self.tree.column("grade", width=70, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_select_row)

        form_frame = ttk.LabelFrame(
            main_frame, text="Данные студента", padding="10"
        )
        form_frame.pack(fill=tk.X, pady=8)

        for col_idx in range(4):
            form_frame.columnconfigure(col_idx, weight=1)

        ttk.Label(form_frame, text="ФИО:").grid(
            row=0, column=0, sticky="w", padx=4, pady=3
        )
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=4, pady=3)

        ttk.Label(form_frame, text="Группа:").grid(
            row=0, column=2, sticky="w", padx=4, pady=3
        )
        self.group_entry = ttk.Entry(form_frame)
        self.group_entry.grid(row=0, column=3, sticky="ew", padx=4, pady=3)

        ttk.Label(form_frame, text="Дисциплина:").grid(
            row=1, column=0, sticky="w", padx=4, pady=3
        )
        self.subject_entry = ttk.Entry(form_frame)
        self.subject_entry.insert(
            0, "Методы и технологии программирования"
        )
        self.subject_entry.grid(row=1, column=1, sticky="ew", padx=4, pady=3)

        ttk.Label(form_frame, text="Оценка:").grid(
            row=1, column=2, sticky="w", padx=4, pady=3
        )
        self.grade_combobox = ttk.Combobox(
            form_frame, values=["2", "3", "4", "5"], state="readonly"
        )
        self.grade_combobox.current(3)
        self.grade_combobox.grid(row=1, column=3, sticky="ew", padx=4, pady=3)

        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=4)

        ttk.Button(
            buttons_frame, text="Добавить", command=self._on_add
        ).pack(side=tk.LEFT, padx=3)
        ttk.Button(
            buttons_frame, text="Обновить", command=self._on_update
        ).pack(side=tk.LEFT, padx=3)
        ttk.Button(
            buttons_frame, text="Удалить", command=self._on_delete
        ).pack(side=tk.LEFT, padx=3)
        ttk.Button(
            buttons_frame, text="Очистить форму", command=self.clear_form
        ).pack(side=tk.LEFT, padx=3)

        self.status_label = ttk.Label(
            main_frame, text="", font=("Arial", 9), foreground="#7f8c8d"
        )
        self.status_label.pack(anchor="w", pady=(4, 0))

    def load_records(self, records: Optional[List[Tuple]] = None) -> None:
        """Очищает и наполняет таблицу строками из базы данных."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        data = self.db.get_all_records() if records is None else records
        for row_data in data:
            self.tree.insert("", tk.END, values=row_data)

        self.status_label.config(text=f"Всего записей в базе: {len(data)}")

    def _on_select_row(self, _event: tk.Event) -> None:
        """Заполняет форму данными выбранной строки."""
        selection = self.tree.selection()
        if not selection:
            return

        values = self.tree.item(selection[0], "values")
        if values:
            self.selected_id = int(values[0])
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])

            self.group_entry.delete(0, tk.END)
            self.group_entry.insert(0, values[2])

            self.subject_entry.delete(0, tk.END)
            self.subject_entry.insert(0, values[3])

            self.grade_combobox.set(str(values[4]))

    def _on_add(self) -> None:
        """Добавляет новую запись в БД."""
        data = self._validate_inputs()
        if not data:
            return

        full_name, group_name, subject, grade = data
        self.db.add_record(full_name, group_name, subject, grade)
        self.load_records()
        self.clear_form()
        messagebox.showinfo("Успех", "Запись успешно добавлена в базу данных.")

    def _on_update(self) -> None:
        """Обновляет выбранную запись в базе данных."""
        if self.selected_id is None:
            messagebox.showwarning(
                "Предупреждение", "Выберите строку для редактирования."
            )
            return

        data = self._validate_inputs()
        if not data:
            return

        full_name, group_name, subject, grade = data
        self.db.update_record(
            self.selected_id, full_name, group_name, subject, grade
        )
        self.load_records()
        self.clear_form()
        messagebox.showinfo("Успех", "Запись успешно обновлена.")

    def _on_delete(self) -> None:
        """Удаляет выбранную запись из базы данных."""
        if self.selected_id is None:
            messagebox.showwarning(
                "Предупреждение", "Выберите запись для удаления."
            )
            return

        confirm = messagebox.askyesno(
            "Подтверждение удаления",
            f"Вы точно хотите удалить запись #{self.selected_id}?",
        )
        if confirm:
            self.db.delete_record(self.selected_id)
            self.load_records()
            self.clear_form()
            messagebox.showinfo("Успех", "Запись удалена.")

    def _on_search(self) -> None:
        """Выполняет фильтрацию таблицы по поисковой строке."""
        query = self.search_entry.get().strip()
        if not query:
            self.load_records()
            return
        results = self.db.search_records(query)
        self.load_records(results)

    def _on_reset_search(self) -> None:
        """Сбрасывает поисковый запрос и отображает все записи."""
        self.search_entry.delete(0, tk.END)
        self.load_records()

    def clear_form(self) -> None:
        """Очищает поля ввода формы."""
        self.selected_id = None
        self.name_entry.delete(0, tk.END)
        self.group_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.subject_entry.insert(
            0, "Методы и технологии программирования"
        )
        self.grade_combobox.current(3)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

    def _validate_inputs(self) -> Optional[Tuple[str, str, str, int]]:
        """Проверяет корректность введенных в форму значений."""
        name = self.name_entry.get().strip()
        group = self.group_entry.get().strip()
        subject = self.subject_entry.get().strip()
        grade_str = self.grade_combobox.get().strip()

        if not name or not group or not subject or not grade_str:
            messagebox.showerror(
                "Ошибка валидации", "Все поля формы должны быть заполнены."
            )
            return None

        try:
            grade = int(grade_str)
            if grade not in {2, 3, 4, 5}:
                raise ValueError("Оценка должна быть от 2 до 5")
        except ValueError:
            messagebox.showerror(
                "Ошибка валидации",
                "Оценка должна быть целым числом от 2 до 5.",
            )
            return None

        return name, group, subject, grade

    def _on_close(self) -> None:
        """Закрывает соединение с БД и главное окно."""
        self.db.close()
        self.root.destroy()


def main() -> None:
    """Точка входа в приложение базы данных SQLite."""
    root = tk.Tk()
    SQLiteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
