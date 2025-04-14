import sys
from model.model import AppModel, AppConfig
from controller.controller import Controller

from PyQt5.QtWidgets import QApplication

from view.view import View


if __name__ == "__main__":
    # Initialize model and controller
    app_model = AppModel()        # Initialize the model
    app_state = AppConfig()        # Initialize the state
    controller = Controller(app_model, app_state)  # Initialize the controller

    # Initialize view and run application
    app = QApplication(sys.argv)
    view = View(controller)
    view.show()
    sys.exit(app.exec_())
    
    """
    while True:
        # Show a prompt and get user input
        command = input("Enter command (increment/get/exit): ").strip().lower()
        
        if command == "exit":
            print("Exiting the application.")
            break

        # Handle the command via the controller
        controller.handle_command(command)
    """