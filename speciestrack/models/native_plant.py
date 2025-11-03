from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, DateTime, func
from speciestrack.models import db


class NativePlant(db.Model):
    """Model for native California plants"""

    __tablename__ = 'native_plants'

    # Primary key
    id = Column(Integer, primary_key=True)

    # Basic identification
    botanical_name = Column(String(255), unique=True, nullable=False)
    common_name = Column(String(255))
    other_names = Column(Text)
    alternative_common_names = Column(Text)
    obsolete_names = Column(Text)

    # Plant classification
    plant_type = Column(String(255))
    form = Column(String(255))
    is_cultivar = Column(Boolean, default=False)
    rarity = Column(String(255))

    # Wildlife support
    butterflies_and_moths_supported = Column(Text)
    attracts_wildlife = Column(Text)

    # Physical characteristics
    height = Column(Text)
    width = Column(Text)
    height_min = Column(Numeric(10, 2))
    height_max = Column(Numeric(10, 2))
    width_min = Column(Numeric(10, 2))
    width_max = Column(Numeric(10, 2))
    growth_rate = Column(String(255))
    seasonality = Column(String(255))

    # Flowers
    flower_color = Column(String(255))
    flowering_season = Column(String(255))
    fragrance = Column(String(255))

    # Growing conditions
    sun = Column(String(255))
    soil_drainage = Column(String(255))
    water_requirement = Column(String(255))
    summer_irrigation = Column(String(255))
    ease_of_care = Column(String(255))

    # Soil
    soil = Column(Text)
    soil_texture = Column(String(255))
    soil_ph = Column(String(255))
    soil_toxicity = Column(String(255))
    mulch = Column(Text)

    # Site and environment
    site_type = Column(String(255))
    elevation_min = Column(Integer)
    elevation_max = Column(Integer)
    rainfall_min = Column(Numeric(10, 2))
    rainfall_max = Column(Numeric(10, 2))

    # Geographic zones
    hardiness = Column(String(255))
    sunset_zones = Column(String(255))

    # Plant communities
    communities_simplified = Column(Text)
    communities = Column(Text)

    # Availability and companions
    nursery_availability = Column(String(255))
    companions = Column(Text)

    # Uses and care
    special_uses = Column(Text)
    tips = Column(Text)
    pests = Column(Text)
    propagation = Column(Text)

    # External resources
    jepson_link = Column(String(500))
    plant_url = Column(String(500))
    qr_codes = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f'<NativePlant {self.botanical_name} ({self.common_name})>'

    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'botanical_name': self.botanical_name,
            'common_name': self.common_name,
            'plant_type': self.plant_type,
            'form': self.form,
            'butterflies_and_moths_supported': self.butterflies_and_moths_supported,
            'attracts_wildlife': self.attracts_wildlife,
            'height': self.height,
            'width': self.width,
            'height_min': float(self.height_min) if self.height_min else None,
            'height_max': float(self.height_max) if self.height_max else None,
            'width_min': float(self.width_min) if self.width_min else None,
            'width_max': float(self.width_max) if self.width_max else None,
            'growth_rate': self.growth_rate,
            'seasonality': self.seasonality,
            'flower_color': self.flower_color,
            'flowering_season': self.flowering_season,
            'fragrance': self.fragrance,
            'sun': self.sun,
            'soil_drainage': self.soil_drainage,
            'water_requirement': self.water_requirement,
            'summer_irrigation': self.summer_irrigation,
            'ease_of_care': self.ease_of_care,
            'soil': self.soil,
            'soil_texture': self.soil_texture,
            'soil_ph': self.soil_ph,
            'soil_toxicity': self.soil_toxicity,
            'mulch': self.mulch,
            'site_type': self.site_type,
            'elevation_min': self.elevation_min,
            'elevation_max': self.elevation_max,
            'rainfall_min': float(self.rainfall_min) if self.rainfall_min else None,
            'rainfall_max': float(self.rainfall_max) if self.rainfall_max else None,
            'hardiness': self.hardiness,
            'sunset_zones': self.sunset_zones,
            'communities_simplified': self.communities_simplified,
            'communities': self.communities,
            'nursery_availability': self.nursery_availability,
            'companions': self.companions,
            'special_uses': self.special_uses,
            'tips': self.tips,
            'pests': self.pests,
            'propagation': self.propagation,
            'other_names': self.other_names,
            'alternative_common_names': self.alternative_common_names,
            'obsolete_names': self.obsolete_names,
            'rarity': self.rarity,
            'is_cultivar': self.is_cultivar,
            'jepson_link': self.jepson_link,
            'plant_url': self.plant_url,
            'qr_codes': self.qr_codes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
