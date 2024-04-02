import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QGridLayout
import random

class ChoiceDiceDialog(QDialog):
    def __init__(self, dice_results, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Choisissez les dés à relancer')

        self.layout = QVBoxLayout()

        self.buttons = []
        self.selected_dice = []

        self.grid_layout = QGridLayout()
        for i, result in enumerate(dice_results):
            button = QPushButton(str(result))
            button.clicked.connect(lambda _, index=i: self.toggle_dice(index))
            self.buttons.append(button)
            self.grid_layout.addWidget(button, i // 3, i % 3)
        self.layout.addLayout(self.grid_layout)

        self.confirm_button = QPushButton("Valider")
        self.confirm_button.clicked.connect(self.accept)
        self.layout.addWidget(self.confirm_button)

        self.setLayout(self.layout)

    def toggle_dice(self, index):
        if index in self.selected_dice:
            self.selected_dice.remove(index)
            self.buttons[index].setStyleSheet('')
        else:
            self.selected_dice.append(index)
            self.buttons[index].setStyleSheet('background-color: yellow')

    def get_selected_dice(self):
        return self.selected_dice


class YamsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yams")
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel("Bienvenue dans le jeu de Yams !", self)
        self.label.setGeometry(50, 50, 300, 30)

        self.button_roll = QPushButton("Lancer les dés", self)
        self.button_roll.setGeometry(150, 150, 150, 30)
        self.button_roll.clicked.connect(self.roll_dice)

        self.button_choose = QPushButton("Choisir une combinaison", self)
        self.button_choose.setGeometry(150, 200, 200, 30)
        self.button_choose.setEnabled(False)
        self.button_choose.clicked.connect(self.choose_combination)

        self.scores_table = QTableWidget(self)
        self.scores_table.setGeometry(200, 500, 400, 200)
        self.scores_table.setColumnCount(2)
        self.scores_table.setHorizontalHeaderLabels(["Combinaison", "Score"])

        self.combinations = ["As", "Deux", "Trois", "Quatre", "Cinq", "Six", "Brelan", "Carré", "Full", "Petite Suite", "Grande Suite", "Yams", "Chance"]
        self.dés = [1, 2, 3, 4, 5, 6]
        self.scores = {combination: None for combination in self.combinations}  # Initialize scores dictionary
        for i, combination in enumerate(self.combinations):
            self.scores_table.insertRow(i)
            self.scores_table.setItem(i, 0, QTableWidgetItem(combination))

        self.tours = 0
        self.dice_results = []

    def roll_dice(self):
        self.tours += 1
        if self.tours <= 3:
            if self.tours == 1:
                self.dice_results = [random.randint(1, 6) for _ in range(5)]
            else:
                # Allow the player to choose which dice to re-roll
                choice_dialog = ChoiceDiceDialog(self.dice_results, self)
                if choice_dialog.exec() == QDialog.Accepted:
                    selected_dice = choice_dialog.get_selected_dice()
                    for index in selected_dice:
                        self.dice_results[index] = random.randint(1, 6)
            result_text = "Résultats du lancer : " + ", ".join(str(result) for result in self.dice_results)
            self.label.setText(result_text)

            if self.tours < 3:
                self.button_roll.setText("Relancer les dés")
            else:
                self.button_roll.setEnabled(False)
                self.button_choose.setEnabled(True)

    def choose_combination(self):
        choice_dialog = ChoiceDiceDialog(self.combinations, self)
        choice_dialog.exec()
        chosen_combination = choice_dialog.get_selected_combination()
        if chosen_combination:
            score = self.calculate_score(chosen_combination)
            self.scores[chosen_combination] = score
            self.display_score(chosen_combination)
        self.tours = 0  # Reset tours
        self.button_roll.setEnabled(True)
        self.button_choose.setEnabled(False)

    def display_score(self, combination):
        row_index = self.combinations.index(combination)
        self.scores_table.setItem(row_index, 1, QTableWidgetItem(str(self.scores[combination])))

    def calculate_score(self, combination):
        if combination == 'As':
            return self.dice_results.count(1)
        elif combination == 'Deux':
            return self.dice_results.count(2) * 2
        elif combination == 'Trois':
            return self.dice_results.count(3) * 3
        elif combination == 'Quatre':
            return self.dice_results.count(4) * 4
        elif combination == 'Cinq':
            return self.dice_results.count(5) * 5
        elif combination == 'Six':
            return self.dice_results.count(6) * 6
        elif combination == 'Brelan':
            counts = {i: self.dice_results.count(i) for i in range(1, 7)}
            for count in counts.values():
                if count >= 3:
                    return sum(self.dice_results)              
        elif combination == "Petite Suite":
            if sorted(self.dice_results) in ([1, 2, 3, 4, 5]):
                return 25
        elif combination == "Grande Suite" :
            if sorted(self.dice_results) in ([ 2, 3, 4, 5, 6]) :
                return 25
        elif combination == "Full":
            counts = {i: self.dice_results.count(i) for i in range(1, 7)}
            if 2 in counts.values() and 3 in counts.values():
                return 30
        elif combination == 'Carré':
            # Count the occurrences of each dice roll
            counts = {i: self.dice_results.count(i) for i in range(1, 7)}
            # Check if any count is 4
            for value, count in counts.items():
                if count >= 4:
                    return 40
        elif combination == "Yams" :
            counts = {i : self.dice_results.count(i) for i in range(1,7)}
            if 5 in counts.values():
                return 50
        elif combination == "Chance" :
            return sum(self.dice_results)
        return 0
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YamsWindow()
    window.show()
    sys.exit(app.exec())
