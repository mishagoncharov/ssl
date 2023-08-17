import torch.nn as nn

from timm.models.resnet import (
    BasicBlock as _BasicBlock,
    Bottleneck as _Bottleneck,
    ResNet,
    _create_resnet
)


class BasicBlock(_BasicBlock):
    def __init__(
            self,
            *args,
            dropout_rate: float = 0.0,
            drop_channel_rate: float = 0.0,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        
        self.dropout = nn.Dropout(dropout_rate)
        self.drop_channel = nn.Dropout2d(drop_channel_rate)

    def forward(self, x):
        shortcut = x

        x = self.conv1(x)
        x = self.bn1(x)
        x = self.act1(x)

        x = self.dropout(x)
        x = self.drop_channel(x)
        x = self.drop_block(x)

        x = self.aa(x)

        x = self.conv2(x)
        x = self.bn2(x)

        if self.se is not None:
            x = self.se(x)

        if self.drop_path is not None:
            x = self.drop_path(x)

        if self.downsample is not None:
            shortcut = self.downsample(shortcut)
        x += shortcut
        x = self.act2(x)

        return x


class Bottleneck(_Bottleneck):
    def __init__(
            self,
            *args,
            dropout_rate: float = 0.0,
            drop_channel_rate: float = 0.0,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        
        self.dropout = nn.Dropout(dropout_rate)
        self.drop_channel = nn.Dropout2d(drop_channel_rate)

    def forward(self, x):
        shortcut = x

        x = self.conv1(x)
        x = self.bn1(x)
        x = self.act1(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.act2(x)
        
        x = self.drop_block(x)
        x = self.drop_channel(x)
        x = self.drop_block(x)

        x = self.aa(x)

        x = self.conv3(x)
        x = self.bn3(x)

        if self.se is not None:
            x = self.se(x)

        if self.drop_path is not None:
            x = self.drop_path(x)

        if self.downsample is not None:
            shortcut = self.downsample(shortcut)
        x += shortcut
        x = self.act3(x)

        return x


def resnet50(**kwargs) -> ResNet:
    """Constructs a ResNet-50 model.
    """
    kwargs = dict(block=Bottleneck, layers=[3, 4, 6, 3], **kwargs)
    return _create_resnet('resnet50', **kwargs)
