import pytest
from django.urls import reverse

from notes.forms import NoteForm

from notes.pytest_tests.constants import NOTES_ON_PAGE, NOTE_SLUG


def test_note_is_in_author_list(
    note,
    author_client,
):
    response = author_client.get(reverse('notes:list'))
    notes = response.context['object_list']

    assert list(notes) == [note]


def test_note_is_not_in_reader_list(
    note,
    reader_client,
):
    response = reader_client.get(reverse('notes:list'))
    notes = response.context['object_list']

    assert note not in notes


def test_notes_are_sorted_newest_first(
    notes,
    author_client,
):
    response = author_client.get(reverse('notes:list'))
    object_list = list(response.context['object_list'])
    expected_notes = list(reversed(notes))[:NOTES_ON_PAGE]

    assert object_list == expected_notes


def test_notes_count_on_page_is_limited(
    notes,
    author_client,
):
    response = author_client.get(reverse('notes:list'))
    object_list = response.context['object_list']

    assert len(object_list) == NOTES_ON_PAGE


@pytest.mark.parametrize(
    ('name', 'args'),
    (
        ('notes:add', ()),
        ('notes:edit', (NOTE_SLUG,)),
    ),
)
def test_add_and_edit_pages_contain_form(
    note,
    author_client,
    name,
    args,
):
    url = reverse(name, args=args)

    response = author_client.get(url)

    assert isinstance(response.context['form'], NoteForm)
