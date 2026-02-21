from core.storage import initialize_storage
from core.fixture import get_next_days_matches


def main():
    initialize_storage()
    matches = get_next_days_matches(2)

    print("PARTIDOS ENCONTRADOS:")
    for m in matches[:5]:
        print(m["league"], "-", m["home"], "vs", m["away"])

    print("Total:", len(matches))


if __name__ == "__main__":
    main()
