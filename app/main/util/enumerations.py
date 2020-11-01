import enum


class FilteredQuestions(enum.Enum):
    films_country = 1
    ov = 2
    awarded = 3
    recent_films = 4
    tags = 5
    cast = 6
    time = 7


class QuestionOV(enum.Enum):
    ov = 1
    not_ov = 2


class QuestionAwarded(enum.Enum):
    yes = 1
    no = 2


class QuestionRecentFilms(enum.Enum):
    yes = 1
    no = 2


class TimeSpend(enum.Enum):
    t_0_90 = 1,
    t_90_120 = 2,
    t_120_180 = 3,
    t_180 = 4
