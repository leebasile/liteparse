"""Minimal DocumentInformation for pypdf compatibility."""

from __future__ import annotations

from typing import Optional


class DocumentInformation:
    """
    Stub matching ``pypdf.DocumentInformation``.

    LiteParse does not currently extract PDF metadata fields, so all
    properties return ``None``.  This object exists so that code which
    accesses ``reader.metadata.title`` etc. does not crash with an
    ``AttributeError``.
    """

    @property
    def title(self) -> Optional[str]:
        return None

    @property
    def author(self) -> Optional[str]:
        return None

    @property
    def subject(self) -> Optional[str]:
        return None

    @property
    def creator(self) -> Optional[str]:
        return None

    @property
    def producer(self) -> Optional[str]:
        return None

    @property
    def creation_date(self) -> None:
        return None

    @property
    def modification_date(self) -> None:
        return None

    def __repr__(self) -> str:
        return "DocumentInformation()"
