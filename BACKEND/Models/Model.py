from sqlalchemy import Column, Integer, String, LargeBinary, Text, ForeignKey
from sqlalchemy.orm import relationship
from db.Database import Base


class Fileupload(Base):
    __tablename__ = "fileupload"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=False, index=True)
    data = Column(LargeBinary)

    # Relationships (must be indented inside the class)
    images = relationship("Image", back_populates="document", cascade="all, delete")
    summaries = relationship("Summary", back_populates="document", cascade="all, delete")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)  # ✅ separate primary key
    filename = Column(String, index=True)  # ✅ allow duplicates
    data = Column(LargeBinary)

    # Foreign key to Fileupload
    document_id = Column(Integer, ForeignKey("fileupload.id"))
    document = relationship("Fileupload", back_populates="images")


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, index=True)  # ✅ separate primary key
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # ✅ unlimited length
    summary = Column(Text, nullable=False)

    # Foreign key to Fileupload
    document_id = Column(Integer, ForeignKey("fileupload.id"))
    document = relationship("Fileupload", back_populates="summaries")
