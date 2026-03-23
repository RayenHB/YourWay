from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from FastAPI_back.db.base import ConcreteTable
from FastAPI_back.utils.errors import DatabaseError, NotFoundError, UnprocessableError
from typing import Any, AsyncGenerator, Generic, Type, Optional, Dict, List
from sqlalchemy import Select, asc, delete, desc, func, select, update, or_,and_
from sqlalchemy.engine import Result
from asyncpg.exceptions import UniqueViolationError
import traceback


__all__ = ("BaseRepository",)

from FastAPI_back.utils.tools import build_filters


class BaseRepository(Generic[ConcreteTable]):
    """This class implements the base interface for working with the database
    and makes it easier to work with type annotations.

    The Session class implements the database interaction layer.
    """

    schema_class: Type[ConcreteTable]
    _ERRORS = (IntegrityError, InvalidRequestError, UniqueViolationError)

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        super().__init__()
        if not self.schema_class:
            raise UnprocessableError(
                message=(
                    "Cannot initiate the class without schema_class attribute"
                )
            )

    async def _update(
        self, key: str, value: Any, payload: dict[str, Any]
    ) -> ConcreteTable:
        """Updates an existing instance of the model in the related table.
        If some data does not exist in the payload, then the null value will
        be passed to the schema class."""

        query = (
            update(self.schema_class)
            .where(getattr(self.schema_class, key) == value)
            .values(payload)
            .returning(self.schema_class)
        )
        result: Result = await self._session.execute(query)

        if not (schema := result.scalar_one_or_none()):
            raise DatabaseError

        return schema

    async def _get(self, id_: int, relationships: Optional[List[str]] = None) -> ConcreteTable:
        query = select(self.schema_class).where(self.schema_class.id == id_)

        if relationships:
            for relationship in relationships:
                query = query.options(selectinload(getattr(self.schema_class, relationship)))

        result: Result = await self._session.execute(query)

        if not (instance := result.scalars().one_or_none()):
            raise NotFoundError

        return instance

    async def count(self) -> int:
        result: Result = await self._session.execute(func.count(self.schema_class.id))
        value = result.scalar()

        if not isinstance(value, int):
            raise UnprocessableError(
                message=(
                    "For some reason count function returned not an integer."
                    f"Value: {value}"
                ),
            )

        return value

    async def find_by(self, filters: Dict[str, Any], relationships: Optional[List[str]] = None) -> Optional[
         ConcreteTable]:
        """Find a single instance of the model by dynamic attributes.

        Args:
            filters (Dict[str, Any]): A dictionary of attributes and their corresponding values to filter by.
            relationships (Optional[List[str]]): A list of relationship names to eagerly load.

        Returns:
            Optional[ConcreteTable]: The found instance or None if no instance is found.
        """
        query = select(self.schema_class)

        # Apply relationships if provided
        if relationships:
            for relationship in relationships:
                query = query.options(selectinload(getattr(self.schema_class, relationship)))

        # Apply filters dynamically
        conditions = [
            getattr(self.schema_class, key) == value if value is not None else None
            for key, value in filters.items()
        ]
        query = query.where(*conditions).limit(1)

        result: Result = await self._session.execute(query)
        return result.scalars().first()

    async def _first(self, by: str = "id") -> Optional[ConcreteTable]:
        result: Result = await self._session.execute(
            select(self.schema_class).order_by(asc(by)).limit(1)
        )

        return result.scalar_one_or_none()

    async def _last(self, by: str = "id") -> ConcreteTable:
        result: Result = await self._session.execute(
            select(self.schema_class).order_by(desc(by)).limit(1)
        )

        if not (_result := result.scalar_one_or_none()):
            raise NotFoundError

        return _result
    


    async def _save(self, payload: dict[str, Any]) -> ConcreteTable:
        try:
            schema = self.schema_class(**payload)
            self._session.add(schema)
            await self._session.flush()
            await self._session.refresh(schema)
            return schema
        except Exception as e:
            print("💥 DATABASE ERROR:", e)
            traceback.print_exc()
            raise

    async def _all(self) -> AsyncGenerator[ConcreteTable, None]:
        result: Result = await self._session.execute(select(self.schema_class))
        schemas = result.scalars().all()

        for schema in schemas:
            yield schema

    async def _all_paginated(
        self,
        page: int,
        page_size: int,
        relationships: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if relationships is None:
            relationships = []

        # Base query for the count
        total_count_query = select(func.count()).select_from(self.schema_class)

        if filters:
            total_count_query = build_filters(self.schema_class, total_count_query, filters)

        # Execute count query
        total_count_result: Result = await self._session.execute(total_count_query)
        total_count = total_count_result.scalar()

        # Base query for the data
        base_query = select(self.schema_class)

        # Add filters and relationships to the base query
        if filters:
            base_query = build_filters(self.schema_class, base_query, filters)

        for relationship in relationships:
            base_query = base_query.options(selectinload(getattr(self.schema_class, relationship)))

        # Apply pagination
        offset = (page - 1) * page_size
        paginated_query = base_query.limit(page_size).offset(offset)

        # Execute paginated query
        result: Result = await self._session.execute(paginated_query)
        schemas = result.scalars().all()

        return {
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "result": schemas
        }


    async def _all_with_filters(
        self,
        relationships: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[Any] = None,
        limit: Optional[int] = None,
    ) -> AsyncGenerator[ConcreteTable, None]:
        # Initialize relationships as an empty list if None
        if relationships is None:
            relationships = []

        # Start with the base select statement
        query = select(self.schema_class)

        # Apply dynamic relationships loading
        for relationship in relationships:
            query = query.options(selectinload(getattr(self.schema_class, relationship)))

        # Apply dynamic filters
        if filters:
            query = build_filters(self.schema_class, query, filters)

        if order_by is not None:
            query = query.order_by(order_by)

    # Apply limit
        if limit is not None:
            query = query.limit(limit)
        # Execute the query
        result: Result = await self._session.execute(query)
        schemas = result.scalars().all()

        # Return the results
        for schema in schemas:
            yield schema

    async def _delete(self, id_: int) -> None:
        await self._session.execute(
            delete(self.schema_class).where(self.schema_class.id == id_)
        )

    async def _exists(
        self,
        filters: Dict[str, Any],
        exclude_id: Optional[Any] = None,
        operator: Optional[str] = "OR",
    ) -> bool:
        """Check if a record exists by given filters using OR operator, with optional exclusion of a specific record."""

        try:
            conditions = [
                (
                    func.lower(getattr(self.schema_class, key)) == value.strip().lower()
                    if isinstance(value, str)
                    else getattr(self.schema_class, key) == value
                )
                for key, value in filters.items()
                if value is not None
            ]

            if not conditions:
                return False

            # Optionally exclude a specific record by its ID
            if exclude_id is not None:
                conditions.append(getattr(self.schema_class, "id") != exclude_id)

        except AttributeError as e:
            raise UnprocessableError(message=f"Invalid attribute in filters: {str(e)}")
        if operator == "OR":
            query = select(self.schema_class).where(or_(*conditions))
        else:
            query = select(self.schema_class).where(and_(*conditions))
        result = await self._session.execute(query)
        return result.scalars().first() is not None
