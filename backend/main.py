import json
from typing import List

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from astrology_api import ProkeralaAPI
from compatibility import CompatibilityCalculator
from database import UserProfileDB, create_tables, get_db
from models import (
    BirthDataInput,
    MatchResult,
    PlanetPosition,
    UserProfileResponse,
)

load_dotenv()

app = FastAPI(title="Astro Matching Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()

compatibility_calculator = CompatibilityCalculator()
prokerala_api = ProkeralaAPI()


def db_to_response(user: UserProfileDB) -> UserProfileResponse:
    parsed_positions = []

    if user.planetary_positions:
        try:
            raw_positions = json.loads(user.planetary_positions)
            if isinstance(raw_positions, list):
                parsed_positions = [
                    PlanetPosition(**item)
                    for item in raw_positions
                    if isinstance(item, dict)
                ]
        except (json.JSONDecodeError, TypeError, ValueError):
            parsed_positions = []

    return UserProfileResponse(
        id=user.id,
        name=user.name,
        gender=user.gender,
        birth_date=user.birth_date,
        birth_time=user.birth_time,
        birth_city=user.birth_city,
        sun_sign=user.sun_sign,
        moon_sign=user.moon_sign,
        mercury_sign=user.mercury_sign,
        venus_sign=user.venus_sign,
        mars_sign=user.mars_sign,
        jupiter_sign=user.jupiter_sign,
        saturn_sign=user.saturn_sign,
        ascendant=user.ascendant,
        ascendant_sign=user.ascendant_sign,
        planetary_positions=parsed_positions,
    )


def normalize_sign(value):
    if not value:
        return None
    return str(value).strip().lower()


def extract_signs_from_provider_data(astrology_data: dict) -> dict:
    sign_map = {
        "sun_sign": normalize_sign(astrology_data.get("sun_sign")),
        "moon_sign": normalize_sign(astrology_data.get("moon_sign")),
        "mercury_sign": normalize_sign(astrology_data.get("mercury_sign")),
        "venus_sign": normalize_sign(astrology_data.get("venus_sign")),
        "mars_sign": normalize_sign(astrology_data.get("mars_sign")),
        "jupiter_sign": normalize_sign(astrology_data.get("jupiter_sign")),
        "saturn_sign": normalize_sign(astrology_data.get("saturn_sign")),
    }

    planetary_positions = astrology_data.get("planetary_positions", [])

    for item in planetary_positions:
        if not isinstance(item, dict):
            continue

        name = str(item.get("name", "")).strip().lower()
        sign = normalize_sign(item.get("sign"))

        if name == "sun" and not sign_map["sun_sign"]:
            sign_map["sun_sign"] = sign
        elif name == "moon" and not sign_map["moon_sign"]:
            sign_map["moon_sign"] = sign
        elif name == "mercury" and not sign_map["mercury_sign"]:
            sign_map["mercury_sign"] = sign
        elif name == "venus" and not sign_map["venus_sign"]:
            sign_map["venus_sign"] = sign
        elif name == "mars" and not sign_map["mars_sign"]:
            sign_map["mars_sign"] = sign
        elif name == "jupiter" and not sign_map["jupiter_sign"]:
            sign_map["jupiter_sign"] = sign
        elif name == "saturn" and not sign_map["saturn_sign"]:
            sign_map["saturn_sign"] = sign

    return sign_map


@app.get("/")
def root():
    return {"message": "Astro Matching Platform API is running"}


@app.post("/create-profile", response_model=UserProfileResponse)
async def create_profile(payload: BirthDataInput, db: Session = Depends(get_db)):
    astrology_data = await prokerala_api.get_natal_chart(
        birth_date=payload.birth_date,
        birth_time=payload.birth_time,
        birth_city=payload.birth_city,
    )

    if not astrology_data:
        raise HTTPException(
            status_code=502,
            detail="Failed to get astrology data from provider",
        )

    planetary_positions = astrology_data.get("planetary_positions", [])
    ascendant = normalize_sign(
        astrology_data.get("ascendant") or astrology_data.get("ascendant_sign")
    )

    sign_map = extract_signs_from_provider_data(astrology_data)

    user = UserProfileDB(
        name=payload.name,
        gender=payload.gender,
        birth_date=payload.birth_date,
        birth_time=payload.birth_time,
        birth_city=payload.birth_city,
        sun_sign=sign_map["sun_sign"],
        moon_sign=sign_map["moon_sign"],
        mercury_sign=sign_map["mercury_sign"],
        venus_sign=sign_map["venus_sign"],
        mars_sign=sign_map["mars_sign"],
        jupiter_sign=sign_map["jupiter_sign"],
        saturn_sign=sign_map["saturn_sign"],
        ascendant=ascendant,
        ascendant_sign=ascendant,
        planetary_positions=json.dumps(planetary_positions),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return db_to_response(user)


@app.get("/profiles", response_model=List[UserProfileResponse])
def get_profiles(db: Session = Depends(get_db)):
    users = db.query(UserProfileDB).order_by(UserProfileDB.id.desc()).all()
    return [db_to_response(user) for user in users]


@app.get("/profiles/{profile_id}", response_model=UserProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfileDB).filter(UserProfileDB.id == profile_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Profile not found")

    return db_to_response(user)


@app.get("/match/{profile_id}", response_model=List[MatchResult])
def get_matches(profile_id: int, limit: int = 10, db: Session = Depends(get_db)):
    current_user = db.query(UserProfileDB).filter(UserProfileDB.id == profile_id).first()

    if not current_user:
        raise HTTPException(status_code=404, detail="Current profile not found")

    all_users = db.query(UserProfileDB).all()

    results = compatibility_calculator.find_matches(
        current_user=current_user,
        all_users=all_users,
        limit=limit,
    )

    return results


@app.delete("/profiles/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfileDB).filter(UserProfileDB.id == profile_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(user)
    db.commit()

    return {"message": f"Profile {profile_id} deleted successfully"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "provider": "Prokerala Astrology API",
        "integration": "live astrology_api.py",
    }