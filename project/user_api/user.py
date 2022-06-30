from project.models import User, Folder, Deck


def fetch_user(id_user):
    user = User.query.filter_by(id_user=id_user).first()
    root_folder = Folder.query.filter_by(id_folder=user.id_root_folder).first()

    return {
        'user': {
            'id': id_user,
            'name': user.name,
            'email': user.email
        },
        'state': extract_folder(root_folder.id_folder)
    }


def extract_folder(id_folder):
    folder = Folder.query.filter_by(id_folder=id_folder).first()
    nested_folders = Folder.query.filter_by(id_parent_folder=folder.id_folder).all()

    extracted = []
    if nested_folders:
        for nested_folder in nested_folders:
            extracted.append(extract_folder(nested_folder.id_folder))
    else:
        for deck in folder.decks:
            extracted.append(extract_deck(deck.id_deck))

    return {
        'id': id_folder,
        'name': folder.name,
        'children': extracted
    }


def extract_deck(id_deck):
    deck = Deck.query.filter_by(id_deck=id_deck).first()

    return {
        'id': id_deck,
        'name': deck.name,
        'cards': [{'id': card.id_card,
                   'name': card.front_side,
                   'translations': card.back_side.split(' ')
                   } for card in deck.cards
                  ]
    }
