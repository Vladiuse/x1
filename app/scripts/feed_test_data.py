import json
import random

from faker import Faker
from links.models import Link, LinkCollection
from users.models import CustomUser


def run() -> None:
    f = Faker()
    CustomUser.objects.all().delete()
    LinkCollection.objects.all().delete()
    Link.objects.all().delete()

    COLLECTION_NAMES = [
        'music',
        'work',
        'videos',
        'games',
        'other',
        'books',
    ]
    with open('_data/links_data.json', encoding='utf-8') as file:
        LINKS_DATA = json.load(file)

    LINKS_DATA = LINKS_DATA[:30]
    CustomUser.objects.create_user(email='vladiuse@gmail.com', password='0000')

    unique_email = [f.email() for _ in range(100)][:30]
    users_to_create = [CustomUser(email=email) for email in unique_email]
    CustomUser.objects.bulk_create(users_to_create)
    created_users = CustomUser.objects.all()
    for user in created_users:
        user.set_password('0000')
    CustomUser.objects.bulk_update(created_users, ['password'])

    collections_to_create = []
    for user in created_users:
        collection_names = random.sample(COLLECTION_NAMES, k=random.randint(1, len(COLLECTION_NAMES)))
        for name in collection_names:
            collection = LinkCollection(owner=user, name=name)
            collections_to_create.append(collection)

    LinkCollection.objects.bulk_create(collections_to_create)

    for user in created_users:
        user_link_collections = list(LinkCollection.objects.filter(owner=user))
        links_data = random.sample(LINKS_DATA, k=random.randint(5, len(LINKS_DATA)))
        links_to_create = []
        for link_item in links_data:
            link = Link(
                owner=user,
                url=link_item['url'],
                parsed_url=link_item['parsed_url'],
                title=link_item['title'],
                description=link_item['description'],
                type=link_item['type'],
                image_url=link_item['image_url'],
            )
            links_to_create.append(link)
        Link.objects.bulk_create(links_to_create)
        user_links = Link.objects.filter(owner=user)
        for link in user_links:
            collections_to_add = random.sample(user_link_collections, k=random.randint(0, len(user_link_collections)))
            link.collections.set(collections_to_add)

    print('Users', CustomUser.objects.count())
    print('Collections', LinkCollection.objects.count())
    print('Links', Link.objects.count())
