import io
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from collections import namedtuple
from matplotlib.legend_handler import HandlerPatch
import matplotlib.patches as mpatches
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

engine = create_engine('postgresql://admin:36WiUDeHRxUUDj9@134.209.250.123/tutorappserver')


@api_view(['GET'])
def experience_dashboard(request):
    query_experience = "SELECT skill_group, count(*) FROM (SELECT CASE WHEN experience = 'Нет опыта' THEN 'Нет опыта' WHEN experience = 'До 3 лет' THEN 'До 3 лет' WHEN experience = 'От 3 до 5 лет' THEN 'От 3 лет до 5 лет' ELSE 'Больше' END skill_group FROM public.tutorapp_customuser WHERE role = 'teacher') AS subquery GROUP BY skill_group ORDER BY CASE WHEN skill_group = 'Больше' THEN 4 WHEN skill_group = 'От 3 лет до 5 лет' THEN 3 WHEN skill_group = 'До 3 лет' THEN 2 ELSE 1 END;"

    result_experience = pd.read_sql(query_experience, engine)

    x = result_experience['skill_group']
    y = result_experience['count']

    plt.figure(figsize=(8, 6), facecolor='#FFFFFF')
    ax = plt.gca()
    plt.plot(x, y, marker='o', linestyle='-', color='#252641')

    for i, (xi, yi) in enumerate(zip(x, y)):
        plt.annotate(f'({yi})', (xi, yi), textcoords="offset points", xytext=(0, 10), ha='center')

    ax.set_facecolor('#FFFFFF')

    plt.title('Статистика опыта работы наших репетитеров',
              fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontfamily': 'serif'})
    plt.xlabel('Опыт')
    plt.ylabel('Лет')

    plt.grid(True)

    # plt.show()

    svg_buffer = io.BytesIO()
    plt.savefig(svg_buffer, format='svg')
    svg_buffer.seek(0)
    svg_data = svg_buffer.getvalue()

    plt.close()

    return HttpResponse(svg_data, content_type='image/svg+xml', status=status.HTTP_200_OK)


@api_view(['GET'])
def age_dashboard(request):
    query_age = "select age_count, count(*) from(select case when age>=18 and age<=23 then '18-20 лет'when age>=24 and age<=29 then '24-29 лет'when age>=30 and age<=35 then '30-35 лет'when age>=36 and age>=41 then '36-41 лет'when age>=42 and age<=47 then '42-47 лет'when age>=48 and age<=53 then '48-53 лет'when age>=54 and age<=59 then '54-59 лет' else '60+ лет'end age_count from public.tutorapp_customuser where role = 'teacher') group by age_count order by age_count;"
    result_age = pd.read_sql(query_age, engine)

    plt.figure(figsize=(8, 6), facecolor='#FFFFFF')
    ax = plt.gca()
    plt.barh(result_age['age_count'], result_age['count'], color='#252641')
    ax.set_facecolor('#FFFFFF')
    plt.title('Статистика возрастов наших репетиторов',
              fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontfamily': 'serif'})
    plt.xlabel('Число')
    plt.ylabel('Возраст')
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    # plt.show()

    svg_buffer = io.BytesIO()
    plt.savefig(svg_buffer, format='svg')
    svg_buffer.seek(0)
    svg_data = svg_buffer.getvalue()

    plt.close()

    return HttpResponse(svg_data, content_type='image/svg+xml', status=status.HTTP_200_OK)


@api_view(['GET'])
def city_dashboard(request):
    query_city = " SELECT city, count(*) as count FROM public.tutorapp_customuser where role='teacher' group by city ORDER BY count DESC limit 15"
    result_city = pd.read_sql(query_city, engine)

    colors = ['#EDB62E', '#DFAC30', '#D1A232', '#C29833', '#B48E34', '#A68436', '#987A38', '#8A7039',
              '#7C653A', '#6E5B3C', '#60513E', '#60513E', '#433D40', '#353342', '#272944']
    plt.figure(figsize=(8, 6), facecolor='#FFFFFF')
    plt.pie(result_city['count'], autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title('Из каких городов наши репетиторы',
              fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontfamily': 'serif'})
    plt.axis('equal')

    legend_labels = list(result_city['city'])
    legend_colors = colors[:len(result_city)]

    class HandlerCircle(HandlerPatch):
        def create_artists(self, legend, orig_handle,
                           xdescent, ydescent, width, height,
                           fontsize, trans):

            center = 0.5 * width - 0.5 * xdescent, 0.5 * height - 0.5 * ydescent
            p = mpatches.Circle(xy=center, radius=min(width, height) / 2)
            self.update_prop(p, orig_handle, legend)
            p.set_transform(trans)
            return [p]


    plt.legend(handles=[mpatches.Patch(color=color) for color in legend_colors],
            labels=legend_labels, loc="lower right", fontsize='small', title="Курсы",
            handler_map={mpatches.Patch: HandlerCircle()})

    #plt.show()

    svg_buffer = io.BytesIO()
    plt.savefig(svg_buffer, format='svg')
    svg_buffer.seek(0)
    svg_data = svg_buffer.getvalue()

    plt.close()

    return HttpResponse(svg_data, content_type='image/svg+xml', status=status.HTTP_200_OK)


@api_view(['GET'])
def count_courses_student_dashboard(request):
    query_countStuOfCourse = "SELECT course.name as name, count(stu.student_id_id) as count FROM public.tutorapp_coursestudent stu left join public.tutorapp_course course on course.id =stu.course_id_id group by course.name order by count DESC limit 5"
    result_countStuOfCourse = pd.read_sql(query_countStuOfCourse, engine)

    colors = ['#191F45', '#272C94', '#475BB7', '#526DF0', '#93A5FD']
    explode = (0.05, 0.05, 0.05, 0.05, 0.05)

    plt.figure(facecolor='#FFFFFF')

    plt.pie(result_countStuOfCourse['count'], colors=colors, pctdistance=0.85, explode=explode)

    centre_circle = plt.Circle((0, 0), 0.70, fc='#FFFFFF')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.title('Курсы с наибольшим количеством студентов',
               fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontfamily': 'serif'})

    legend_labels = [f"{name} - {percent:.1f}%"
                      for name, percent in zip(result_countStuOfCourse['name'],
                                               result_countStuOfCourse['count'] / result_countStuOfCourse[
                                                   'count'].sum() * 100)]
    legend_colors = colors[:len(result_countStuOfCourse)]


    class HandlerCircle(HandlerPatch):
         def create_artists(self, legend, orig_handle,
                            xdescent, ydescent, width, height,
                            fontsize, trans):
             center = 0.5 * width - 0.5 * xdescent, 0.5 * height - 0.5 * ydescent
             p = mpatches.Circle(xy=center, radius=min(width, height) / 2)
             self.update_prop(p, orig_handle, legend)
             p.set_transform(trans)
             return [p]


    plt.legend(handles=[mpatches.Patch(color=color) for color in legend_colors],
               labels=legend_labels, loc="lower right", fontsize='small', title="Курсы",
               handler_map={mpatches.Patch: HandlerCircle()})

    # plt.show()
    svg_buffer = io.BytesIO()
    plt.savefig(svg_buffer, format='svg')
    svg_buffer.seek(0)
    svg_data = svg_buffer.getvalue()

    plt.close()

    return HttpResponse(svg_data, content_type='image/svg+xml', status=status.HTTP_200_OK)


Course = namedtuple('Course', ['name', 'rating'])
Score = namedtuple('Score', ['value'])


def fetch_course_data():
    query = "SELECT course.name as name, ROUND(AVG(rating), 1) as rating FROM public.tutorapp_courserating rate left join public.tutorapp_course course on course.id =rate.course_id_id group by course.name ORDER BY rating DESC limit 3;"
    course_data = pd.read_sql_query(query, engine)
    if not course_data.empty:
        course_row = course_data.iloc[0]
        course = Course(name=course_row['name'], rating=course_row['rating'])
        return course
    else:
        return None


def fetch_scores():
    result_best_course = pd.read_sql(
        "SELECT course.name as name, ROUND(AVG(rating), 1) as avg_rating FROM public.tutorapp_courserating rate left join public.tutorapp_course course on course.id =rate.course_id_id group by course.name ORDER BY avg_rating DESC limit 3;",
        engine)

    scores_by_test = {}
    for index, row in result_best_course.iterrows():
        course_name = row['name']
        avg_rating = row['avg_rating']
        scores_by_test[course_name] = Score(value=avg_rating)

    return scores_by_test


def plot_course_results(course, scores_by_test, cohort_size):
    plt.figure(figsize=(8, 6), facecolor='#FFFFFF')
    ax = plt.gca()

    bars = plt.bar(list(scores_by_test.keys()), [score.value for score in scores_by_test.values()], color='#F5C400')

    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(bar.get_height()), ha='center', va='bottom')

    ax.set_facecolor('#FFFFFF')

    legend_labels = [f"Top {i + 1}: {course} - {scores_by_test[course].value}" for i, course in
                     enumerate(scores_by_test.keys())]
    plt.legend(bars, legend_labels, loc='upper right', handlelength=1.5)

    plt.xlabel('Название курса')
    plt.ylabel('Средний рейтинг')
    plt.title('Топ 3 курса по среднему рейтингу',
              fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontfamily': 'serif'})

    #plt.show()


@api_view(['GET'])
def top_courses(request):
    Course = fetch_course_data()
    scores_by_test = fetch_scores()
    plot_course_results(Course, scores_by_test, cohort_size=62)

    svg_buffer = io.BytesIO()
    plt.savefig(svg_buffer, format='svg')
    svg_buffer.seek(0)
    svg_data = svg_buffer.getvalue()

    plt.close()

    return HttpResponse(svg_data, content_type='image/svg+xml', status=status.HTTP_200_OK)


@api_view(['GET'])
def number_of_users_dashboard(request):
    query_userCounter = "SELECT TO_CHAR(date_joined, 'Month') AS month_name, SUM(CASE WHEN role = 'teacher' THEN 1 ELSE 0 END) AS teacher_count, SUM(CASE WHEN role = 'student' THEN 1 ELSE 0 END) AS student_count FROM public.tutorapp_customuser GROUP BY  EXTRACT(MONTH FROM date_joined), TO_CHAR(date_joined, 'Month') ORDER BY EXTRACT(MONTH FROM date_joined);"
    result_userCounter = pd.read_sql(query_userCounter, engine)

    plt.figure(facecolor='#D8E7F7')
    ax = plt.gca()

    X = result_userCounter['month_name']
    Yteacher = result_userCounter['teacher_count']
    Zstudent = result_userCounter['student_count']

    X_axis = np.arange(len(X))

    plt.bar(X_axis - 0.2, Yteacher, 0.4, label='Teachers', linewidth=1.5, color="#F08FC2")
    plt.bar(X_axis + 0.2, Zstudent, 0.4, label='Students', linewidth=1.5, color="#A2639C")

    ax.set_facecolor('#D8E7F7')

    plt.xticks(X_axis, X)
    plt.xlabel("Месяц")
    plt.ylabel("Число")
    plt.title("Число наших пользователей за каждый месяц",
              fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontfamily': 'serif'})
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
    plt.legend()
    #plt.show()

    svg_buffer = io.BytesIO()
    plt.savefig(svg_buffer, format='svg')
    svg_buffer.seek(0)
    svg_data = svg_buffer.getvalue()

    plt.close()

    return HttpResponse(svg_data, content_type='image/svg+xml', status=status.HTTP_200_OK)