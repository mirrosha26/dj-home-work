import pytest 
import random
from pprint import pprint
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course



@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

#проверяем запрос на получение курса
@pytest.mark.django_db
def test_first_course(client, course_factory, student_factory):
    # Arrange
    students = student_factory(_quantity=10)
    student_ids = [student.pk for student in students]
    course = course_factory(_quantity=1, students=students)
    # Act
    response = client.get(f"/api/v1/courses/{course[0].pk}/")
    # Assert
    assert response.status_code == 200
    assert response.data['id'] == course[0].pk
    assert response.data['name'] == course[0].name
    assert set(response.data['students']) == set(student_ids)


#проверка получения списка курсов (list-логика):
@pytest.mark.django_db
def test_list_course(client, course_factory, student_factory):
    # Arrange
    students = student_factory(_quantity=10)
    student_ids = [student.pk for student in students]
    courses = course_factory(_quantity=10,students=students)
    # Act
    response = client.get(f"/api/v1/courses/")
    # Assert
    assert response.status_code == 200
    for i, c in enumerate(courses):
        assert c.pk == response.data[i]['id']
        assert c.name == response.data[i]['name']
        assert set(response.data[i]['students']) == set(student_ids)


#проверка фильтрации списка курсов по id:
@pytest.mark.django_db
def test_get_filter_id_course(client, course_factory, student_factory):
    # Arrange
    students = student_factory(_quantity=10)
    student_ids = [student.pk for student in students]
    courses = course_factory(_quantity=10,students=students)
    # Act
    random_course = random.choice(courses)
    response = client.get(f'/api/v1/courses/?id={random_course.pk}')
    # Assert
    assert response.status_code == 200
    assert response.data[0]['id'] == random_course.pk
    assert response.data[0]['name'] == random_course.name
    assert set(response.data[0]['students']) == set(student_ids)


#проверка фильтрации списка курсов по name;
@pytest.mark.django_db
def test_get_filter_name_course(client, course_factory, student_factory):
    # Arrange
    students = student_factory(_quantity=10)
    student_ids = [student.pk for student in students]
    courses = course_factory(_quantity=10,students=students)
    #Act 
    random_course = random.choice(courses)
    response = client.get(f'/api/v1/courses/?name={random_course.name}')
    # Assert
    assert response.status_code == 200
    data = response.json()
    for i, c in enumerate(data):
        assert c['name'] == random_course.name
        assert c['name'] == random_course.name
        assert set(c['students']) == set(student_ids)


#тест успешного создания курса:
@pytest.mark.django_db
def test_post_course(client, student_factory):
    # Arrange
    students = student_factory(_quantity=3)
    student_ids = [student.pk for student in students]
    #Act 
    response = client.post('/api/v1/courses/', data={'name': 'mirrosha_test', 'students': student_ids}, format='json')
    # Assert
    assert response.status_code == 201
    assert response.data['name'] == 'mirrosha_test'
    assert set(response.data['students']) == set(student_ids)


#тест успешного обновления курса:
@pytest.mark.django_db
def test_patch_course(client, course_factory, student_factory):
    # Arrange
    students = student_factory(_quantity=3)
    student_ids = [student.pk for student in students]
    course = course_factory(_quantity=1,students=students)
    #Act 
    response = client.patch(f'/api/v1/courses/{course[0].pk}/', data={'name': 'mirrosha_course', 'students' : student_ids[:1]}, format='json')
    assert response.status_code == 200
    assert response.data['name'] == 'mirrosha_course'
    assert set(response.data['students']) == set(student_ids[:1])

#тест успешного удаления курса.
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.delete(f'/api/v1/courses/{course[0].pk}/')
    assert response.status_code == 204
    assert response.data is None