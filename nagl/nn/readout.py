import typing

import torch

from nagl.molecules import DGLMolecule, DGLMoleculeBatch
from nagl.nn import Sequential
from nagl.nn.pooling import PoolingLayer
from nagl.nn.postprocess import PostprocessLayer


class ReadoutModule(torch.nn.Module):
    """A module that transforms node features generated by a series of graph
    convolutions via propagation through a pooling, feed forward and optional
    postprocess layer.
    """

    def __init__(
        self,
        pooling_layer: PoolingLayer,
        forward_layers: Sequential,
        postprocess_layer: typing.Optional[PostprocessLayer] = None,
    ):
        """

        Args:
            pooling_layer: The pooling layer that will concatenate the node features
                computed by a graph convolution into appropriate extended features (e.g.
                bond or angle features). The concatenated features will be provided as
                input to the dense readout layers.
            forward_layers: The dense NN layers to apply to the output of the
                pooling layers that will predict the readout values.
            postprocess_layer: A (optional) postprocessing layer to apply to the output
                of the readout layers
        """

        super().__init__()

        self.pooling_layer = pooling_layer
        self.forward_layers = forward_layers
        self.postprocess_layer = postprocess_layer

    def forward(
        self, molecule: typing.Union[DGLMolecule, DGLMoleculeBatch]
    ) -> torch.Tensor:
        x = self.pooling_layer.forward(molecule)
        x = self.forward_layers.forward(x)

        if self.postprocess_layer is not None:
            x = self.postprocess_layer.forward(molecule, x)

        return x