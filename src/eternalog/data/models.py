import datetime
import uuid

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Uuid
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import Relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Block(Base):
    __tablename__ = "block"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, init=True)

    content: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime)
    signature: Mapped[bytes] = mapped_column(Text)
    child_blocks: Relationship["Block"] = relationship(
        "Block", back_populates="parent_block", default=None
    )
    parent_block_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey(id), nullable=True, default=None, init=False
    )
    parent_block: Relationship["Block"] = relationship(
        "Block",
        remote_side=[id],
        back_populates="child_blocks",
        default=None,
        foreign_keys=[parent_block_id],
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        insert_default=datetime.datetime.now,
        default_factory=datetime.datetime.now,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        insert_default=datetime.datetime.now,
        default_factory=datetime.datetime.now,
    )
