"""Задание №3 (повышенная сложность): Игра «Кликер»."""

import tkinter as tk
from tkinter import messagebox, ttk


class ClickerGameApp:
    """Интерактивная игра-кликер с улучшениями и пассивным доходом."""

    def __init__(self, root: tk.Tk) -> None:
        """Инициализирует состояние игры и пользовательский интерфейс."""
        self.root = root
        self.root.title("Игра «Кликер»")
        self.root.geometry("480x560")
        self.root.minsize(440, 500)

        self.score: int = 0
        self.click_power: int = 1
        self.passive_income: int = 0
        self.total_clicks: int = 0

        self.upgrade_power_cost: int = 15
        self.upgrade_auto_cost: int = 30
        self.upgrade_mega_cost: int = 120

        self._is_running: bool = True

        self._configure_styles()
        self._build_ui()
        self._update_ui_state()

        self.root.after(1000, self._passive_income_loop)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _configure_styles(self) -> None:
        """Настраивает графические стили компонентов."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Score.TLabel",
            font=("Arial", 22, "bold"),
            foreground="#2c3e50",
        )
        style.configure(
            "Stat.TLabel",
            font=("Arial", 10),
            foreground="#7f8c8d",
        )
        style.configure("Shop.TLabelframe", font=("Arial", 10, "bold"))

    def _build_ui(self) -> None:
        """Создает элементы игрового поля и магазина апгрейдов."""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        score_frame = ttk.Frame(main_frame)
        score_frame.pack(fill=tk.X, pady=(0, 10))

        self.score_label = ttk.Label(
            score_frame,
            text="Счет: 0 монет",
            style="Score.TLabel",
            anchor="center",
        )
        self.score_label.pack(fill=tk.X)

        self.stat_label = ttk.Label(
            score_frame,
            text="",
            style="Stat.TLabel",
            anchor="center",
        )
        self.stat_label.pack(fill=tk.X, pady=3)

        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        self.level_label = ttk.Label(
            progress_frame,
            text="Уровень 1",
            font=("Arial", 9, "bold"),
        )
        self.level_label.pack(anchor="w")
        self.progressbar = ttk.Progressbar(
            progress_frame,
            orient="horizontal",
            mode="determinate",
            maximum=100,
        )
        self.progressbar.pack(fill=tk.X, pady=2)

        click_frame = ttk.Frame(main_frame, padding="10")
        click_frame.pack(fill=tk.X, pady=10)

        self.click_button = tk.Button(
            click_frame,
            text="КЛИКНИ МЕНЯ!\n(+1)",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            command=self._on_click,
        )
        self.click_button.pack(fill=tk.X, ipady=15)

        shop_frame = ttk.LabelFrame(
            main_frame, text="Магазин улучшений", padding="10"
        )
        shop_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        for col_idx in range(2):
            shop_frame.columnconfigure(col_idx, weight=1)

        self.power_btn = ttk.Button(
            shop_frame,
            text="",
            command=self._buy_power_upgrade,
        )
        self.power_btn.grid(
            row=0, column=0, columnspan=2, sticky="nsew", pady=4
        )

        self.auto_btn = ttk.Button(
            shop_frame,
            text="",
            command=self._buy_auto_upgrade,
        )
        self.auto_btn.grid(
            row=1, column=0, columnspan=2, sticky="nsew", pady=4
        )

        self.mega_btn = ttk.Button(
            shop_frame,
            text="",
            command=self._buy_mega_upgrade,
        )
        self.mega_btn.grid(
            row=2, column=0, columnspan=2, sticky="nsew", pady=4
        )

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(5, 0))

        reset_btn = ttk.Button(
            bottom_frame,
            text="Сбросить игру",
            command=self._reset_game,
        )
        reset_btn.pack(side=tk.RIGHT)

    def _on_click(self) -> None:
        """Обрабатывает ручной клик по игровой кнопке."""
        self.score += self.click_power
        self.total_clicks += 1
        self._update_ui_state()

    def _buy_power_upgrade(self) -> None:
        """Покупает улучшение базовой силы клика (+1)."""
        if self.score >= self.upgrade_power_cost:
            self.score -= self.upgrade_power_cost
            self.click_power += 1
            self.upgrade_power_cost = int(self.upgrade_power_cost * 1.5)
            self._update_ui_state()

    def _buy_auto_upgrade(self) -> None:
        """Покупает автокликер (+1 пассивный доход в секунду)."""
        if self.score >= self.upgrade_auto_cost:
            self.score -= self.upgrade_auto_cost
            self.passive_income += 1
            self.upgrade_auto_cost = int(self.upgrade_auto_cost * 1.6)
            self._update_ui_state()

    def _buy_mega_upgrade(self) -> None:
        """Покупает мега-клик (+5 к силе клика)."""
        if self.score >= self.upgrade_mega_cost:
            self.score -= self.upgrade_mega_cost
            self.click_power += 5
            self.upgrade_mega_cost = int(self.upgrade_mega_cost * 1.7)
            self._update_ui_state()

    def _passive_income_loop(self) -> None:
        """Периодически начисляет пассивный доход раз в секунду."""
        if not self._is_running:
            return
        if self.passive_income > 0:
            self.score += self.passive_income
            self._update_ui_state()
        self.root.after(1000, self._passive_income_loop)

    def _update_ui_state(self) -> None:
        """Синхронизирует графический интерфейс с состоянием игры."""
        self.score_label.config(text=f"Счет: {self.score} монет")
        self.stat_label.config(
            text=(
                f"Сила клика: +{self.click_power} | "
                f"Доход: +{self.passive_income}/сек | "
                f"Кликов: {self.total_clicks}"
            )
        )
        self.click_button.config(text=f"КЛИКНИ МЕНЯ!\n(+{self.click_power})")

        level = (self.total_clicks // 25) + 1
        progress_val = (self.total_clicks % 25) * 4
        self.level_label.config(
            text=f"Уровень {level} (до уровня {level + 1})"
        )
        self.progressbar["value"] = progress_val

        power_ok = self.score >= self.upgrade_power_cost
        self.power_btn.config(
            text=f"Усилить клик (+1) — {self.upgrade_power_cost} монет",
            state=tk.NORMAL if power_ok else tk.DISABLED,
        )
        auto_ok = self.score >= self.upgrade_auto_cost
        self.auto_btn.config(
            text=f"Автокликер (+1/сек) — {self.upgrade_auto_cost} монет",
            state=tk.NORMAL if auto_ok else tk.DISABLED,
        )
        mega_ok = self.score >= self.upgrade_mega_cost
        self.mega_btn.config(
            text=f"Мега-клик (+5) — {self.upgrade_mega_cost} монет",
            state=tk.NORMAL if mega_ok else tk.DISABLED,
        )

    def _reset_game(self) -> None:
        """Сбрасывает прогресс игры после подтверждения пользователя."""
        confirm = messagebox.askyesno(
            "Подтверждение сброса",
            "Вы уверены, что хотите сбросить весь прогресс?",
        )
        if confirm:
            self.score = 0
            self.click_power = 1
            self.passive_income = 0
            self.total_clicks = 0
            self.upgrade_power_cost = 15
            self.upgrade_auto_cost = 30
            self.upgrade_mega_cost = 120
            self._update_ui_state()

    def _on_close(self) -> None:
        """Корректно завершает работу приложения."""
        self._is_running = False
        self.root.destroy()


def main() -> None:
    """Точка входа в игру-кликер."""
    root = tk.Tk()
    ClickerGameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
