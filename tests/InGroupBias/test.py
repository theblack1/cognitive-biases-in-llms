from core.base import TestGenerator, LLM, RatioScaleMetric
from core.testing import TestCase, Template, TestConfig, DecisionResult


class InGroupBiasTestGenerator(TestGenerator):
    """
    Test generator for the In-group bias.

    Attributes:
        BIAS (str): The cognitive bias associated with this test generator.
        config (TestConfig): The test configuration for this cognitive bias.
    """

    def __init__(self):
        self.BIAS: str = "In Group Bias"
        self.config: TestConfig = super().load_config(self.BIAS)

    def generate(
        self,
        model: LLM,
        scenario: str,
        custom_values: dict = {},
        temperature: float = 0.0,
        seed: int = 42,
    ) -> TestCase:
        # Load the control and treatment templates
        control: Template = self.config.get_control_template()
        treatment: Template = self.config.get_treatment_template()

        # Populate the templates using the model and the scenario
        control, treatment = super().populate(
            model, control, treatment, scenario, temperature, seed
        )

        # Create a test case object
        test_case = TestCase(
            bias=self.BIAS,
            control=control,
            treatment=treatment,
            generator=model.NAME,
            temperature=temperature,
            seed=seed,
            scenario=scenario,
            variant=None,
            remarks=None,
        )

        return test_case


class InGroupBiasMetric(RatioScaleMetric):
    """
    A class that describes the quantitative evaluation of the In-group bias in a model.

    Metric:
    𝔅(â₁, â₂) = (â₂ - â₁) / max(â₁, â₂) ∈ [-1, 1]

    where:
    â₁, â₂ are the chosen answers for the control and treatment versions, respectively;

    Attributes:
        test_results (list[tuple[TestCase, DecisionResult]]): A list of test results to be used for the metric calculation.
    """

    def __init__(self, test_results: list[tuple[TestCase, DecisionResult]]):
        super().__init__(test_results)
