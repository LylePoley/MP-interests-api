from httpx import Client

members_client = Client(base_url="https://members.parliament.uk/", follow_redirects=True)