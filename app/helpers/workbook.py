from dataclasses import dataclass
from io import BytesIO

import openpyxl


@dataclass
class Workbook:
    workbook: openpyxl.Workbook

    @classmethod
    def from_bytes(
        cls,
        bytes: bytes,
    ):
        with BytesIO(
            initial_bytes=bytes,
        ) as bytes_io:
            return openpyxl.load_workbook(bytes_io)
