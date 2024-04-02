import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox, QInputDialog

class ToDoListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Création du widget central et du layout vertical
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Champ de saisie pour les nouvelles tâches
        self.task_input = QLineEdit()
        layout.addWidget(self.task_input)

        # Bouton d'ajout de tâche
        add_button = QPushButton("Ajouter")
        add_button.clicked.connect(self.addTask)
        layout.addWidget(add_button)

        # Bouton de modification de tâche
        modify_button = QPushButton("Modifier")
        modify_button.clicked.connect(self.modifyTask)
        layout.addWidget(modify_button)

        # Bouton de suppression de tâche
        delete_button = QPushButton("Supprimer")
        delete_button.clicked.connect(self.deleteTask)
        layout.addWidget(delete_button)

        # Liste pour afficher les tâches
        self.tasks_list = QListWidget()
        layout.addWidget(self.tasks_list)

        # Définition du widget central
        self.setCentralWidget(central_widget)
        self.setWindowTitle("To-Do List avec Qt6")

    def addTask(self):
        task = self.task_input.text()
        if task:  # Ajouter la tâche uniquement si le champ n'est pas vide
            self.tasks_list.addItem(task)
            self.task_input.clear()

    def modifyTask(self):
        selected_items = self.tasks_list.selectedItems()
        if not selected_items:  # Vérifier si un élément est sélectionné
            QMessageBox.information(self, "Modification de tâche", "Veuillez sélectionner une tâche à modifier.")
            return
        for item in selected_items:
            # Demande la nouvelle valeur pour la tâche sélectionnée
            new_task, ok = QInputDialog.getText(self, "Modifier tâche", "Modifier la tâche sélectionnée :", QLineEdit.Normal, item.text())
            if ok and new_task:
                item.setText(new_task)

    def deleteTask(self):
        selected_items = self.tasks_list.selectedItems()
        if not selected_items:  # Vérifier si un élément est sélectionné
            QMessageBox.information(self, "Suppression de tâche", "Veuillez sélectionner une tâche à supprimer.")
            return
        for item in selected_items:
            self.tasks_list.takeItem(self.tasks_list.row(item))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    to_do_list_app = ToDoListApp()
    to_do_list_app.show()
    sys.exit(app.exec())
