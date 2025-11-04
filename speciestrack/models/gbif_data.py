from sqlalchemy import Column, Integer, String, Boolean, Numeric, DateTime, func
from speciestrack.models import db


class GbifData(db.Model):
    """Model for GBIF species observation data"""

    __tablename__ = 'gbif_data'

    # Primary key
    id = Column(Integer, primary_key=True)

    # Observation data
    scientific_name = Column(String(500), nullable=False)
    common_name = Column(String(255))
    observation_count = Column(Integer, default=1)
    observation_type = Column(String(100))
    native = Column(Boolean, default=False)
    decimal_latitude = Column(Numeric(10, 8))  # Allows -90 to +90 with 8 decimal precision
    decimal_longitude = Column(Numeric(11, 8))  # Allows -180 to +180 with 8 decimal precision

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
            'common_name': self.common_name,
            'observation_count': self.observation_count,
            'observation_type': self.observation_type,
            'native': self.native,
            'decimal_latitude': float(self.decimal_latitude) if self.decimal_latitude else None,
            'decimal_longitude': float(self.decimal_longitude) if self.decimal_longitude else None,
            'fetch_date': self.fetch_date.isoformat() if self.fetch_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
