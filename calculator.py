"""Задание №3 (средней сложности): Простейший калькулятор."""

import ast
import tkinter as tk
from tkinter import ttk


class SafeCalculatorEvaluator:
    """Безопасный вычислитель простых арифметических выражений."""

    @classmethod
    def evaluate(cls, expression: str) -> float:
        """Вычисляет значение выражения без использования eval."""
        clean_expr = expression.strip().replace("×", "*").replace("÷", "/")
        if not clean_expr:
            raise ValueError("Пустое выражение")

        try:
            node = ast.parse(clean_expr, mode="eval")
        except SyntaxError as exc:
            raise ValueError("Некорректный синтаксис выражения") from exc

        return cls._eval_node(node.body)

    @classmethod
    def _eval_node(cls, node: ast.AST) -> float:
        """Рекурсивно вычисляет значение узла синтаксического дерева."""
        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return float(node.value)

        if isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand)
            if isinstance(node.op, ast.USub):
                return -operand
            if isinstance(node.op, ast.UAdd):
                return operand
            raise ValueError("Неподдерживаемый унарный оператор")

        if isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError("Деление на ноль")
                return left / right
            raise ValueError("Неподдерживаемая бинарная операция")

        raise ValueError(f"Недопустимый элемент выражения: {type(node)}")


class CalculatorApp:
    """Графический интерфейс простейшего калькулятора на Tkinter."""

    def __init__(self, root: tk.Tk) -> None:
        """Инициализирует главное окно калькулятора."""
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("320x420")
        self.root.resizable(False, False)

        self.expression: str = ""
        self.display_var = tk.StringVar(value="0")
        self.should_reset: bool = False

        self._configure_styles()
        self._build_ui()

    def _configure_styles(self) -> None:
        """Настраивает стили для ttk-виджетов калькулятора."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Calc.TButton", font=("Arial", 12))
        style.configure("Op.TButton", font=("Arial", 12, "bold"))
        style.configure("Equal.TButton", font=("Arial", 12, "bold"))

    def _build_ui(self) -> None:
        """Создает элементы пользовательского интерфейса."""
        display_frame = ttk.Frame(self.root, padding="12 12 12 8")
        display_frame.pack(fill=tk.X)

        entry = ttk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 20),
            justify="right",
            state="readonly",
        )
        entry.pack(fill=tk.X, ipady=8)

        keypad_frame = ttk.Frame(self.root, padding="12 4 12 12")
        keypad_frame.pack(fill=tk.BOTH, expand=True)

        for col_idx in range(4):
            keypad_frame.columnconfigure(col_idx, weight=1)
        for row_idx in range(5):
            keypad_frame.rowconfigure(row_idx, weight=1)

        buttons_data = [
            ("C", 0, 0, "Op.TButton", 1),
            ("CE", 0, 1, "Op.TButton", 1),
            ("±", 0, 2, "Op.TButton", 1),
            ("÷", 0, 3, "Op.TButton", 1),
            ("7", 1, 0, "Calc.TButton", 1),
            ("8", 1, 1, "Calc.TButton", 1),
            ("9", 1, 2, "Calc.TButton", 1),
            ("×", 1, 3, "Op.TButton", 1),
            ("4", 2, 0, "Calc.TButton", 1),
            ("5", 2, 1, "Calc.TButton", 1),
            ("6", 2, 2, "Calc.TButton", 1),
            ("-", 2, 3, "Op.TButton", 1),
            ("1", 3, 0, "Calc.TButton", 1),
            ("2", 3, 1, "Calc.TButton", 1),
            ("3", 3, 2, "Calc.TButton", 1),
            ("+", 3, 3, "Op.TButton", 1),
            ("0", 4, 0, "Calc.TButton", 1),
            (".", 4, 1, "Calc.TButton", 1),
            ("=", 4, 2, "Equal.TButton", 2),
        ]

        for text, r_pos, c_pos, style_name, c_span in buttons_data:
            self._create_calc_button(
                keypad_frame, text, r_pos, c_pos, style_name, c_span
            )

    def _create_calc_button(
        self,
        parent: ttk.Frame,
        text: str,
        row_pos: int,
        col_pos: int,
        style_name: str,
        col_span: int,
    ) -> ttk.Button:
        """Создает кнопку с корректным замыканием обработчика клика."""
        btn = ttk.Button(
            parent,
            text=text,
            style=style_name,
            command=lambda: self.on_button_click(text),
        )
        btn.grid(
            row=row_pos,
            column=col_pos,
            columnspan=col_span,
            sticky="nsew",
            padx=3,
            pady=3,
        )
        return btn

    def on_button_click(self, char: str) -> None:
        """Обрабатывает нажатие клавиши калькулятора."""
        if char == "C":
            self.clear_all()
        elif char == "CE":
            self.clear_entry()
        elif char == "±":
            self.toggle_sign()
        elif char == "=":
            self.calculate_result()
        elif char in {"+", "-", "×", "÷"}:
            self.add_operator(char)
        elif char == ".":
            self.add_decimal_point()
        else:
            self.add_digit(char)

    def add_digit(self, digit: str) -> None:
        """Добавляет цифру к текущему выражению."""
        if self.should_reset:
            self.expression = ""
            self.should_reset = False

        if self.expression == "0":
            self.expression = digit
        else:
            self.expression += digit
        self.display_var.set(self.expression)

    def add_decimal_point(self) -> None:
        """Добавляет десятичную точку к числу."""
        if self.should_reset:
            self.expression = "0"
            self.should_reset = False

        parts = (
            self.expression.replace("×", " ")
            .replace("÷", " ")
            .replace("+", " ")
            .replace("-", " ")
            .split()
        )
        current_token = parts[-1] if parts else ""

        if "." not in current_token:
            if not self.expression or self.expression[-1] in "+-×÷":
                self.expression += "0."
            else:
                self.expression += "."
            self.display_var.set(self.expression)

    def add_operator(self, op: str) -> None:
        """Добавляет арифметический оператор к выражению."""
        self.should_reset = False
        if not self.expression:
            if op == "-":
                self.expression = "-"
                self.display_var.set(self.expression)
            return

        if self.expression[-1] in "+-×÷":
            self.expression = self.expression[:-1] + op
        else:
            self.expression += op
        self.display_var.set(self.expression)

    def toggle_sign(self) -> None:
        """Меняет знак текущего числа на противоположный."""
        if not self.expression or self.expression == "0":
            return
        try:
            val = SafeCalculatorEvaluator.evaluate(self.expression)
            val = -val
            self.expression = self._format_number(val)
            self.display_var.set(self.expression)
        except (ValueError, ZeroDivisionError):
            pass

    def calculate_result(self) -> None:
        """Вычисляет результат текущего выражения."""
        if not self.expression:
            return

        try:
            val = SafeCalculatorEvaluator.evaluate(self.expression)
            formatted = self._format_number(val)
            self.display_var.set(formatted)
            self.expression = formatted
            self.should_reset = True
        except ZeroDivisionError:
            self.display_var.set("Ошибка: деление на 0")
            self.expression = ""
            self.should_reset = True
        except ValueError:
            self.display_var.set("Ошибка")
            self.expression = ""
            self.should_reset = True

    def clear_all(self) -> None:
        """Полностью очищает состояние калькулятора."""
        self.expression = ""
        self.display_var.set("0")
        self.should_reset = False

    def clear_entry(self) -> None:
        """Удаляет последний введенный символ."""
        if self.should_reset:
            self.clear_all()
            return

        if len(self.expression) > 1:
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression)
        else:
            self.expression = ""
            self.display_var.set("0")

    @staticmethod
    def _format_number(val: float) -> str:
        """Форматирует число, удаляя лишнюю дробную часть."""
        if val.is_integer():
            return str(int(val))
        return f"{val:.6g}"


def main() -> None:
    """Точка входа в приложение калькулятора."""
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
