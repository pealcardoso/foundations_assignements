import enum

class Country(enum.Enum):
    """
    Enum class of the possible countries
    """
    AT='AT'
    BE='BE'
    BG='BG'
    CH='CH'
    CY='CY'
    CZ='CZ'
    DK='DK'
    EE='EE'
    EL='EL'
    ES='ES'
    FI='FI'
    FR='FR'
    HR='HR'
    HU='HU'
    IS='IS'
    IT='IT'
    LI='LI'
    LT='LT'
    LU='LU'
    LV='LV'
    MT='MT'
    NL='NL'
    NO='NO'
    PL='PL'
    PT='PT'
    RO='RO'
    SE='SE'
    SI='SI'
    SK='SK'
    DE='DE'
    AL='AL'
    IE='IE'
    ME='ME'
    MK='MK'
    RS='RS'
    AM='AM'
    AZ='AZ'
    GE='GE'
    TR='TR'
    UA='UA'
    BY='BY'
    UK='UK'
    XK='XK'
    FX='FX'
    MD='MD'
    SM='SM'
    RU='RU'

    @classmethod
    def list_of_countries(cls):
        """
        Class method to return the list of possible countries
        """
        return [c.value for c in cls]
