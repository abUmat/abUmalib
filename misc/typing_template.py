from typing import Generic, Iterator, List, Tuple, Dict, Iterable, Sequence, Callable, Union, Optional, TypeVar
T = TypeVar('T')
Pair = Tuple[int, int]
Graph = List[List[int]]
Poly = List[int]
Vector = List[int]
Matrix = List[List[int]]
Func10 = Callable[[int], None]
Func20 = Callable[[int, int], None]
Func11 = Callable[[int], int]
Func21 = Callable[[int, int], int]
Func31 = Callable[[int, int, int], int]
