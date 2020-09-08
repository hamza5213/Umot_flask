import copy
import datetime
import json
import random

from app.main.model.answers import Answers
from app.main.model.genre_scores import GenreScores
from app.main.model.movie_raw_complete import MovieRawComplete, AwardsCount
from app.main.model.questions import Questions
from app.main.model.recommendations import Recommendations
from app.main.model.user_rating import UserRating
from app.main.service.db_operations import add_to_db
from app.main.util.enumerations import FilteredQuestions, QuestionOV, QuestionAwarded, QuestionRecentFilms


def get_questions_list(locale):
    banned_question = [6, 7, 22, 23, 24, 25, 32, 33]
    questions = Questions.query.order_by(Questions.group).all()
    questions = list(filter((lambda x: x.locale == locale and x.id not in banned_question), questions))
    questions = get_by_group(questions)
    questions = get_prepared_question_list(questions)
    qas = get_answers_list(questions)
    return qas


def get_by_group(questions):
    return list(filter((lambda x: x.group == 0), questions)), list(filter((lambda x: x.group == 1), questions)), \
           list(filter((lambda x: x.group == 2), questions)), list(filter((lambda x: x.group == 3), questions))


def get_random_ele(arr, size):
    random.seed(datetime.datetime.now())
    indexes = random.sample(range(0, len(arr)), size)
    return [arr[index] for index in indexes]


def get_prepared_question_list(questions):
    group0 = questions[0]
    group1 = get_random_ele(questions[1], 2)
    group2 = get_random_ele(questions[2], 1)
    group3 = get_random_ele(questions[3], 1)

    return group0 + group1 + group2 + group3


def get_answers_list(questions):
    question_ids = [question.id for question in questions]
    answers = Answers.query.filter(Answers.question_id.in_(question_ids))
    qas = {}

    for answer in answers:
        if answer.question_id not in qas:
            qas[answer.question_id] = [{'text': answer.text,
                                        'value': answer.value,
                                        'answer_id': answer.id}]
        else:
            qas[answer.question_id].append({'text': answer.text,
                                            'value': answer.value,
                                            'answer_id': answer.id})

    final_list = []
    for question in questions:
        final_list.append({
            'question_id': question.id,
            'text': question.text,
            'value': question.value,
            'group': question.group,
            'answers': qas[question.id] if question.id in qas else None
        })

    return final_list


def get_questions(question_ids):
    questions = Questions.query.filter(Questions.id.in_(question_ids)).all()
    return {question.id: question for question in questions}


def get_answers(answers_ids):
    answers = Answers.query.filter(Answers.id.in_(answers_ids)).all()
    return {answer.id: answer for answer in answers}


def update_response(response):
    question_ids, answer_ids = [], []
    for ele in response:
        question_ids.append(ele['question_id'])
        if ele["answer_id"] != None:
            answer_ids.append(ele['answer_id'])
    questions = get_questions(question_ids)
    answers = get_answers(answer_ids)

    for ele in response:
        ele['question'] = questions[ele['question_id']]
        ele['answer'] = answers[ele['answer_id']] if ele["answer_id"] != None else None

    return response


def submit_response(response, locale, user_id=1):
    updated_response = update_response(copy.deepcopy(response))
    filter_question = list(filter((lambda x: x['question'].category == 'fitered'), updated_response))
    calculated_question = list(filter((lambda x: x['question'].category == 'calculated'), updated_response))

    query = get_query(filter_question, locale)
    filtered_movies = query.order_by(MovieRawComplete.vote_count.desc()).limit(500).all()
    total_score = get_genre_scores(calculated_question)
    recommendations = get_recommendation(total_score, filtered_movies)
    submit_recommendations(user_id, response, recommendations)


def submit_recommendations(user_id, response, movies):
    recommendation = Recommendations()
    recommendation.movies = ','.join([str(i) for i in movies])
    recommendation.user_id = user_id
    recommendation.question_response = json.dumps(response)
    recommendation.created_on = datetime.datetime.now()
    add_to_db(recommendation)


def get_recommendations(user_id=1):
    watched = UserRating.query.filter_by(user_id=user_id).all()
    watched_movies = [watched_movie.movie_id for watched_movie in watched]

    recommendation = Recommendations.query.filter(Recommendations.user_id == user_id).order_by(
        Recommendations.created_on.desc()).first()
    if recommendation != None and recommendation.movies != "":
        recommendation_movies = list(map(int, recommendation.movies.split(',')))
        # res = list(set(recommendation_movies) ^ set(watched_movies))
        for movie in watched_movies:
            if movie in recommendation_movies:
                index = recommendation_movies.index(movie)
                recommendation_movies.pop(index)
        return recommendation_movies
    else:
        return "no record found"


def get_genre_scores(questions):
    answer_ids = [question["answer_id"] for question in questions]
    genre_scores = GenreScores.query.filter(GenreScores.answer_id.in_(answer_ids)).all()
    total_scores = {}
    # TODO to be replaced by db list
    genres = ['comedy', 'drama', 'horror', 'action', 'fantasy', 'film_noir', 'animation', 'western', 'documentary',
              'thriller',
              'adventure', 'war', 'sci_fi', 'biography', 'crime', 'romance', 'mystery', 'history', 'family',
              'sport', 'musical', 'music', 'adult', 'news', 'game_show']
    for score in genre_scores:
        for genre in genres:
            if genre not in total_scores:
                total_scores[genre] = 0
            total_scores[genre] += getattr(score, genre)

    # normalize
    for genre in genres:
        total_scores[genre] = (total_scores[genre]) * 1.0 / len(answer_ids)

    return total_scores


def get_query(filter_question, locale):
    query = MovieRawComplete.query.filter(MovieRawComplete.release_date_c != '0001-01-01 BC')

    for ele in filter_question:
        if ele['question'].value == FilteredQuestions.ov.value:
            if ele['answer'].value == QuestionOV.ov.value:
                query = query.filter(MovieRawComplete.original_language == locale)


        elif ele['question'].value == FilteredQuestions.awarded.value:
            if ele['answer'].value == QuestionAwarded.yes.value:
                query = query.join(AwardsCount).filter(AwardsCount.count != 0)
            elif ele['answer'].value == QuestionAwarded.no.value:
                query = query.join(AwardsCount).filter(AwardsCount.count == 0)

        elif ele['question'].value == FilteredQuestions.tags.value:
            query = query.filter(MovieRawComplete.keywords_json.contains({'keywords': [{"id": int(ele['extra'])}]}))

        elif ele['question'].value == FilteredQuestions.cast.value:
            query = query.filter(MovieRawComplete.credits_json.contains({'cast': [{"id": int(ele['extra'])}]}))

        elif ele['question'].value == FilteredQuestions.recent_films.value:
            if ele['answer'].value == QuestionRecentFilms.yes.value:
                query = query.filter(MovieRawComplete.release_date_c > '2018-01-01')
                # query = query.order_by(MovieRawComplete.release_date_c.desc())
            elif ele['answer'].value == QuestionRecentFilms.no.value:
                query = query.filter(MovieRawComplete.release_date_c < '2010-01-01')
                # query = query.order_by(MovieRawComplete.release_date_c)
    return query


# TODO name change
def get_recommendation(total_scores, filtered_movies):
    movie_scores = {}
    for movie in filtered_movies:
        if movie == None:
            continue
        score = 0
        if len(movie.movie_imdb_genres) > 0:
            for genre in movie.movie_imdb_genres:
                key = genre.name.lower()
                score += total_scores[key] if key in total_scores else 0
        else:
            for genre in json.loads(movie.genres):
                key = genre["name"].lower()
                score += total_scores[key] if key in total_scores else 0
        movie_scores[movie.tmdb_id] = score
    movie_scores = {k: v for k, v in sorted(movie_scores.items(), key=lambda item: item[1], reverse=True)}
    result = list(movie_scores.keys())
    return result if len(result) <= 300 else result[:300]


def test():
    # t = MovieRawComplete.query.filter(MovieRawComplete.spoken_languages_json.contains([{"iso_639_1": "en"}])).first()
    # t = MovieRawComplete.query.filter(MovieRawComplete.credits_json.contains({'cast':[{"name": "Joaquin Phoenix"}]})).first()
    t = MovieRawComplete.query.join(AwardsCount).filter(AwardsCount.count == 1).first()
    print('g')
