from typing import Annotated, Literal
import numpy as np
from numpy.typing import NDArray

ByteArray8x8 = Annotated[NDArray[np.byte], Literal[8, 8]]
CharArray8x8 = Annotated[NDArray[np.character], Literal[8, 8]]
