# coding: utf-8

from dext.forms import fields

from game.persons.models import PERSON_STATE

from game.bills.models import BILL_TYPE
from game.bills.forms import BaseUserForm, BaseModeratorForm

from game.persons.storage import persons_storage
from game.map.places.storage import places_storage

class UserForm(BaseUserForm):

    person = fields.ChoiceField(label=u'Персонаж')

    def __init__(self, choosen_person_id, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        persons_by_place = {}

        for person in persons_storage.filter(state=PERSON_STATE.IN_GAME):
            if person.place_id not in persons_by_place:
                persons_by_place[person.place_id] = []
            persons_by_place[person.place_id].append(person)

        candidates = []

        for place_id, persons in persons_by_place.items():
            place = places_storage[place_id]
            sorted_persons = sorted(persons, key=lambda p: -p.power)
            candidates.extend(sorted_persons[place.max_persons_number/2:])

        choices = [(person.id, u'%s (%s)' % (person.name, person.place.name)) for person in candidates]

        for person_id, name in choices:
            if person.id == choosen_person_id:
                choosen_person_id = None
                break

        if choosen_person_id:
            person = persons_storage[choosen_person_id]
            choices.append((choosen_person_id, u'%s (%s)' % (person.name, person.place.name)))

        self.fields['person'].choices = sorted(choices, key=lambda p: p[1])


class ModeratorForm(BaseModeratorForm):
    pass

class PersonRemove(object):

    type = BILL_TYPE.PERSON_REMOVE
    type_str = BILL_TYPE.ID_2_STR[BILL_TYPE.PERSON_REMOVE].lower()

    UserForm = UserForm
    ModeratorForm = ModeratorForm

    USER_FORM_TEMPLATE = 'bills/bills/person_remove_user_form.html'
    MODERATOR_FORM_TEMPLATE = 'bills/bills/person_remove_moderator_form.html'
    SHOW_TEMPLATE = 'bills/bills/person_remove_show.html'

    CAPTION = u'Закон об изгнании персонажа'
    DESCRIPTION = u'В случае если персонаж утратил доверие духов-хранителей, его можно изгнать из города. Изгонять можно только наименее влиятельных персонажей.'

    def __init__(self, person_id=None):
        self.person_id = person_id

    @property
    def person(self):
        return persons_storage[self.person_id]

    @property
    def user_form_initials(self):
        return {'person': self.person_id}

    @property
    def moderator_form_initials(self):
        return {}

    def initialize_with_user_data(self, user_form):
        self.person_id = int(user_form.c.person)

    def initialize_with_moderator_data(self, moderator_form):
        pass

    @classmethod
    def get_user_form_create(cls, post=None):
        return UserForm(None, post)

    def get_user_form_update(self, post=None, initial=None):
        if initial:
            return UserForm(self.person_id, initial=initial)
        return  UserForm(self.person_id, post)

    def apply(self):
        self.person.move_out_game()
        self.person.place.sync_persons()

        self.person.save()
        persons_storage.update_version()

    def serialize(self):
        return {'type': self.type_str,
                'person_id': self.person_id}

    @classmethod
    def deserialize(cls, data):
        obj = cls()
        obj.person_id = data['person_id']

        return obj
