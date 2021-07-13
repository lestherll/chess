from typing import Union, List, Any, Optional

from chess.model.pieces import Piece


class Block:

    def __init__(self, x: int, y: int, piece: Optional[Piece] = None) -> None:
        self.x: int = x
        self.y: int = y
        self.piece: Optional[Piece] = piece

    def __repr__(self) -> str:
        return f"Block(x={self.x}, y={self.y}, piece={self.piece})"

    def __str__(self) -> str:
        return f"{self.piece}"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Block):
            if other.x == self.x and other.y == self.y:
                return True
        return False


class Board:

    def __init__(self) -> None:
        self.blocks: List[List[Block]] = [[Block(x=i, y=j) for i in range(8)] for j in range(8)]

    def __len__(self) -> int:
        return len(self.blocks)

    def __getitem__(self, pos: Union[int, Block]) -> Union[Block, list[Block], IndexError]:
        if isinstance(pos, Block):
            return self.blocks[pos.y][pos.x]
        return self.blocks[pos]

    def put_piece(self, block: Block, piece: Piece) -> None:
        self[block].piece = piece

    def move_piece(self, from_block: Block, to_block: Block) -> None:
        piece: Optional[Piece] = self[from_block].piece
        self[from_block].piece = None
        self[to_block].piece = piece
        # piece: Piece = self[from_block.x][from_block.y].piece
        # self[from_block.y][from_block.x].piece = None
        # self[to_block.y][to_block.x].piece = piece

    def remove_piece(self, from_block: Block):
        self[from_block].piece = None

    def show(self) -> None:
        for i in self:
            for j in i:
                print(str(j), end=" ")
            print()
        print()
