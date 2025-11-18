import sys
import csv
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
    QMessageBox, QGridLayout, QScrollArea, QHeaderView
)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt

csv_file = "workout_log.csv"
headers = ["Timestamp", "Exercise", "Reps", "Sets", "Weight"]

def ensure_csv_headers(csv_path, headers): 
    """
    Ensures the workout CSV file exists and has correct headers.

    If the file does not exist, it creates it.
    If headers are missing or out of order, it rewrites them.
    This function guarantees data consistency throughout the app.
    """
    try:
        with open(csv_path, "r", newline="") as f: 
            first_line = f.readline().strip().split(",") 
            if first_line != headers: 
                f.seek(0)
                existing = list(csv.DictReader(f))
                with open(csv_path, "w", newline="") as fw:
                    writer = csv.DictWriter(fw, fieldnames=headers)
                    writer.writeheader()
                    for row in existing:
                        writer.writerow({h: row.get(h, "") for h in headers})
    except FileNotFoundError:
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()


class AddWorkoutWindow(QWidget):
    """
    A secondary window that allows users to add a new workout session.
    Users can dynamically add or remove exercise entry rows before saving.
    Each saved session is timestamped automatically.
    """
    def __init__(self, refresh_callback):
        """
        Initializes the AddWorkoutWindow.

        Parameters:
            refresh_callback: A function passed from MainWindow to refresh
                              the main table after saving new data.
        """
        super().__init__()
        self.refresh_callback = refresh_callback

        self.setWindowTitle("Add Workout Session")
        self.setGeometry(250, 250, 925, 520)
        self.setMinimumWidth(600)

        # === MAIN CONTAINER LAYOUT ===
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Title
        title = QLabel("Add Workout Session")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #333;")
        main_layout.addWidget(title)

        subtitle = QLabel("Enter your exercises below (Exercise, Reps, Sets, Weight)")
        subtitle.setStyleSheet("font-size: 14px; color: #666; margin-bottom: 10px;")
        main_layout.addWidget(subtitle)

        # === CARD-LIKE CONTAINER ===
        card = QWidget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(10)
        card.setStyleSheet("""
            background: white;
            border-radius: 10px;
            border: 1px solid #ddd;
        """)

        # === SCROLL AREA ===
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)
        scroll_layout.setSpacing(12)

        # Header row
        header_style = "font-weight: bold; color: #444; padding-bottom: 5px;"
        scroll_layout.addWidget(self._header_label("Exercise"), 0, 0)
        scroll_layout.addWidget(self._header_label("Reps"),     0, 1)
        scroll_layout.addWidget(self._header_label("Sets"),     0, 2)
        scroll_layout.addWidget(self._header_label("Weight (lbs)"), 0, 3)

        self.grid = scroll_layout
        scroll_area.setWidget(scroll_widget)

        card_layout.addWidget(scroll_area)
        main_layout.addWidget(card)

        # === BUTTON ROW ===
        btn_row = QHBoxLayout()
        btn_row.setSpacing(15)

        add_row_btn = QPushButton("Add Exercise")
        remove_row_btn = QPushButton("Remove Last")
        save_btn = QPushButton("Save Workout")

        add_row_btn.clicked.connect(self.add_row)
        remove_row_btn.clicked.connect(self.remove_last_row)
        save_btn.clicked.connect(self.save_workout)

        btn_row.addWidget(add_row_btn)
        btn_row.addWidget(remove_row_btn)
        btn_row.addStretch()
        btn_row.addWidget(save_btn)

        main_layout.addLayout(btn_row)
        self.setLayout(main_layout)

        # DATA STRUCTURES
        self.inputs = []
        self.row_count = 0

        self.add_row()

        # === GLOBAL STYLING ===
        self.setStyleSheet("""
        QWidget {
            background-color: #f3f4f7;
            font-family: Segoe UI;
        }

        QLineEdit {
            padding: 10px;
            font-size: 14px;
            border: 2px solid #c8ccd3;
            border-radius: 8px;
            background: #ffffff;
            min-width: 180px;   /* WIDER INPUT */
        }

        QLineEdit:focus {
            border: 2px solid #0078d7;
            background: #fff;
        }

        /* LABELS */
        QLabel {
            font-size: 14px;
            color: #444;
        }

        /* BUTTONS */
        QPushButton {
            background-color: #0078d7;
            color: white;
            font-weight: bold;
            padding: 10px 18px;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #005fa3;
        }

        /* CARD BACKGROUND */
        #FormCard {
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid #dcdcdc;
            padding: 20px;
        }
    """)

    def _header_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
        return lbl


    def add_row(self):
        """Adds a new set of QLineEdits (one exercise entry)."""
        self.row_count += 1
        exercise = QLineEdit()
        reps = QLineEdit()
        sets = QLineEdit()
        weight = QLineEdit()

        exercise.setPlaceholderText(f"Exercise {self.row_count}")
        reps.setPlaceholderText("Reps")
        sets.setPlaceholderText("Sets")
        weight.setPlaceholderText("Weight")

        self.grid.addWidget(exercise, self.row_count, 0)
        self.grid.addWidget(reps, self.row_count, 1)
        self.grid.addWidget(sets, self.row_count, 2)
        self.grid.addWidget(weight, self.row_count, 3)

        self.inputs.append((exercise, reps, sets, weight))

    def remove_last_row(self):
        """Removes the most recently added row of exercise inputs."""
        if not self.inputs:
            QMessageBox.warning(self, "No Rows", "There are no rows to remove.")
            return

        # Remove widgets from grid
        exercise, reps, sets, weight = self.inputs.pop()
        for widget in (exercise, reps, sets, weight):
            self.grid.removeWidget(widget)
            widget.deleteLater()

        self.row_count -= 1
    def validate_row(self, ex, rp, st, wt, row_number):
        """Validates a single exercise row. Returns (True, cleaned_data) or (False, error_message)."""

        # Check for empty fields
        if not ex or not rp or not st or not wt:
            return False, f"Row {row_number}: All fields must be filled."

        # Numeric validation
        if not rp.isdigit():
            return False, f"Row {row_number}: Reps must be a whole number."
        if int(rp) <= 0:
            return False, f"Row {row_number}: Reps must be greater than zero."

        # Validate Sets
        if not st.isdigit():
            return False, f"Row {row_number}: Sets must be a whole number."
        if int(st) <= 0:
            return False, f"Row {row_number}: Sets must be greater than zero."

        # Validate Weight (can be 0 for bodyweight)
        if not wt.replace('.', '', 1).isdigit() and not self.is_float(wt):
            return False, f"Row {row_number}: Weight must be a number."

        weight_val = float(wt)
        if weight_val < 0:
            return False, f"Row {row_number}: Weight cannot be negative."

        return True, {
            "Exercise": ex,
            "Reps": int(rp),
            "Sets": int(st),
            "Weight": float(wt),
        }


    def is_float(self, value):
        """Checks if a string can be safely converted to float."""
        try:
            float(value)
            return True
        except ValueError:
            return False

    def save_workout(self):
        """
        Collects all valid exercise inputs and appends them to the CSV file.
        Each workout session is timestamped.
        """
        ensure_csv_headers(csv_file, headers)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        new_rows = []
        row_number = 1

        for exercise, reps, sets, weight in self.inputs:
            ex = exercise.text().strip()
            rp = reps.text().strip()
            st = sets.text().strip()
            wt = weight.text().strip()

            # Validate this row
            valid, result = self.validate_row(ex, rp, st, wt, row_number)

            if not valid:
                QMessageBox.warning(self, "Invalid Entry", result)
                return

            # Add timestamp AFTER validation
            result["Timestamp"] = timestamp
            new_rows.append(result)

            row_number += 1

        # Write them all at once
        with open(csv_file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writerows(new_rows)

        QMessageBox.information(self, "Workout Saved", f"Saved {len(new_rows)} exercise(s).")
        self.refresh_callback()
        self.close()


class MainWindow(QMainWindow):
    """
    The main application window that displays all recorded workouts.
    Includes options to add, remove, or visualize workouts.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TrainUp — Workout Log")
        self.resize(900, 600)
        self.setMinimumWidth(850)

        # === MAIN CONTAINER ===
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # === TITLE ===
        title = QLabel("Workout History")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #333;")
        main_layout.addWidget(title)

        # === TABLE CARD CONTAINER ===
        card = QWidget()
        card.setObjectName("TableCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(10)

        card.setStyleSheet("""
            QWidget#TableCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #cccccc;
            }
        """)

        # === TABLE ===
        self.table = QTableWidget()
        self.table.setMinimumHeight(400)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(34)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Table styling
        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                background: white;
                font-size: 14px;
            }
            QHeaderView::section {
                background: #eef0f3;
                font-weight: bold;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #d0d0d0;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:hover {
                background-color: #dfeffe;
            }
        """)

        card_layout.addWidget(self.table)
        main_layout.addWidget(card)

        # === BUTTON BAR ===
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        add_button = QPushButton("Add Workout")
        remove_button = QPushButton("Remove Selected")
        chart_button = QPushButton("Show Chart")

        add_button.clicked.connect(self.open_add_window)
        remove_button.clicked.connect(self.remove_selected)
        chart_button.clicked.connect(self.make_chart)

        # Button styling
        for btn in (add_button, remove_button, chart_button):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    padding: 10px 18px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #005fa3;
                }
                QPushButton:pressed {
                    background-color: #004276;
                }
            """)

        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addStretch()
        button_layout.addWidget(chart_button)

        main_layout.addLayout(button_layout)

        self.load_csv()


    def load_csv(self):
        """Reads workout data from CSV file and loads it into the table."""
        try:
            with open(csv_file, "r") as f:
                reader = csv.DictReader(f)
                data = list(reader)
        except FileNotFoundError:
            data = []

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(data):
            for col_idx, header in enumerate(headers):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(row_data.get(header, "")))

        self.table.resizeColumnsToContents()
    
    def remove_selected(self):
        """Deletes the currently selected workout entry from the log."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a row to remove.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this workout entry?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.No:
            return

        with open(csv_file, "r") as f:
            reader = list(csv.DictReader(f))

        if 0 <= selected_row < len(reader):
            del reader[selected_row]

        with open(csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(reader)

        self.load_csv()

    def open_add_window(self):
        """Opens the AddWorkoutWindow to input a new session."""
        self.add_window = AddWorkoutWindow(refresh_callback=self.load_csv)
        self.add_window.show()

    def make_chart(self):
        """Shows volume progression (Weight × Reps × Sets) for exercises logged more than once."""
        try:
            with open(csv_file, "r") as f:
                reader = csv.DictReader(f)
                data = list(reader)
        except FileNotFoundError:
            print("No workout log found.")
            return

        if not data:
            QMessageBox.warning(self, "No Workout Data", "Please Add a Workout")
            return

        # Dictionary: exercise → list of volumes
        progress = {}

        for row in data:
            exercise = row.get("Exercise", "").strip()

            try:
                reps = int(row.get("Reps", 0))
                sets = int(row.get("Sets", 0))
                weight = float(row.get("Weight", 0))
            except ValueError:
                continue

            volume = weight * reps * sets  # TOTAL WORKLOAD

            if exercise not in progress:
                progress[exercise] = []

            progress[exercise].append(volume)

        # Only exercises with 2+ sessions
        multi_logged = {ex: vols for ex, vols in progress.items() if len(vols) > 1}

        if not multi_logged:
            QMessageBox.information(
                self,
                "Not Enough Data",
                "You need at least 2 logged sessions per exercise to show volume progress."
            )
            return

        num_exercises = len(multi_logged)
        plt.figure(figsize=(10, 4 * num_exercises))

        for idx, (exercise, volumes) in enumerate(multi_logged.items(), start=1):

            sessions = list(range(1, len(volumes) + 1))

            ax = plt.subplot(num_exercises, 1, idx)

            ax.plot(
                sessions,
                volumes,
                marker="o",
                linewidth=2,
                color="purple"
            )

            ax.set_title(f"{exercise} — Total Training Volume Over Time")
            ax.set_xlabel("Session Number")
            ax.set_ylabel("Volume (Weight × Reps × Sets)")

            ax.grid(True, linestyle="--", alpha=0.4)

        plt.tight_layout()
        plt.show()




if __name__ == "__main__":
    # Create application and shows main window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
