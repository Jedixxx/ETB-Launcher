import subprocess
import customtkinter
from src.core.config import Config

ETB_APP_ID = "1943950"


class LaunchGame:
    """
    Defines the CTk button which is displayed for launching/closing the game
    Handles the logic for launching and closing the game
    Contains custom button states which correlate to the game states
    """

    def __init__(self, master, width, height, x, y, text_size):
        self.config = Config()
        self.launch_game_button = customtkinter.CTkButton(master=master, text="Launch Game", width=width, height=height,
                                                          font=("Arial", text_size, "bold"))

        self.width, self.height = width, height
        self.x, self.y = x, y

        self.steam_exe_path = self.config.config_data["paths"]["steam_path"]

        self.running_state = None
        self.update_function = self.update_button_loop

        self.launch_game_button.bind("<Enter>", self.on_hover)
        self.launch_game_button.bind("<Leave>", self.on_leave)

    def load(self):
        self.launch_game_button.place(x=self.x, y=self.y)

    def update_button_loop(self):
        prev_running_state = self.running_state
        self.running_state = self.game_running()

        if self.running_state == prev_running_state:
            return
        if self.running_state:
            self._change_state(button_state="Running")
        else:
            self._change_state(button_state="Default")

    def launch_game(self):
        self._change_state(button_state="Loading")
        launch_command = [self.steam_exe_path, "-applaunch", ETB_APP_ID]
        subprocess.run(launch_command, check=True)

    def close_game(self):
        self._change_state(button_state="Closing")
        close_command = [self.steam_exe_path, '+app_stop', ETB_APP_ID]
        subprocess.run(close_command, check=True)

    @staticmethod
    def game_running():
        backrooms_exe = "Backrooms.exe"
        result = subprocess.run(
            ['tasklist', '/FI', f'IMAGENAME eq {backrooms_exe}', '/NH'],
            stdout=subprocess.PIPE,
            text=True
        )

        return backrooms_exe.lower() in result.stdout.lower()

    def on_hover(self, event) -> None:
        self.launch_game_button.configure(width=self.width * 1.01, height=self.height * 1.01)
        self.launch_game_button.place(x=self.x - self.width * 0.005, y=self.y - self.height * 0.005)

    def on_leave(self, event) -> None:
        self.launch_game_button.configure(width=self.width, height=self.height)
        self.launch_game_button.place(x=self.x, y=self.y)

    def _change_state(self, button_state: str = "Default"):
        """
        Takes a state for the launch game button to be in and configures the button appropriately

        :param button_state: Expects a string of the desired state: "Default", "Loading", "Closing", "Running"
        """
        match button_state:
            case "Default":
                self.launch_game_button.configure(text="Launch Game", fg_color="green", command=self.launch_game)
            case "Loading":
                self.launch_game_button.configure(text="Loading...", fg_color="gray", command=None)
            case "Closing":
                self.launch_game_button.configure(text="Closing...", fg_color="gray", command=None)
            case "Running":
                self.launch_game_button.configure(text="Close Game", fg_color="blue", command=self.close_game)
