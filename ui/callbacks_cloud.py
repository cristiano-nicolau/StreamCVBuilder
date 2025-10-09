from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class EditorCallbacks:
    on_save: Callable[[], None]
    on_load_example: Callable[[], None]
    on_delete: Callable[[], None]
    on_open_preview: Callable[[], None]
    on_download: Callable[[], None]
    on_upload: Callable[[], None]


@dataclass(frozen=True)
class PreviewCallbacks:
    on_edit: Callable[[], None]
    on_load_example: Callable[[], None]