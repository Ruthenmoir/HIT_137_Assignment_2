from PIL import Image
from typing import List


class HistoryManager:
    def __init__(self):
        self.original_image = None
        self.current_image = None
        self.history: List[Image] = []
        self.current_index: int = -1
        self.status: str = ""

    def save_to_history(self, image: Image):
        """
        Saves the given image state to the history for undo/redo.

        :param image: The image to save to history
        """
        if self.original_image is None:
            self.original_image = image

        # Check if image is the same as the previous. If it is, don't add
        if image != self.current_image:
            self.history = self.history[:self.current_index + 1]
            self.current_image = image
            self.history.append(image)
            self.current_index = len(self.history) - 1

    def undo(self):
        """
        Reverts to the previous image state in the history.
        """
        if self.current_index > 0:
            self.current_index -= 1
            self.current_image = self.history[self.current_index]
            self.status = "Undo performed"
        else:
            self.status = "Nothing to undo"

    def redo(self):
        """
        Restores the next image state in the history.
        """
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            self.current_image = self.history[self.current_index]
            self.status = "Redo performed"
        else:
            self.status = "Nothing to redo"


    def reset(self):
        """
        Resets the image to its initial state.
        """
        if self.original_image is not None:
            self.history = [self.original_image]
            self.current_index = 0
            self.current_image = self.original_image
            self.status = "Image reset to original"
        else:
            self.status = "No image loaded"
