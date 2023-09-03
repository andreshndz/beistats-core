from enum import Enum


class UserType(str, Enum):
    organizer = 'organizer'
    player = 'player'
