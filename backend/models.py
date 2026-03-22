from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class BirthDataInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    gender: Optional[str] = Field(default=None, max_length=20)
    birth_date: str
    birth_time: str
    birth_city: str


class PlanetPosition(BaseModel):
    name: str
    sign: str
    degree: Optional[float] = None
    house: Optional[int] = None


class UserProfileBase(BaseModel):
    name: str
    gender: Optional[str] = None
    birth_date: str
    birth_time: str
    birth_city: str

    sun_sign: Optional[str] = None
    moon_sign: Optional[str] = None
    mercury_sign: Optional[str] = None
    venus_sign: Optional[str] = None
    mars_sign: Optional[str] = None
    jupiter_sign: Optional[str] = None
    saturn_sign: Optional[str] = None

    ascendant: Optional[str] = None
    ascendant_sign: Optional[str] = None

    planetary_positions: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfile(UserProfileBase):
    id: int

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    id: int
    name: str
    gender: Optional[str] = None
    birth_date: str
    birth_time: str
    birth_city: str

    sun_sign: Optional[str] = None
    moon_sign: Optional[str] = None
    mercury_sign: Optional[str] = None
    venus_sign: Optional[str] = None
    mars_sign: Optional[str] = None
    jupiter_sign: Optional[str] = None
    saturn_sign: Optional[str] = None

    ascendant: Optional[str] = None
    ascendant_sign: Optional[str] = None

    planetary_positions: Optional[List[PlanetPosition]] = None

    class Config:
        from_attributes = True


class CompatibilityDetails(BaseModel):
    overall_score: float
    match_label: str
    category: str
    report_text: str
    extra_notes: List[str] = []
    compatible_planets: List[str] = []
    incompatible_planets: List[str] = []
    missing_planets: List[str] = []
    user1_signs: Dict[str, Optional[str]] = {}
    user2_signs: Dict[str, Optional[str]] = {}


class MatchResult(BaseModel):
    user_id: int
    name: str
    compatibility_score: float
    match_label: str
    details: CompatibilityDetails