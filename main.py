

def fetch_all_active_members() -> Iterable[ApiMemberItem]:
    logger.info(f"Fetching all active members")

    all_members: Iterable[ApiMemberItem] = ()
    skip = 0

    while True:
        response = search_members(
            client=members_client,
            is_current_member=True,
            house=House.VALUE_1,
            skip=skip,
        )
        if not response:
            logger.warning("No members found")
            break

        items = response.items
        if not items:
            break

        all_members = chain(all_members, items)
        skip += len(items)

    return all_members
