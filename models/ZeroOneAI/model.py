from core.base import LLM
from fireworks.client import Fireworks
import yaml
import os


class Yi(LLM):
    """
    An abstract class representing Yi models by 01.AI provided by the Fireworks AI API.

    Attributes:
        NAME (str): The name of the model.
    """

    def __init__(
        self, randomly_flip_options: bool = False, shuffle_answer_options: bool = False
    ):
        super().__init__(
            randomly_flip_options=randomly_flip_options,
            shuffle_answer_options=shuffle_answer_options,
        )
        if "FIREWORKS_API_KEY" not in os.environ:
            raise ValueError(
                "Cannot access Fireworks AI API due to missing API key. Please store your API key in environment variable 'FIREWORKS_API_KEY'."
            )
        # The client object for the Fireworks API
        self._CLIENT = Fireworks(api_key=os.environ["FIREWORKS_API_KEY"])
        self.RESPONSE_FORMAT = None
        with open("./models/ZeroOneAI/prompts.yml") as f:
            self._PROMPTS = yaml.safe_load(f)

    def prompt(self, prompt: str, temperature: float = 0.0, seed: int = 42) -> str:
        """
        Generates a response to the provided prompt.

        Args:
            prompt (str): The prompt to generate a response for.
            temperature (float): The temperature value of the LLM. For strictly decision models, we use a temperature of 0.0.
            seed (int): The seed for controlling the LLM's output. It is not used in Yi-Large 2 model.

        Returns:
            str: The response generated by the LLM.
        """
        # Call the chat completions API endpoint
        response = self._CLIENT.chat.completions.create(
            model=self.NAME,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )

        # Extract and return the answer
        return response.choices[0].message.content


class YiLarge(Yi):
    """
    A class representing a YiLarge LLM.

    Attributes:
        NAME (str): The name of the model.
    """

    def __init__(
        self, randomly_flip_options: bool = False, shuffle_answer_options: bool = False
    ):
        super().__init__(
            randomly_flip_options=randomly_flip_options,
            shuffle_answer_options=shuffle_answer_options,
        )
        self.NAME = "accounts/yi-01-ai/models/yi-large"
