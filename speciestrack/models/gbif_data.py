from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from speciestrack.models import db


class GbifData(db.Model):
    """Model for GBIF species observation data"""

    __tablename__ = 'gbif_data'

    # Primary key
    id = Column(Integer, primary_key=True)

    # Observation data
    scientific_name = Column(String(500), nullable=False)
    observation_count = Column(Integer, default=1)
    observation_type = Column(String(100))
    native = Column(Boolean, default=False)

    # Timestamps
    fetch_date = Column(DateTime, default=func.current_timestamp())
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f'<GbifData {self.scientific_name} (count: {self.observation_count})>'

    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'scientific_name': self.scientific_name,
            'observation_count': self.observation_count,
            'observation_type': self.observation_type,
            'native': self.native,
            'fetch_date': self.fetch_date.isoformat() if self.fetch_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
