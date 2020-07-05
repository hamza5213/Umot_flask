import enum


class FilteredQuestions(enum.Enum):
    films_country = 1
    ov = 2
    awarded = 3
    recent_films = 4
    tags = 5
    cast = 6


class QuestionOV(enum.Enum):
    ov = 1
    not_ov = 2


class QuestionAwarded(enum.Enum):
    yes = 1
    no = 2


class QuestionRecentFilms(enum.Enum):
    yes = 1
    no = 2
