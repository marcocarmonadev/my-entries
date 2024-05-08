import asyncio
import datetime as dt
from dataclasses import dataclass

from clients import ClickUpClient
from helpers import Workbook


@dataclass
class HttpController:
    click_up_client: ClickUpClient

    async def register_super_purchases(
        self,
        xlsx_bytes: bytes,
    ):
        workbook = Workbook.from_bytes(xlsx_bytes)
        sheet = workbook.get_sheet_by_name("Sheet1")
        today = dt.datetime.today()
        await asyncio.gather(
            *[
                self.register_super_purchase(
                    task_id,  # type: ignore
                    place_of_purchase,  # type: ignore
                    quantity,  # type: ignore
                    cost,  # type: ignore
                    purchase_datetime=purchase_datetime or today,  # type: ignore
                )
                for (
                    name,
                    task_id,
                    place_of_purchase,
                    quantity,
                    cost,
                    purchase_datetime,
                ) in sheet.iter_rows(
                    min_row=2,
                    max_col=6,
                    values_only=True,
                )
                if task_id
            ]
        )
        workbook.close()

    async def register_super_purchase(
        self,
        task_id: str,
        place_of_purchase: str,
        quantity: int | float,
        cost: float,
        purchase_datetime: dt.datetime,
    ):
        unitary_cost = cost / quantity
        purchase_date = purchase_datetime.strftime(format="%Y-%m-%d")
        await asyncio.gather(
            self.click_up_client.create_task_comment(
                task_id,
                comment_text=f"{purchase_date} / ${unitary_cost} / {place_of_purchase}",
            ),
            self.click_up_client.update_task(
                task_id,
                status="closed",
            ),
        )
