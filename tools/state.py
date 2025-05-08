"""State management for the writing assistant graph."""

from dataclasses import dataclass, field
from typing import Literal, TypedDict

@dataclass(kw_only=True)
class InputState:
    """The content from clipboard."""
    content: str
    """The behavior type determined from the last line."""
    behavior: Literal["topic", "rewrite", "generate", "cite", "conclude"]

@dataclass(kw_only=True)
class WritingState(InputState):
    """State of the writing assistant graph."""
    """The generated response."""
    response: str = field(default="")