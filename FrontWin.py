import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ---- Настройки окна ----
        self.title("Анализ банкетов — выбор файлов")
        self.geometry("700x520")
        self.minsize(600, 480)

        ctk.set_appearance_mode("system")   # "light" / "dark" / "system"
        ctk.set_default_color_theme("blue")

        # Хранилище выбранных путей
        self.selected_files: list[str] = []

        # ---- Заголовок ----
        self.label_title = ctk.CTkLabel(
            self, text="Выберите файлы .xlsx для анализа",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.label_title.pack(pady=(20, 10))

        # ---- Кнопка выбора файлов ----
        self.btn_select = ctk.CTkButton(
            self, text="Выбрать файлы…", command=self.select_files,
            width=200, height=36
        )
        self.btn_select.pack(pady=10)

        # ---- Статус подтверждения ----
        self.label_status = ctk.CTkLabel(
            self, text="Файлы пока не выбраны",
            text_color="gray", font=ctk.CTkFont(size=13)
        )
        self.label_status.pack(pady=(0, 10))

        # ---- Прокручиваемый список выбранных файлов ----
        self.scroll_frame = ctk.CTkScrollableFrame(
            self, label_text="Выбранные файлы", width=620, height=250
        )
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # ---- Кнопка "Обработать" (заглушка) ----
        self.btn_process = ctk.CTkButton(
            self, text="Обработать", command=self.process_files,
            width=200, height=36, state="disabled"
        )
        self.btn_process.pack(pady=(0, 20))

    # ------------------------------------------------------------------
    def select_files(self):
        """Открывает диалог выбора файлов и сохраняет результат."""
        files = filedialog.askopenfilenames(
            title="Выберите файлы банкетов",
            filetypes=[("Excel файлы", "*.xlsx *.xls"), ("Все файлы", "*.*")]
        )

        if not files:
            # Пользователь закрыл диалог или отменил выбор
            if not self.selected_files:
                self._set_status("Выбор файлов отменён.", ok=False)
            return

        # Оставляем только .xlsx / .xls на случай, если пользователь
        # вручную ввёл что-то другое в поле "Имя файла"
        valid = [f for f in files if Path(f).suffix.lower() in (".xlsx", ".xls")]

        if not valid:
            self._set_status("В выбранных файлах нет .xlsx / .xls", ok=False)
            return

        self.selected_files = valid
        self._render_file_list()
        self._set_status(
            f"Успешно выбрано файлов: {len(self.selected_files)}", ok=True
        )
        self.btn_process.configure(state="normal")

    # ------------------------------------------------------------------
    def _render_file_list(self):
        """Перерисовывает список выбранных файлов."""
        # Очищаем старые строки
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for i, path in enumerate(self.selected_files, start=1):
            row = ctk.CTkLabel(
                self.scroll_frame,
                text=f"{i}. {Path(path).name}",
                anchor="w",
                justify="left",
            )
            row.pack(fill="x", padx=8, pady=2)

    # ------------------------------------------------------------------
    def _set_status(self, text: str, ok: bool = True):
        """Обновляет строку статуса (зелёный/красный)."""
        self.label_status.configure(
            text=text,
            text_color="#2ecc71" if ok else "#e74c3c"
        )

    # ------------------------------------------------------------------
    def process_files(self):
        """Здесь будет вызов вашей логики (pandas / analyzer)."""
        # Пример:
        # from analyzer import load_and_analyze
        # result = load_and_analyze(self.selected_files)
        # ...

        # Пока просто подтверждение:
        self._set_status(
            f"Готово к обработке: {len(self.selected_files)} файл(ов). "
            f"Подключите свою логику в process_files().",
            ok=True,
        )
        print("Выбранные файлы:")
        for f in self.selected_files:
            print(" -", f)


if __name__ == "__main__":
    App().mainloop()