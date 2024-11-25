from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from uuid import UUID

from src.models.items import Item

class ItemRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_item(self, item_data: Item) -> Item:
        """Create a new Item in the database (commit to db session)"""
        self.db_session.add(item_data)
        await self.db_session.commit()
        await self.db_session.refresh(_data)
        return item_data

    async def update_item(self, item_data: Item) -> Item:
        """Update existing Item in the db"""
        await self.db_session.commit()
        return item_data

    async def _get_item(self, criteria) -> Item:
        """Private method to retrieve an Item based on a given criteria"""
        stmt = select(Item).where(criteria)
        result = await self.db_session.execute(stmt)
        item = result.scalars().one_or_none()
        if item is None:
            raise NoResultFound("Item not found")
        return item

    async def get_item_by_id(self, item_id: UUID) -> Item:
        """Retrieve Item by its ID"""
        return await self._get_item(Item.item_id == item_id)

    async def get_item_by_name(self, item_name: str) -> Item:
        """Retrieve Item by its name"""
        return await self._get_item(Item.name == item_name)

    async def get_all_items(self) -> list[Item]:
        """Retrieve all Item objects from the database"""
        stmt = select(Item)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def delete_item(self, item_id: UUID) -> None:
        """Delete Item from the database by its ID"""
        item = await self.get_item_by_id(item_id)
        await self.db_session.delete(item)
        await self.db_session.commit()
