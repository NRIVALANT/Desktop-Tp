import cmd

class ToDoList(cmd.Cmd):
    prompt = '(to-do) '
    intro = 'Bienvenue dans votre to-do list ! Tapez help ou ? pour lister les commandes.\n'
    
    def __init__(self):
        super(ToDoList, self).__init__()
        self.to_do_list = []

    def do_ajouter(self, item):
        "Ajoute un élément à la to-do list: ajouter [élément]"
        self.to_do_list.append(item)
        print(f"'{item}' a été ajouté à la liste.")

    def do_lister(self, args):
        "Liste tous les éléments de la to-do list: lister"
        for idx, item in enumerate(self.to_do_list, 1):
            print(f"{idx}. {item}")

    def do_supprimer(self, position):
        "Supprime un élément de la to-do list par sa position: supprimer [position]"
        try:
            position = int(position) - 1
            if position < 0 or position >= len(self.to_do_list):
                print("Position invalide.")
                return
            removed_item = self.to_do_list.pop(position)
            print(f"'{removed_item}' a été supprimé de la liste.")
        except ValueError:
            print("Veuillez entrer un nombre.")

    def do_quitter(self, args):
        "Quitte l'application: quitter"
        print("Merci d'avoir utilisé la to-do list. À bientôt !")
        return True

if __name__ == '__main__':
    ToDoList().cmdloop()
