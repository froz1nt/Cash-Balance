import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
from datetime import datetime

if sys.platform == "win32":
    APP_DIR = os.path.join(
        os.getenv("APPDATA") or os.path.expanduser("~"),
        "CashBalance"
    )

elif sys.platform == "darwin":
    APP_DIR = os.path.join(
        os.path.expanduser("~"),
        "Library",
        "Application Support",
        "CashBalance"
    )

else:
    APP_DIR = os.path.join(
        os.path.expanduser("~"),
        ".local",
        "share",
        "CashBalance"
    )

os.makedirs(APP_DIR, exist_ok=True)

SAVE_FILE = os.path.join(
    APP_DIR,
    "cash_balance_save.json"
)

# =========================================================
# COLORS
# =========================================================

BG = "#05070a"
CARD = "#0b1017"
CARD_2 = "#0f1620"
CARD_3 = "#121b26"

BLUE = "#1683ff"
BLUE_DARK = "#0d5fc4"
BLUE_HOVER = "#3195ff"

WHITE = "#ffffff"
TEXT = "#dce5ef"
MUTED = "#718096"

GREEN = "#27d17f"
GREEN_DARK = "#1aaa66"

RED = "#ff4d5f"
RED_DARK = "#d93647"

BORDER = "#182330"
BORDER_LIGHT = "#233242"


class CashBalance:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self, root):
        self.root = root

        self.root.title("Cash Balance")
        self.root.geometry("1150x750")
        self.root.minsize(950, 650)
        self.root.configure(bg=BG)

        self.operations = []
        self.goal = None

        self.current_page = None
        self.page_frame = None

        self.operation_type = "Доход"

        self.load_data()

        self.main = tk.Frame(
            self.root,
            bg=BG
        )

        self.main.pack(
            fill="both",
            expand=True
        )

        self.show_history()

        self.root.after(
            2000,
            self.auto_save
        )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

    # =====================================================
    # SAVE / LOAD
    # =====================================================

    def load_data(self):

        if not os.path.exists(SAVE_FILE):
            self.operations = []
            self.goal = None
            return

        try:

            with open(
                SAVE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError

            self.operations = data.get(
                "operations",
                []
            )

            self.goal = data.get(
                "goal",
                None
            )

            if not isinstance(
                self.operations,
                list
            ):
                self.operations = []

        except Exception:
            self.operations = []
            self.goal = None

    def save_data(self):

        try:

            data = {
                "operations": self.operations,
                "goal": self.goal
            }

            with open(
                SAVE_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception as error:
            print(
                "Ошибка сохранения:",
                error
            )

    def auto_save(self):

        self.save_data()

        self.root.after(
            2000,
            self.auto_save
        )

    # =====================================================
    # CALCULATIONS
    # =====================================================

    def get_balance(self):

        balance = 0

        for operation in self.operations:

            try:

                price = float(
                    operation.get(
                        "price",
                        0
                    )
                )

                quantity = int(
                    operation.get(
                        "quantity",
                        1
                    )
                )

            except (
                ValueError,
                TypeError
            ):
                continue

            total = price * quantity

            if operation.get("type") == "Доход":
                balance += total
            else:
                balance -= total

        return balance

    def get_to_goal(self):

        if self.goal is None:
            return None

        balance = self.get_balance()

        return max(
            self.goal - balance,
            0
        )

    # =====================================================
    # UI HELPERS
    # =====================================================

    def clear_page(self):

        for widget in self.main.winfo_children():
            widget.destroy()

        self.page_frame = None

    def create_cube(
        self,
        parent,
        size=24
    ):

        canvas = tk.Canvas(
            parent,
            width=size,
            height=size,
            bg=CARD_2,
            highlightthickness=0
        )

        s = size

        p1 = (
            s * 0.50,
            2
        )

        p2 = (
            s - 3,
            s * 0.27
        )

        p3 = (
            s * 0.50,
            s * 0.52
        )

        p4 = (
            3,
            s * 0.27
        )

        p5 = (
            s * 0.50,
            s - 2
        )

        p6 = (
            s - 3,
            s * 0.73
        )

        p7 = (
            3,
            s * 0.73
        )

        canvas.create_polygon(
            p1,
            p2,
            p3,
            p4,
            fill="#020304",
            outline="#10151b"
        )

        canvas.create_polygon(
            p4,
            p3,
            p5,
            p7,
            fill="#050607",
            outline="#10151b"
        )

        canvas.create_polygon(
            p3,
            p2,
            p6,
            p5,
            fill="#080a0c",
            outline="#10151b"
        )

        canvas.create_line(
            p1[0],
            p1[1],
            p3[0],
            p3[1],
            fill=BLUE,
            width=1
        )

        return canvas

    # =====================================================
    # BUTTON HOVER
    # =====================================================

    def add_button_hover(
        self,
        button,
        normal,
        hover
    ):

        button.bind(
            "<Enter>",
            lambda event:
            button.configure(
                bg=hover
            )
        )

        button.bind(
            "<Leave>",
            lambda event:
            button.configure(
                bg=normal
            )
        )

    # =====================================================
    # PAGE ANIMATION
    # =====================================================

    def switch_page(
        self,
        page_function
    ):

        if self.page_frame is None:
            page_function()
            return

        old_frame = self.page_frame

        self.animate_page_out(
            old_frame,
            page_function,
            0
        )

    def animate_page_out(
        self,
        frame,
        callback,
        step
    ):

        if step >= 10:

            try:
                frame.destroy()
            except tk.TclError:
                pass

            self.page_frame = None

            callback()

            self.animate_page_in(
                self.page_frame,
                0
            )

            return

        try:

            frame.place_configure(
                relx=-0.08 * (step + 1)
            )

        except tk.TclError:
            callback()
            return

        self.root.after(
            15,
            lambda:
            self.animate_page_out(
                frame,
                callback,
                step + 1
            )
        )

    def animate_page_in(
        self,
        frame,
        step
    ):

        if frame is None:
            return

        if step >= 10:

            frame.place_configure(
                relx=0
            )

            return

        try:

            position = 0.08 * (
                1 - (step + 1) / 10
            )

            frame.place_configure(
                relx=position
            )

        except tk.TclError:
            return

        self.root.after(
            15,
            lambda:
            self.animate_page_in(
                frame,
                step + 1
            )
        )

    # =====================================================
    # FADE-LIKE CONTENT ANIMATION
    # =====================================================

    def animate_widgets(
        self,
        widgets,
        index=0
    ):

        if index >= len(widgets):
            return

        widget = widgets[index]

        try:

            widget.place_configure(
                relx=0.02
            )

            self.root.after(
                20,
                lambda:
                self.animate_widget_position(
                    widget,
                    0,
                    widgets,
                    index
                )
            )

        except tk.TclError:
            pass

    def animate_widget_position(
        self,
        widget,
        step,
        widgets,
        index
    ):

        if step >= 5:

            try:
                widget.place_configure(
                    relx=0
                )
            except tk.TclError:
                pass

            self.root.after(
                25,
                lambda:
                self.animate_widgets(
                    widgets,
                    index + 1
                )
            )

            return

        try:

            position = 0.02 * (
                1 - (step + 1) / 5
            )

            widget.place_configure(
                relx=position
            )

        except tk.TclError:
            return

        self.root.after(
            15,
            lambda:
            self.animate_widget_position(
                widget,
                step + 1,
                widgets,
                index
            )
        )

    # =====================================================
    # HISTORY PAGE
    # =====================================================

    def show_history(self):

        self.clear_page()

        self.current_page = "history"

        self.page_frame = tk.Frame(
            self.main,
            bg=BG
        )

        self.page_frame.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        # =================================================
        # HEADER
        # =================================================

        header = tk.Frame(
            self.page_frame,
            bg=BG
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(25, 15)
        )

        logo_frame = tk.Frame(
            header,
            bg=BG
        )

        logo_frame.pack(
            side="left"
        )

        # =================================================
        # GRADIENT LOGO — CASH BALANCE
        # =================================================

        logo_canvas = tk.Canvas(
            header,
            width=300,
            height=42,
            bg=BG,
            highlightthickness=0,
            bd=0
        )

        logo_canvas.pack(
            side="left"
        )

        def draw_gradient_text(
                canvas,
                text,
                x,
                y,
                font,
                start_color,
                end_color
        ):

            # Получаем ширину текста
            temp = canvas.create_text(
                x,
                y,
                text=text,
                font=font,
                anchor="w",
                fill=start_color
            )

            bbox = canvas.bbox(temp)

            canvas.delete(temp)

            if not bbox:
                return

            text_width = bbox[2] - bbox[0]

            # Создаём текст посимвольно,
            # чтобы каждый символ мог иметь свой оттенок
            current_x = x

            start_rgb = tuple(
                int(start_color[i:i + 2], 16)
                for i in (1, 3, 5)
            )

            end_rgb = tuple(
                int(end_color[i:i + 2], 16)
                for i in (1, 3, 5)
            )

            total_width = max(
                text_width,
                1
            )

            for char in text:

                temp_char = canvas.create_text(
                    0,
                    0,
                    text=char,
                    font=font
                )

                char_bbox = canvas.bbox(
                    temp_char
                )

                canvas.delete(
                    temp_char
                )

                if not char_bbox:
                    continue

                char_width = (
                        char_bbox[2]
                        - char_bbox[0]
                )

                position = (
                                   current_x - x
                           ) / total_width

                position = max(
                    0,
                    min(
                        1,
                        position
                    )
                )

                r = int(
                    start_rgb[0]
                    + (
                            end_rgb[0]
                            - start_rgb[0]
                    ) * position
                )

                g = int(
                    start_rgb[1]
                    + (
                            end_rgb[1]
                            - start_rgb[1]
                    ) * position
                )

                b = int(
                    start_rgb[2]
                    + (
                            end_rgb[2]
                            - start_rgb[2]
                    ) * position
                )

                color = (
                    f"#{r:02x}"
                    f"{g:02x}"
                    f"{b:02x}"
                )

                canvas.create_text(
                    current_x,
                    y,
                    text=char,
                    font=font,
                    anchor="w",
                    fill=color
                )

                current_x += char_width

        # CASH
        draw_gradient_text(
            logo_canvas,
            "CASH",
            0,
            21,
            (
             "Arial Rounded MT Bold",
             24,
             "bold"

            ),
            "#ffffff",
            "#8fd3ff"
        )

        # BALANCE
        draw_gradient_text(
            logo_canvas,
            " BALANCE",
            108,
            21,
                 (
            (
            "Arial Rounded MT Bold",
             24,
            "bold"
                )
            ),
            "#4da9ff",
            "#1677d2"
        )

        create_button = tk.Button(
            header,
            text="＋ СОЗДАТЬ ОПЕРАЦИЮ",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            fg=WHITE,
            bg=BLUE,
            activebackground=BLUE_DARK,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2",
            command=lambda:
            self.switch_page(
                self.show_create_page
            )
        )

        create_button.pack(
            side="right"
        )

        self.add_button_hover(
            create_button,
            BLUE,
            BLUE_HOVER
        )

        # =================================================
        # STATS
        # =================================================

        stats = tk.Frame(
            self.page_frame,
            bg=BG
        )

        stats.pack(
            fill="x",
            padx=35,
            pady=(5, 18)
        )

        balance = self.get_balance()

        to_goal = self.get_to_goal()

        self.create_stat(
            stats,
            "БАЛАНС",
            f"{balance:,.0f}$".replace(
                ",",
                " "
            ),
            BLUE
        )

        self.create_stat(
            stats,
            "ДО ЦЕЛИ",
            "—"
            if to_goal is None
            else f"{to_goal:,.0f}$".replace(
                ",",
                " "
            ),
            GREEN
        )

        self.create_stat(
            stats,
            "ЦЕЛЬ",
            "—"
            if self.goal is None
            else f"{self.goal:,.0f}$".replace(
                ",",
                " "
            ),
            WHITE
        )

        # =================================================
        # HISTORY CARD
        # =================================================

        history_card = tk.Frame(
            self.page_frame,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        history_card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 30)
        )

        # =================================================
        # TITLE
        # =================================================

        title_frame = tk.Frame(
            history_card,
            bg=CARD
        )

        title_frame.pack(
            fill="x",
            padx=20,
            pady=(18, 10)
        )

        tk.Label(
            title_frame,
            text="История транзакций",
            font=(
                "Segoe UI",
                16,
                "bold"
            ),
            fg=WHITE,
            bg=CARD
        ).pack(
            side="left"
        )

        tk.Label(
            title_frame,
            text=f"{len(self.operations)} операций",
            font=(
                "Segoe UI",
                9
            ),
            fg=MUTED,
            bg=CARD
        ).pack(
            side="right"
        )

        # =================================================
        # COLUMN HEADERS
        # =================================================

        columns = tk.Frame(
            history_card,
            bg=CARD_2
        )

        columns.pack(
            fill="x",
            padx=15
        )

        headers = [
            "",
            "ТИП",
            "ЦЕНА",
            "КОЛ-ВО",
            "СУММА",
            "КОММЕНТАРИЙ",
            "ДАТА",
            ""
        ]

        widths = [
            4,
            14,
            14,
            12,
            14,
            28,
            20,
            7
        ]

        for index, text in enumerate(headers):

            tk.Label(
                columns,
                text=text,
                font=(
                    "Segoe UI",
                    8,
                    "bold"
                ),
                fg=MUTED,
                bg=CARD_2,
                anchor="w"
            ).grid(
                row=0,
                column=index,
                sticky="ew",
                padx=8,
                pady=8
            )

        for i, width in enumerate(widths):

            columns.grid_columnconfigure(
                i,
                weight=width
            )

        # =================================================
        # SCROLL
        # =================================================

        container = tk.Frame(
            history_card,
            bg=CARD
        )

        container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        canvas = tk.Canvas(
            container,
            bg=CARD,
            highlightthickness=0
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        list_frame = tk.Frame(
            canvas,
            bg=CARD
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=list_frame,
            anchor="nw"
        )

        def update_scroll(event=None):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

            canvas.itemconfig(
                canvas_window,
                width=canvas.winfo_width()
            )

        list_frame.bind(
            "<Configure>",
            update_scroll
        )

        canvas.bind(
            "<Configure>",
            update_scroll
        )

        def mousewheel(event):

            canvas.yview_scroll(
                int(
                    -1 *
                    (event.delta / 120)
                ),
                "units"
            )

        canvas.bind(
            "<MouseWheel>",
            mousewheel
        )

        # =================================================
        # EMPTY
        # =================================================

        if not self.operations:

            empty = tk.Frame(
                list_frame,
                bg=CARD
            )

            empty.pack(
                fill="x",
                pady=80
            )

            tk.Label(
                empty,
                text="История операций пуста",
                font=(
                    "Segoe UI",
                    14,
                    "bold"
                ),
                fg=WHITE,
                bg=CARD
            ).pack()

            tk.Label(
                empty,
                text="Создайте первую операцию",
                font=(
                    "Segoe UI",
                    10
                ),
                fg=MUTED,
                bg=CARD
            ).pack(
                pady=(7, 0)
            )

        else:

            for operation in reversed(
                self.operations
            ):

                self.create_operation_row(
                    list_frame,
                    operation
                )

        self.root.after(
            50,
            update_scroll
        )

    # =====================================================
    # STAT CARD
    # =====================================================

    def create_stat(
        self,
        parent,
        title,
        value,
        accent
    ):

        card = tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=6
        )

        tk.Label(
            card,
            text=title,
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            fg=MUTED,
            bg=CARD
        ).pack(
            anchor="w",
            padx=18,
            pady=(14, 2)
        )

        tk.Label(
            card,
            text=value,
            font=(
                "Segoe UI",
                20,
                "bold"
            ),
            fg=accent,
            bg=CARD
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 14)
        )

    # =====================================================
    # OPERATION ROW
    # =====================================================

    def create_operation_row(
        self,
        parent,
        operation
    ):

        row = tk.Frame(
            parent,
            bg=CARD_2,
            highlightbackground=BORDER,
            highlightthickness=1,
            height=58
        )

        row.pack(
            fill="x",
            pady=4
        )

        row.pack_propagate(False)

        for column, weight in enumerate(
            [
                4,
                14,
                14,
                12,
                14,
                28,
                20,
                7
            ]
        ):

            row.grid_columnconfigure(
                column,
                weight=weight
            )

        # =================================================
        # CUBE
        # =================================================

        cube_frame = tk.Frame(
            row,
            bg=CARD_2
        )

        cube_frame.grid(
            row=0,
            column=0,
            sticky="w",
            padx=8
        )

        cube = self.create_cube(
            cube_frame,
            22
        )

        cube.pack()

        # =================================================
        # TYPE
        # =================================================

        type_color = (
            GREEN
            if operation.get("type")
            == "Доход"
            else RED
        )

        tk.Label(
            row,
            text=operation.get(
                "type",
                "—"
            ),
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=type_color,
            bg=CARD_2,
            anchor="w"
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=8
        )

        # =================================================
        # PRICE
        # =================================================

        try:

            price = float(
                operation.get(
                    "price",
                    0
                )
            )

        except (
            ValueError,
            TypeError
        ):

            price = 0

        tk.Label(
            row,
            text=f"{price:,.0f}$".replace(
                ",",
                " "
            ),
            font=(
                "Segoe UI",
                9
            ),
            fg=TEXT,
            bg=CARD_2,
            anchor="w"
        ).grid(
            row=0,
            column=2,
            sticky="ew",
            padx=8
        )

        # =================================================
        # QUANTITY
        # =================================================

        try:

            quantity = int(
                operation.get(
                    "quantity",
                    1
                )
            )

        except (
            ValueError,
            TypeError
        ):

            quantity = 1

        tk.Label(
            row,
            text=str(quantity),
            font=(
                "Segoe UI",
                9
            ),
            fg=TEXT,
            bg=CARD_2,
            anchor="w"
        ).grid(
            row=0,
            column=3,
            sticky="ew",
            padx=8
        )

        # =================================================
        # TOTAL
        # =================================================

        total = price * quantity

        tk.Label(
            row,
            text=f"{total:,.0f}$".replace(
                ",",
                " "
            ),
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=WHITE,
            bg=CARD_2,
            anchor="w"
        ).grid(
            row=0,
            column=4,
            sticky="ew",
            padx=8
        )

        # =================================================
        # COMMENT
        # =================================================

        comment = operation.get(
            "comment",
            ""
        )

        tk.Label(
            row,
            text=comment
            if comment
            else "—",
            font=(
                "Segoe UI",
                9
            ),
            fg=TEXT
            if comment
            else MUTED,
            bg=CARD_2,
            anchor="w"
        ).grid(
            row=0,
            column=5,
            sticky="ew",
            padx=8
        )

        # =================================================
        # DATE
        # =================================================

        tk.Label(
            row,
            text=operation.get(
                "date",
                ""
            ),
            font=(
                "Segoe UI",
                8
            ),
            fg=MUTED,
            bg=CARD_2,
            anchor="w"
        ).grid(
            row=0,
            column=6,
            sticky="ew",
            padx=8
        )

        # =================================================
        # DELETE
        # =================================================

        delete_button = tk.Button(
            row,
            text="✕",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=RED,
            bg=CARD_2,
            activebackground=CARD_2,
            activeforeground=RED,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda op=operation:
            self.delete_transaction(op)
        )

        delete_button.grid(
            row=0,
            column=7,
            padx=6
        )

        # Hover удаления
        delete_button.bind(
            "<Enter>",
            lambda event:
            delete_button.configure(
                fg="#ff7b87"
            )
        )

        delete_button.bind(
            "<Leave>",
            lambda event:
            delete_button.configure(
                fg=RED
            )
        )

    # =====================================================
    # CREATE PAGE
    # =====================================================

    def show_create_page(self):

        self.clear_page()

        self.current_page = "create"

        self.page_frame = tk.Frame(
            self.main,
            bg=BG
        )

        self.page_frame.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        # =================================================
        # TOP
        # =================================================

        top = tk.Frame(
            self.page_frame,
            bg=BG
        )

        top.pack(
            fill="x",
            padx=35,
            pady=(25, 15)
        )

        back_button = tk.Button(
            top,
            text="← НАЗАД",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=MUTED,
            bg=BG,
            activebackground=BG,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda:
            self.switch_page(
                self.show_history
            )
        )

        back_button.pack(
            side="left"
        )

        back_button.bind(
            "<Enter>",
            lambda event:
            back_button.configure(
                fg=WHITE
            )
        )

        back_button.bind(
            "<Leave>",
            lambda event:
            back_button.configure(
                fg=MUTED
            )
        )

        tk.Label(
            top,
            text="Создать операцию",
            font=(
                "Segoe UI",
                21,
                "bold"
            ),
            fg=WHITE,
            bg=BG
        ).pack(
            side="left",
            padx=25
        )

        # =================================================
        # MAIN CARD
        # =================================================

        card = tk.Frame(
            self.page_frame,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 30)
        )

        # =================================================
        # TYPE TABS
        # =================================================

        tabs = tk.Frame(
            card,
            bg=CARD
        )

        tabs.pack(
            fill="x",
            padx=30,
            pady=(30, 20)
        )

        income_button = tk.Button(
            tabs,
            text="ДОХОД",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        expense_button = tk.Button(
            tabs,
            text="РАСХОД",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        income_button.configure(
            command=lambda:
            self.select_type(
                "Доход",
                income_button,
                expense_button
            )
        )

        expense_button.configure(
            command=lambda:
            self.select_type(
                "Расход",
                income_button,
                expense_button
            )
        )

        income_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5),
            ipady=13
        )

        expense_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 0),
            ipady=13
        )

        self.select_type(
            self.operation_type,
            income_button,
            expense_button
        )

        # =================================================
        # INPUTS
        # =================================================

        inputs = tk.Frame(
            card,
            bg=CARD
        )

        inputs.pack(
            fill="x",
            padx=30
        )

        # =================================================
        # PRICE
        # =================================================

        price_container = tk.Frame(
            inputs,
            bg=CARD
        )

        price_container.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8)
        )

        tk.Label(
            price_container,
            text="Цена",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=TEXT,
            bg=CARD
        ).pack(
            anchor="w",
            pady=(0, 7)
        )

        price_entry = self.create_input(
            price_container
        )

        price_entry.pack(
            fill="x",
            ipady=11
        )

        # =================================================
        # QUANTITY
        # =================================================

        quantity_container = tk.Frame(
            inputs,
            bg=CARD
        )

        quantity_container.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(8, 0)
        )

        tk.Label(
            quantity_container,
            text="Количество",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=TEXT,
            bg=CARD
        ).pack(
            anchor="w",
            pady=(0, 7)
        )

        quantity_entry = self.create_input(
            quantity_container
        )

        quantity_entry.pack(
            fill="x",
            ipady=11
        )

        # =================================================
        # QUANTITY
        # =================================================

        quantity_container = tk.Frame(
            inputs,
            bg=CARD
        )

        tk.Label(
            quantity_container,
            text="Количество",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=TEXT,
            bg=CARD
        ).pack(
            anchor="w",
            pady=(0, 7)
        )

        quantity_entry = self.create_input(
            quantity_container
        )

        quantity_entry.pack(
            fill="x",
            expand=True,
            ipady=11
        )

        # =================================================
        # COMMENT
        # =================================================

        tk.Label(
            card,
            text="Комментарий",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=TEXT,
            bg=CARD
        ).pack(
            anchor="w",
            padx=30,
            pady=(20, 7)
        )

        validate_comment = self.root.register(
            lambda text: len(text) <= 35
        )

        comment_entry = tk.Entry(
            card,
            font=(
                "Segoe UI",
                10
            ),
            validate="key",
            validatecommand=(validate_comment, "%P"),
            fg=TEXT,
            bg=CARD_2,
            insertbackground=WHITE,
            relief="flat",
            bd=0
        )

        comment_entry.pack(
            fill="x",
            padx=30,
            ipady=11
        )

        # =================================================
        # GOAL
        # =================================================

        goal_box = tk.Frame(
            card,
            bg=CARD_2,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        goal_box.pack(
            fill="x",
            padx=30,
            pady=25
        )

        goal_text = tk.Frame(
            goal_box,
            bg=CARD_2
        )

        goal_text.pack(
            side="left",
            padx=15,
            pady=12
        )

        tk.Label(
            goal_text,
            text="Цель",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            fg=WHITE,
            bg=CARD_2
        ).pack(
            anchor="w"
        )

        tk.Label(
            goal_text,
            text="Укажите сумму, которую хотите накопить",
            font=(
                "Segoe UI",
                8
            ),
            fg=MUTED,
            bg=CARD_2
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        # =================================================
        # GOAL INPUT
        # =================================================

        goal_entry = tk.Entry(
            goal_box,
            font=(
                "Segoe UI",
                10
            ),
            fg=TEXT,
            bg="#080d13",
            insertbackground=WHITE,
            relief="flat",
            bd=0
        )

        goal_entry.pack(
            side="right",
            padx=(5, 10),
            pady=12,
            ipady=8
        )

        if self.goal is not None:

            goal_entry.insert(
                0,
                str(self.goal)
            )

        save_goal_button = tk.Button(
            goal_box,
            text="Сохранить",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            fg=WHITE,
            bg=BLUE_DARK,
            activebackground=BLUE,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda:
            self.save_goal(
                goal_entry
            )
        )

        save_goal_button.pack(
            side="right",
            padx=5,
            pady=12,
            ipadx=8,
            ipady=5
        )

        self.add_button_hover(
            save_goal_button,
            BLUE_DARK,
            BLUE
        )

        # =================================================
        # CREATE
        # =================================================

        create_button = tk.Button(
            card,
            text="СОЗДАТЬ ОПЕРАЦИЮ",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            fg=WHITE,
            bg=BLUE,
            activebackground=BLUE_DARK,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda:
            self.add_operation(
                price_entry,
                quantity_entry,
                comment_entry,
                create_button
            )
        )

        create_button.pack(
            side="bottom",
            fill="x",
            padx=30,
            pady=25,
            ipady=12
        )

        self.add_button_hover(
            create_button,
            BLUE,
            BLUE_HOVER
        )

        # =================================================
        # INPUT FOCUS ANIMATION
        # =================================================

        self.add_entry_focus(
            price_entry
        )

        self.add_entry_focus(
            quantity_entry
        )

        self.add_entry_focus(
            comment_entry
        )

        self.add_entry_focus(
            goal_entry
        )

        price_entry.focus_set()

    # =====================================================
    # INPUT
    # =====================================================

    def create_input(
        self,
        parent
    ):

        # Одинаковые настройки для обоих полей.
        # За счёт одинакового контейнера/grid они
        # имеют одинаковую ширину и высоту.

        entry = tk.Entry(
            parent,
            font=(
                "Segoe UI",
                10
            ),
            fg=TEXT,
            bg=CARD_2,
            insertbackground=WHITE,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=BLUE
        )

        return entry

    def add_entry_focus(
        self,
        entry
    ):

        def focus_in(event):

            entry.configure(
                highlightbackground=BLUE,
                bg="#121d29"
            )

        def focus_out(event):

            entry.configure(
                highlightbackground=BORDER,
                bg=CARD_2
            )

        entry.bind(
            "<FocusIn>",
            focus_in
        )

        entry.bind(
            "<FocusOut>",
            focus_out
        )

    # =====================================================
    # TYPE
    # =====================================================

    def select_type(
        self,
        operation_type,
        income_button,
        expense_button
    ):

        self.operation_type = operation_type

        if operation_type == "Доход":

            income_button.configure(
                bg=GREEN,
                fg="#06120c",
                activebackground=GREEN,
                activeforeground="#06120c"
            )

            expense_button.configure(
                bg=CARD_2,
                fg=MUTED,
                activebackground=CARD_2,
                activeforeground=WHITE
            )

            self.add_button_hover(
                income_button,
                GREEN,
                "#38df8d"
            )

            self.add_button_hover(
                expense_button,
                CARD_2,
                CARD_3
            )

        else:

            income_button.configure(
                bg=CARD_2,
                fg=MUTED,
                activebackground=CARD_2,
                activeforeground=WHITE
            )

            expense_button.configure(
                bg=RED,
                fg=WHITE,
                activebackground=RED,
                activeforeground=WHITE
            )

            self.add_button_hover(
                income_button,
                CARD_2,
                CARD_3
            )

            self.add_button_hover(
                expense_button,
                RED,
                "#ff6473"
            )

    # =====================================================
    # ADD OPERATION
    # =====================================================

    def add_operation(
        self,
        price_entry,
        quantity_entry,
        comment_entry,
        create_button
    ):

        price_text = (
            price_entry
            .get()
            .strip()
        )

        quantity_text = (
            quantity_entry
            .get()
            .strip()
        )

        comment = (
            comment_entry
            .get()
            .strip()
        )

        # =================================================
        # PRICE
        # =================================================

        if not price_text:

            self.show_input_error(
                price_entry,
                "Укажите цену операции."
            )

            self.shake_widget(
                price_entry
            )

            return

        # =================================================
        # QUANTITY
        # =================================================

        if not quantity_text:
            quantity_text = "1"

        # =================================================
        # CONVERT
        # =================================================

        try:

            price = float(
                price_text
                .replace(",", ".")
                .replace(" ", "")
            )

            quantity = int(
                quantity_text
            )

        except ValueError:

            messagebox.showerror(
                "Ошибка",
                "Цена должна быть числом, "
                "а количество — целым числом."
            )

            self.shake_widget(
                price_entry
            )

            self.shake_widget(
                quantity_entry
            )

            return

        # =================================================
        # VALIDATION
        # =================================================

        if price <= 0:

            self.show_input_error(
                price_entry,
                "Цена должна быть больше 0."
            )

            self.shake_widget(
                price_entry
            )

            return

        if quantity <= 0:

            self.show_input_error(
                quantity_entry,
                "Количество должно быть больше 0."
            )

            self.shake_widget(
                quantity_entry
            )

            return

        # =================================================
        # OPERATION
        # =================================================

        operation_id = datetime.now().timestamp()

        operation = {
            "id": operation_id,
            "type": self.operation_type,
            "price": price,
            "quantity": quantity,
            "comment": comment,
            "date": datetime.now().strftime(
                "%d.%m.%Y %H:%M"
            )
        }

        self.operations.append(
            operation
        )

        self.save_data()

        # =================================================
        # SUCCESS ANIMATION
        # =================================================

        create_button.configure(
            text="✓ СОЗДАНО!",
            bg=GREEN,
            fg="#06120c",
            activebackground=GREEN
        )

        # Маленькая анимация перед переходом.

        self.root.after(
            100,
            lambda:
            self.success_pulse(
                create_button,
                0
            )
        )

        self.root.after(
            450,
            self.show_history
        )

    # =====================================================
    # SUCCESS PULSE
    # =====================================================

    def success_pulse(
        self,
        button,
        step
    ):

        if step >= 6:
            return

        if step % 2 == 0:

            button.configure(
                bg=GREEN
            )

        else:

            button.configure(
                bg=GREEN_DARK
            )

        self.root.after(
            45,
            lambda:
            self.success_pulse(
                button,
                step + 1
            )
        )

    # =====================================================
    # ERROR
    # =====================================================

    def show_input_error(
        self,
        entry,
        text
    ):

        entry.configure(
            highlightbackground=RED,
            highlightcolor=RED
        )

        messagebox.showerror(
            "Ошибка",
            text
        )

        self.root.after(
            500,
            lambda:
            entry.configure(
                highlightbackground=BORDER,
                highlightcolor=BLUE
            )
        )

    # =====================================================
    # SHAKE
    # =====================================================

        def shake_widget(
                self,
                widget
        ):
            try:
                widget.configure(
                    highlightbackground=RED,
                    highlightcolor=RED
                )

                self.root.after(
                    500,
                    lambda:
                    widget.configure(
                        highlightbackground=BORDER,
                        highlightcolor=BLUE
                    )
                )

            except tk.TclError:
                pass

        def show_input_error(self, widget, message):
            original_x = widget.winfo_x()

        positions = [
            0,
            -5,
            5,
            -4,
            4,
            -2,
            2,
            0
        ]

        def animate(index, widget, original_x):  # ✅ добавляем параметры
            if index >= len(positions):
                try:
                    widget.place_configure(
                        x=original_x
                    )
                except tk.TclError:
                    pass
                return

            try:
                widget.place_configure(
                    x=original_x + positions[index]
                )

            except tk.TclError:

                # Entry может находиться внутри pack/grid.
                # Поэтому используем небольшую анимацию
                # highlight вместо изменения geometry.

                if index % 2 == 0:

                    widget.configure(
                        highlightbackground=RED
                    )

                else:

                    widget.configure(
                        highlightbackground=BLUE
                    )

            self.root.after(
                30,
                lambda:
                animate(index + 1)
            )

        animate(0)

    # =====================================================
    # DELETE
    # =====================================================

    def delete_transaction(
        self,
        operation
    ):

        operation_id = operation.get(
            "id"
        )

        answer = messagebox.askyesno(
            "Удалить операцию",
            "Вы действительно хотите "
            "удалить эту операцию?"
        )

        if not answer:
            return

        self.operations = [
            item
            for item in self.operations
            if item.get("id")
            != operation_id
        ]

        self.save_data()

        self.show_history()

    # =====================================================
    # SAVE GOAL
    # =====================================================

    def save_goal(
        self,
        goal_entry
    ):

        value = (
            goal_entry
            .get()
            .strip()
        )

        if not value:

            self.goal = None

            self.save_data()

            messagebox.showinfo(
                "Цель",
                "Цель удалена."
            )

            return

        try:

            goal = float(
                value
                .replace(",", ".")
                .replace(" ", "")
            )

        except ValueError:

            messagebox.showerror(
                "Ошибка",
                "Цель должна быть числом."
            )

            return

        if goal <= 0:

            messagebox.showerror(
                "Ошибка",
                "Цель должна быть больше 0."
            )

            return

        self.goal = goal

        self.save_data()

        messagebox.showinfo(
            "Цель",
            "Цель установлена: "
            f"{goal:,.0f}$".replace(
                ",",
                " "
            )
        )

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        self.save_data()

        self.root.destroy()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "Cash Balance"
    )

    if getattr(
        sys,
        "frozen",
        False
    ):

        base_path = sys._MEIPASS

    else:

        base_path = os.path.dirname(
            os.path.abspath(
                __file__
            )
        )

    icon_path = os.path.join(
        base_path,
        "icon.ico"
    )

    try:

        root.iconbitmap(
            default=icon_path
        )

    except tk.TclError:
        pass

    app = CashBalance(
        root
    )

    root.mainloop()