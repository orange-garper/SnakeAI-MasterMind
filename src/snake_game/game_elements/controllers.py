from abc import ABC, abstractmethod
from typing import List, Union
import pygame
from pygame.math import Vector2


class AbstractController(ABC):
    """
    Abstract base class for creating snake controllers.

    This class defines the structure for creating custom controllers to control a snake in a game.

    Attributes:
        _buttons (dict[str, Vector2]): A dictionary mapping key names to Vector2 directions.
        _pressed_button (Vector2): The currently pressed button or direction.
        _do_stupid (bool): A flag indicating whether the controller is making a "stupid" move.

    Methods:
        __init__(self, start_pressed_button: Union[str, Vector2] = None):
            Initialize the controller with an optional initial button or direction.

        press_button(self, event_key: int, snake_body: List[Vector2]):
            Handle a button press event and update the controller's state accordingly.

        get_action(self) -> Union[Vector2, None]:
            Get the current action or direction from the controller. Returns None if no action is set.

    Usage Example:
    --------------
    To create a custom controller class, follow these steps:

    1. Subclass AbstractController:

    ```python
    class CustomController(AbstractController):
        def __init__(self):
            super().__init__()

        def press_button(self, event_key: int, snake_body: List[Vector2]):
            # Customize the logic for handling user input or AI decisions here
            pass

        def get_action(self) -> Union[Vector2, None]:
            # Customize the logic for retrieving the current action here
            pass
    ```

    2. Instantiate and use your controller:

    ```python
    custom_controller = CustomController()
    current_action = custom_controller.get_action()
    ```

    Note:
    - This class provides a basic structure for creating snake controllers and defines common attributes
      and methods used for controlling the snake.
    - Customize the `press_button` and `get_action` methods in your subclass to implement your specific
      controller logic.
    - The `_do_stupid` attribute can be used to track whether the controller is making undesirable moves.
    """

    def __init__(self, start_pressed_button: Union[str, Vector2] = None):
        """
        Initialize the controller with an optional initial button or direction.

        Args:
            start_pressed_button (str | Vector2, optional): The initial button or direction.
                Defaults to None.
        """
        self._buttons: dict[
            str, Vector2
        ] = {}  # Customize this dictionary with key-direction mappings
        self._pressed_button: Vector2 = start_pressed_button or Vector2(0, 0)
        self._do_stupid = None  # If needed)

    @abstractmethod
    def press_button(self, event_key: int, snake_body: List[Vector2]):
        """
        Handle a button press event and update the controller's state accordingly.

        Args:
            event_key (int): The key code of the pressed button.
            snake_body (List[Vector2]): The current snake body positions.
        """
        raise NotImplementedError()

    def get_action(self) -> Union[Vector2, None]:
        """
        Get the current action or direction from the controller.

        Returns:
            Union[Vector2, None]: The current action as a Vector2 direction or None if no action is set.
        """
        return self._pressed_button

    @property
    def do_stupid(self) -> bool:
        """
        Get the flag indicating whether the controller is making a "stupid" move.

        Returns:
            bool: True if the controller is making a "stupid" move, False otherwise.
        """
        return self._do_stupid


class HumansController(AbstractController):
    """
    Controller class for human players in a snake game.

    This controller allows human players to control the snake using keyboard input.

    Attributes:
        _buttons (dict[str, Vector2]): A dictionary mapping key names to Vector2 directions.
            Default mapping: Arrow keys for movement.
        _pressed_button (Vector2): The currently pressed button or direction.
        _do_stupid (bool): A flag indicating whether the controller is making a "stupid" move.

    Note:
    - This controller is designed for human players and relies on keyboard input.
    - You can customize the `_buttons` attribute to define different key-direction mappings.
    - The `_do_stupid` flag can be used to track whether the controller is making undesirable moves.

    """

    def __init__(self, start_pressed_button: Union[str, Vector2] = None):
        """
        Initialize the human controller.

        Args:
            start_pressed_button (Union[str, Vector2], optional): The initial button or direction.
                Defaults to None.
        """
        # Default key-direction mappings (Arrow keys for movement)
        self._buttons = {
            "K_UP": Vector2(0, -1),
            "K_LEFT": Vector2(-1, 0),
            "K_DOWN": Vector2(0, 1),
            "K_RIGHT": Vector2(1, 0),
        }
        self._pressed_button = start_pressed_button or Vector2(0, 0)

    def press_button(self, event_key: int, snake_body: List[Vector2]):
        """
        Handle a button press event and update the controller's state accordingly.

        This method processes a button press event and determines the new direction for the snake based on the pressed key.
        It ensures that the snake cannot make a 180-degree turn, which would be an invalid move.

        Args:
            event_key (int): The key code of the pressed button.
            snake_body (List[Vector2]): The current snake body positions.

        Notes:
            - The method checks if the pressed key corresponds to a valid direction (e.g., arrow keys).
            - It also ensures that the new direction is not opposite to the current direction of the snake.
            - If the pressed key is not valid or would result in an invalid move, the current direction is maintained.

        Example:
            To handle a button press event and update the controller's state:

            ```python
            # Get the key code of the pressed button, e.g., from a Pygame event.
            event_key = pygame.key.get_pressed()[pygame.K_LEFT]

            # Call the press_button method to update the controller's state.
            human_controller.press_button(event_key, snake_body)
            ```
        """
        self._pressed_button = next(
            (
                value
                for key, value in self._buttons.items()
                if getattr(pygame, key) == event_key
                and (snake_body[0] + value != snake_body[1])
            ),
            self._pressed_button,
        )

    @property
    def get_action(self) -> Union[Vector2, None]:
        """
        Get the current action or direction from the controller.

        Returns:
            Union[Vector2, None]: The current action as a Vector2 direction or None.
        """
        return self._pressed_button
    
    @property
    def do_stupid(self) -> bool:
        raise NotImplementedError("The variable self._do_stupid is not provided for a Human Controller")


class AIsController(AbstractController):
    """
    Controller for AI-controlled snake movement.

    This controller handles AI-generated actions to control the movement of the snake in the game.

    Args:
        start_pressed_button (str | Vector2, optional): The initial button or direction for the snake.
            Defaults to None, which corresponds to no initial movement.

    Attributes:
        _buttons (dict): A dictionary mapping AI action codes to direction vectors.
        _pressed_button (Vector2): The currently pressed button or direction.
        _do_stupid (bool): A flag indicating if the AI's action would result in an invalid move.

    """

    def __init__(self, start_pressed_button: str | Vector2 = None):
        """
        Initialize a new AI controller.

        Args:
            start_pressed_button (str | Vector2, optional): The initial button or direction for the snake.
                Defaults to None, which corresponds to no initial movement.

        """
        self._buttons = {
            "0": Vector2(0, -1),
            "1": Vector2(-1, 0),
            "2": Vector2(0, 1),
            "3": Vector2(1, 0),
        }
        self._pressed_button = start_pressed_button or Vector2(0, 0)
        self._do_stupid = None

    def press_button(self, ais_action: int, snake_body: List[Vector2]):
        """
        Handle an AI action and update the controller's state accordingly.

        This method processes an AI action and determines the new direction for the snake based on the action code provided.
        It ensures that the AI action is valid and corresponds to a predefined direction.

        Args:
            ais_action (int): The action code provided by the AI.
            snake_body (List[Vector2]): The current snake body positions.

        Raises:
            AssertionError: If the AI action code is not recognized or valid, an assertion error is raised.

        Notes:
            - The method checks if the AI action code corresponds to a valid direction in `_buttons`.
            - It also ensures that the new direction is not opposite to the current direction of the snake.
            - If the AI action code is invalid or would result in an invalid move, an assertion error is raised.
            - If the AI action is valid, the controller's state is updated accordingly.

        Example:
            To handle an AI action and update the controller's state:

            ```python
            # Get the AI's action code, e.g., from an AI agent.
            ai_action = 1

            # Call the press_button method to update the controller's state.
            ai_controller.press_button(ai_action, snake_body)
            ```
        """
        assert (
            str(ais_action) in self._buttons
        ), f"Oh, is your artificial intelligence so stupidly configured?\
Your artificial intelligence decided that it was necessary to violate the existing boundaries of reality,\
and intended to perform an action under the number {ais_action},\
which is even worse than dividing by zero.\
The {ais_action} number is not recorded in self._buttons,\
so come back when you fix your 'child', which you obviously made under booze.\
The eagle stirs up her nest, isn't it?)"

        action = self._buttons.get(str(ais_action))
        if do_not_stupid := snake_body[0] + action != snake_body[1]:
            self._pressed_button = action
        self._do_stupid = not do_not_stupid

    @property
    def get_action(self):
        """
        Get the currently pressed button or direction.

        Returns:
            Vector2: The currently pressed button or direction for snake movement.

        """
        return self._pressed_button

    @property
    def do_stupid(self) -> Union[bool, None]:
        """
        Check if the AI's action would result in an invalid move.

        Returns:
            bool: True if the AI's action would result in an invalid move, False otherwise.

        """
        return self._do_stupid
