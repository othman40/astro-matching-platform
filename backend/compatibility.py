from typing import Dict, List, Optional, Tuple

from models import UserProfile


class CompatibilityCalculator:
    """
    Version 1 compatibility engine.

    Priority:
    1) 100 -> mutual Sun ↔ Ascendant opposition
    2) 98  -> one-way Sun ↔ Ascendant opposition
    3) 95  -> Sun of one person in same sign as Moon of the other
    4) 90-65 -> mirrored personal planets compatibility

    Even for 100 / 98 / 95:
    - compatible_planets and incompatible_planets are always filled
    - extra_notes explains the main challenges honestly
    """

    def __init__(self):
        self.signs = [
            "aries",
            "taurus",
            "gemini",
            "cancer",
            "leo",
            "virgo",
            "libra",
            "scorpio",
            "sagittarius",
            "capricorn",
            "aquarius",
            "pisces",
        ]

        self.sign_elements = {
            "aries": "fire",
            "leo": "fire",
            "sagittarius": "fire",
            "taurus": "earth",
            "virgo": "earth",
            "capricorn": "earth",
            "gemini": "air",
            "libra": "air",
            "aquarius": "air",
            "cancer": "water",
            "scorpio": "water",
            "pisces": "water",
        }

        self.personal_planets = [
            "sun",
            "moon",
            "mercury",
            "venus",
            "mars",
            "jupiter",
            "saturn",
        ]

        self.planet_meaning_notes = {
            "sun": "اختلاف بالروح والهوية والصورة الداخلية",
            "moon": "اختلاف بالعقلية والمشاعر الداخلية",
            "mercury": "تحديات على مستوى التواصل والتفكير",
            "venus": "اختلافات ذوقية وعاطفية",
            "mars": "تحديات على مستوى الطاقة والغضب",
            "jupiter": "اختلاف بالمبادئ والصورة العامة",
            "saturn": "اختلاف بخصوص الانضباط والصرامة",
        }

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def normalize_sign(self, sign: Optional[str]) -> Optional[str]:
        if not sign:
            return None
        sign = str(sign).strip().lower()
        return sign if sign in self.signs else None

    def get_sign_element(self, sign: Optional[str]) -> Optional[str]:
        sign = self.normalize_sign(sign)
        if not sign:
            return None
        return self.sign_elements.get(sign)

    def is_same_sign(self, sign1: Optional[str], sign2: Optional[str]) -> bool:
        sign1 = self.normalize_sign(sign1)
        sign2 = self.normalize_sign(sign2)
        return bool(sign1 and sign2 and sign1 == sign2)

    def is_opposite_sign(self, sign1: Optional[str], sign2: Optional[str]) -> bool:
        sign1 = self.normalize_sign(sign1)
        sign2 = self.normalize_sign(sign2)

        if not sign1 or not sign2:
            return False

        opposites = {
            "aries": "libra",
            "taurus": "scorpio",
            "gemini": "sagittarius",
            "cancer": "capricorn",
            "leo": "aquarius",
            "virgo": "pisces",
            "libra": "aries",
            "scorpio": "taurus",
            "sagittarius": "gemini",
            "capricorn": "cancer",
            "aquarius": "leo",
            "pisces": "virgo",
        }

        return opposites.get(sign1) == sign2

    def are_elements_compatible(self, sign1: Optional[str], sign2: Optional[str]) -> bool:
        """
        Compatible if:
        - same element
        - fire + air
        - earth + water
        """
        e1 = self.get_sign_element(sign1)
        e2 = self.get_sign_element(sign2)

        if not e1 or not e2:
            return False

        if e1 == e2:
            return True

        pair = {e1, e2}
        return pair == {"fire", "air"} or pair == {"earth", "water"}

    # --------------------------------------------------
    # Data extraction
    # --------------------------------------------------

    def get_user_sign_data(self, user: UserProfile) -> Dict[str, Optional[str]]:
        return {
            "sun": self.normalize_sign(getattr(user, "sun_sign", None)),
            "moon": self.normalize_sign(getattr(user, "moon_sign", None)),
            "mercury": self.normalize_sign(getattr(user, "mercury_sign", None)),
            "venus": self.normalize_sign(getattr(user, "venus_sign", None)),
            "mars": self.normalize_sign(getattr(user, "mars_sign", None)),
            "jupiter": self.normalize_sign(getattr(user, "jupiter_sign", None)),
            "saturn": self.normalize_sign(getattr(user, "saturn_sign", None)),
            "ascendant": self.normalize_sign(
                getattr(user, "ascendant", None) or getattr(user, "ascendant_sign", None)
            ),
        }

    # --------------------------------------------------
    # Main priority rules
    # --------------------------------------------------

    def check_mutual_sun_asc_opposition(
        self, user1_data: Dict[str, Optional[str]], user2_data: Dict[str, Optional[str]]
    ) -> bool:
        return (
            self.is_opposite_sign(user1_data.get("sun"), user2_data.get("ascendant"))
            and self.is_opposite_sign(user2_data.get("sun"), user1_data.get("ascendant"))
        )

    def check_one_way_sun_asc_opposition(
        self, user1_data: Dict[str, Optional[str]], user2_data: Dict[str, Optional[str]]
    ) -> bool:
        forward = self.is_opposite_sign(user1_data.get("sun"), user2_data.get("ascendant"))
        backward = self.is_opposite_sign(user2_data.get("sun"), user1_data.get("ascendant"))
        return (forward or backward) and not (forward and backward)

    def check_sun_moon_same_sign(
        self, user1_data: Dict[str, Optional[str]], user2_data: Dict[str, Optional[str]]
    ) -> bool:
        return (
            self.is_same_sign(user1_data.get("sun"), user2_data.get("moon"))
            or self.is_same_sign(user2_data.get("sun"), user1_data.get("moon"))
        )

    def check_moon_moon_same_sign(
        self, user1_data: Dict[str, Optional[str]], user2_data: Dict[str, Optional[str]]
    ) -> bool:
        return self.is_same_sign(user1_data.get("moon"), user2_data.get("moon"))

    # --------------------------------------------------
    # Mirrored personal planets
    # --------------------------------------------------

    def calculate_personal_planet_matches(
        self, user1_data: Dict[str, Optional[str]], user2_data: Dict[str, Optional[str]]
    ) -> Tuple[int, List[str], List[str], List[str]]:
        compatible = []
        incompatible = []
        missing = []

        for planet in self.personal_planets:
            sign1 = user1_data.get(planet)
            sign2 = user2_data.get(planet)

            if not sign1 or not sign2:
                missing.append(planet)
                incompatible.append(planet)
                continue

            if self.are_elements_compatible(sign1, sign2):
                compatible.append(planet)
            else:
                incompatible.append(planet)

        compatible_count = len(compatible)

        if compatible_count >= 7:
            score = 90
        elif compatible_count == 6:
            score = 85
        elif compatible_count == 5:
            score = 80
        elif compatible_count == 4:
            score = 75
        elif compatible_count == 3:
            score = 70
        else:
            score = 65

        return score, compatible, incompatible, missing

    # --------------------------------------------------
    # Notes and labels
    # --------------------------------------------------

    def prettify_planet_name(self, planet: str) -> str:
        names = {
            "sun": "الشمس",
            "moon": "القمر",
            "mercury": "عطارد",
            "venus": "الزهرة",
            "mars": "المريخ",
            "jupiter": "المشتري",
            "saturn": "زحل",
        }
        return names.get(planet, planet)

    def planets_list_ar(self, planets: List[str]) -> str:
        if not planets:
            return "لا يوجد"
        return "، ".join(self.prettify_planet_name(p) for p in planets)

    def build_main_report(
        self,
        score: float,
        category: str,
        compatible_planets: List[str],
        incompatible_planets: List[str],
    ) -> str:
        if category == "mutual_sun_asc":
            return (
                "علاقة مكملة لبعضها، علاقة قوية جدًا، ويمكن اعتبارها نصفك الثاني. "
                "السبب هو وجود تقابل متبادل بين الشمس والطالع عند الطرفين."
            )

        if category == "one_way_sun_asc":
            return (
                "علاقة حب غير كاملة، يوجد جذب قوي وواضح، لكن هذا الجذب ليس متبادلًا بالكامل "
                "لأن تقابل الشمس والطالع موجود باتجاه واحد فقط."
            )

        if category == "sun_moon_same_sign":
            return (
                "انسجام عاطفي قوي جدًا بسبب وجود الشمس عند أحد الطرفين مع القمر عند الطرف الآخر "
                "في نفس البرج. هذه من أقوى العلاقات بعد علاقة الشمس والطالع المتبادلة."
            )

        if category == "personal_planets":
            if score == 90:
                return "توافق جيد جدًا، كل الكواكب الشخصية المتناظرة متوافقة."
            if score == 85:
                return (
                    f"توافق جيد، أغلب الكواكب الشخصية متوافقة. "
                    f"الكواكب المتوافقة: {self.planets_list_ar(compatible_planets)}. "
                    f"غير المتوافق: {self.planets_list_ar(incompatible_planets)}."
                )
            if score == 80:
                return (
                    f"توافق جيد، يوجد تشابه واضح بينكما. "
                    f"الكواكب المتوافقة: {self.planets_list_ar(compatible_planets)}. "
                    f"غير المتوافق: {self.planets_list_ar(incompatible_planets)}."
                )
            if score == 75:
                return (
                    f"توافق متوسط مائل للجيد. "
                    f"الكواكب المتوافقة: {self.planets_list_ar(compatible_planets)}. "
                    f"غير المتوافق: {self.planets_list_ar(incompatible_planets)}."
                )
            if score == 70:
                return (
                    f"يوجد بعض الانسجام، لكن هناك اختلافات واضحة. "
                    f"الكواكب المتوافقة: {self.planets_list_ar(compatible_planets)}. "
                    f"غير المتوافق: {self.planets_list_ar(incompatible_planets)}."
                )

            return (
                f"علاقة صعبة، شخصان مختلفان تمامًا. "
                f"الكواكب المتوافقة: {self.planets_list_ar(compatible_planets)}. "
                f"غير المتوافق: {self.planets_list_ar(incompatible_planets)}."
            )

        return "تقرير التوافق غير متوفر."

    def build_extra_notes(
        self,
        user1_data: Dict[str, Optional[str]],
        user2_data: Dict[str, Optional[str]],
        incompatible_planets: List[str],
    ) -> List[str]:
        notes = []

        if self.check_moon_moon_same_sign(user1_data, user2_data):
            notes.append(
                "علاقة صداقة وارتياح نفسي واضحة بسبب وجود القمرين في نفس البرج."
            )

        # add honest challenge notes based on incompatible planets
        for planet in incompatible_planets:
            note = self.planet_meaning_notes.get(planet)
            if note and note not in notes:
                notes.append(note)

        return notes

    def get_match_label(self, score: float) -> str:
        if score == 100:
            return "soulmate_match"
        if score == 98:
            return "strong_incomplete_love"
        if score == 95:
            return "strong_emotional_union"
        if score == 90:
            return "very_good_compatibility"
        if score == 85:
            return "good_compatibility"
        if score == 80:
            return "good_similarity"
        if score == 75:
            return "moderate_compatibility"
        if score == 70:
            return "mixed_compatibility"
        return "difficult_relationship"

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def calculate_overall_compatibility(
        self, user1: UserProfile, user2: UserProfile
    ) -> Tuple[float, Dict]:
        user1_data = self.get_user_sign_data(user1)
        user2_data = self.get_user_sign_data(user2)

        # always compute mirrored planets for honesty and detail
        mirrored_score, compatible_planets, incompatible_planets, missing_planets = (
            self.calculate_personal_planet_matches(user1_data, user2_data)
        )

        # main priority score
        if self.check_mutual_sun_asc_opposition(user1_data, user2_data):
            score = 100.0
            category = "mutual_sun_asc"

        elif self.check_one_way_sun_asc_opposition(user1_data, user2_data):
            score = 98.0
            category = "one_way_sun_asc"

        elif self.check_sun_moon_same_sign(user1_data, user2_data):
            score = 95.0
            category = "sun_moon_same_sign"

        else:
            score = float(mirrored_score)
            category = "personal_planets"

        report_text = self.build_main_report(
            score=score,
            category=category,
            compatible_planets=compatible_planets,
            incompatible_planets=incompatible_planets,
        )

        extra_notes = self.build_extra_notes(
            user1_data=user1_data,
            user2_data=user2_data,
            incompatible_planets=incompatible_planets,
        )

        details = {
            "overall_score": score,
            "match_label": self.get_match_label(score),
            "category": category,
            "report_text": report_text,
            "extra_notes": extra_notes,
            "compatible_planets": compatible_planets,
            "incompatible_planets": incompatible_planets,
            "missing_planets": missing_planets,
            "user1_signs": user1_data,
            "user2_signs": user2_data,
        }

        return score, details

    def find_matches(
        self,
        current_user: UserProfile,
        all_users: List[UserProfile],
        limit: int = 10,
    ) -> List[Dict]:
        matches = []

        for user in all_users:
            if user.id == current_user.id:
                continue

            score, details = self.calculate_overall_compatibility(current_user, user)

            matches.append(
                {
                    "user_id": user.id,
                    "name": user.name,
                    "compatibility_score": score,
                    "match_label": details["match_label"],
                    "details": details,
                }
            )

        matches.sort(key=lambda item: item["compatibility_score"], reverse=True)
        return matches[:limit]