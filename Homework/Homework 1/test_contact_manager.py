from contact_manager import (
    now_iso, normalize_phone,
    add_contact, display_contact, list_all_contacts,
    search_contacts_by_name, search_contacts_by_category, find_contact_by_phone,
    update_contact, delete_contact, merge_contacts,
    generate_contact_statistics, find_duplicate_contacts
)


def _mk(first, last, phone, *, email="", category="personal", city="", state="", notes=""):
    today = now_iso()
    return {
        "first_name": first,
        "last_name": last,
        "phone": phone,
        "email": email,
        "address": {"street": "", "city": city, "state": state, "zip_code": ""},
        "category": category,
        "notes": notes,
        "created_date": today,
        "last_modified": today,
    }


def _seed():
    db = {}
    add_contact(db, _mk("Alice", "Nguyen", "(402) 555-1111", email="a@x.com", category="work",   city="Omaha",   state="NE"))
    add_contact(db, _mk("Bob",   "Lee",    "402-555-2222",   email="",       category="family", city="Omaha",   state="NE"))
    add_contact(db, _mk("Cara",  "Jones",  "312.555.3333",   email="c@x.com", category="personal", city="Chicago", state="IL"))
    add_contact(db, _mk("Dan",   "Li",     "3125553333",     email="c@x.com", category="work",   city="Chicago", state="IL"))
    add_contact(db, _mk("Evan",  "Stone",  "4025552222",     email="",       category="work",   city="Lincoln", state="NE"))
    return db


# ---------------------------
# Test Cases
# ---------------------------

def test_create_contact():
    db = {}
    cid = add_contact(db, _mk("Amy", "Zed", "555-111-2222", email="amy@example.com"))
    assert cid in db
    assert db[cid]["first_name"] == "Amy"
    bad = {"first_name": "", "last_name": "NoPhone", "phone": ""}
    assert add_contact(db, bad) is None


def test_search_functionality():
    db = _seed()
    hits = search_contacts_by_name(db, "li")
    assert len(hits) >= 1
    work = search_contacts_by_category(db, "work")
    assert len(work) >= 2
    cid, c = find_contact_by_phone(db, "(402)555-2222")
    assert cid and c
    assert normalize_phone(c["phone"]) == "4025552222"


def test_contact_operations():
    db = _seed()
    new_id = add_contact(db, _mk("New", "Guy", "999-000-0000"))
    assert new_id in db
    ok = update_contact(db, new_id, {"email": "newguy@example.com", "address": {"state": "TX"}})
    assert ok and db[new_id]["address"]["state"] == "TX"
    import builtins
    old = builtins.input
    builtins.input = lambda *_: "y"
    deleted = delete_contact(db, new_id)
    builtins.input = old
    assert deleted and new_id not in db


def test_data_analysis():
    db = _seed()
    stats = generate_contact_statistics(db)
    assert stats["total_contacts"] == len(db)
    assert "contacts_by_category" in stats
    dupes = find_duplicate_contacts(db)
    assert any(len(g) >= 2 for g in dupes["phone_duplicates"])
    assert any(len(g) >= 2 for g in dupes["email_duplicates"])


def run_all_tests():
    tests = [test_create_contact, test_search_functionality, test_contact_operations, test_data_analysis]
    passed, failed = 0, 0
    for t in tests:
        try:
            t()
            print(f"[PASS] {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {t.__name__}: {e}")
            failed += 1
    print(f"Results: {passed}/{passed+failed} passed, {failed} failed")


if __name__ == "__main__":
    run_all_tests()
