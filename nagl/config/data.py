"""Models to define the train, val, test data sets."""
import typing

import pydantic

MetricType = typing.Literal["rmse", "mse", "mae"]


@pydantic.dataclasses.dataclass(config={"extra": pydantic.Extra.forbid})
class Target:
    """Defines a particular target to train / evaluate against."""

    column: str = pydantic.Field(
        ..., description="The column in the source field that contains the target data."
    )
    readout: str = pydantic.Field(
        ...,
        description="The name of the model readout that predicts the target data.",
    )
    metric: MetricType = pydantic.Field(
        ...,
        description="The metric to use when comparing the target data with the "
        "model output.",
    )


@pydantic.dataclasses.dataclass(config={"extra": pydantic.Extra.forbid})
class Dataset:
    """Defines the targets to train / evaluate the model against during a given
    stage (i.e train, val, test)."""

    sources: typing.List[str] = pydantic.Field(
        ..., description="The paths to the data."
    )
    targets: typing.List[Target] = pydantic.Field(
        ..., description="The targets to train / evaluate against."
    )
    batch_size: typing.Optional[int] = pydantic.Field(
        None, description="The batch size."
    )


@pydantic.dataclasses.dataclass(config={"extra": pydantic.Extra.forbid})
class DataConfig:
    """Defines the train, val, and test data sets."""

    training: Dataset = pydantic.Field(
        ...,
        description="The training data.",
    )
    validation: typing.Optional[Dataset] = pydantic.Field(
        None,
        description="The validation data.",
    )
    test: typing.Optional[Dataset] = pydantic.Field(
        None,
        description="The test data.",
    )
