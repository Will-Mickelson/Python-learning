from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Tuple, Optional
import json
import re

Contact = Dict[str, Any]
ContactsDB = Dict[str, Contact]


def now_iso() -> str:
    return datetime.now().date().isoformat()


def normalize_phone(raw: str) -> str:
    return re.sub(r"\D+", "", raw)


# -------------------------
# Part 1 — Core Contact Management
# -------------------------

def create_contact() -> Contact:
    first_name = input("First name (required): ").strip()
    if first_name == "":
        first_name = input("First name can't be blank. What is your first name? ")
    last_name = input("Last name (required): ").strip()
    if last_name == "":
        last_name = input("Last name can't be blank. What is your last name? ")
    phone = input("Phone (required): ").strip()
    if phone == "":
        phone = input("Phone number can't be blank. What is your phone number? ")
    if len(phone) != 10:
        phone = int(input("Phone number has wrong amount of digits. What is your phone number? "))

    email = input("Email (optional): ").strip() or ""
    notes = input("Notes (optional): ").strip() or ""
    category = (input("Category [personal/work/family] (default personal): ").strip() or "personal").lower()

    print("-- Address (optional) --")
    address = {
        "street": input("Street: ").strip() or "",
        "city": input("City: ").strip() or "",
        "state": input("State: ").strip() or "",
        "zip_code": input("Zip: ").strip() or "",
    }

    now = now_iso()
    contact: Contact = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "address": address,
        "category": category,
        "notes": notes,
        "created_date": now,
        "last_modified": now,
    }

    return contact


def add_contact(contacts_db: ContactsDB, contact_data: Contact) -> Optional[str]:
    required = ("first_name", "last_name", "phone")
    if not all(contact_data.get(k, "").strip()for k in required):
        return None
    i = 1
    while True:
        cid = f"contact_{i:03d}"
        if cid not in contacts_db:
            contacts_db[cid] = contact_data
            return cid
        i += 1
    return None


def display_contact(contacts_db: ContactsDB, contact_id: str) -> bool:
    c = contacts_db.get(contact_id)
    if not c:
        return False
    addr = c.get("address", {}) or {}
    full_name = f"{c.get('first_name','')}{c.get('last_name','')}".strip()
    
    print("-" * 40)
    print(f"ID: {contact_id})")
    print(f"Name: {full_name}")
    print(f"Phone: {c.get('phone','')}")
    print(f"Email: {c.get('email','')}")
    print(f"Category: {c.get('category','')}")
    print("Address")
    print(f" {addr.get('street','')}")
    print(f" {addr.get('city','')}, {addr.get('state','')}{addr.get('zip_code')}")
    print(f"Notes: {addr.get('notes','')}")
    print(f"Created: {c.get('created_date','')} Last Modified: {c.get('last_modified','')}")
    print("-" * 40)
    return True


def list_all_contacts(contacts_db: ContactsDB) -> None:
    if not contacts_db:
        print("(No contacts)")
        return
    for cid, c in contacts_db.items():
        full_name = f"{c.get('first_name','')}{c.get('last_name','')}".strip()
        print(f"{cid:>12} | {full_name:25} | {c.get('phone','')}")
    pass

def search_contacts_by_name(contacts_db: ContactsDB, search_term: str) -> ContactsDB:
    """Return {id: contact} for case-insensitive, partial matches on first/last name.

    TODOs:
      - Lowercase the search term and names for matching.
      - Consider trimming whitespace and ignoring empty search term.
    """
    # TODO: Implement
    return {}


def search_contacts_by_category(contacts_db: ContactsDB, category: str) -> ContactsDB:
    cat = (category or "").strip().lower()
    if not cat: 
        return {}
    return {cid: c for cid, c in contacts_db.items()
            if c.get("category", "").strip().lower() == cat}


def find_contact_by_phone(contacts_db: ContactsDB, phone_number: str) -> Tuple[Optional[str], Optional[Contact]]:
    """Return (id, contact) if a contact exists with exact phone match (after normalization).

    TODOs:
      - Use normalize_phone() for both stored phone and query.
    """
    # TODO: Implement
    return None, None


# -------------------------
# Part 2 — Advanced Operations
# -------------------------


def update_contact(contacts_db: ContactsDB, contact_id: str, field_updates: Dict[str, Any]) -> bool:
    c = contacts_db.get(contact_id)
    if not c:
        return False
    for k, v in field_updates.items():
        c[k] = v
    
    from datetime import datetime
    c["last_modified"] = datetime.now().date().isoformat()
    return True


def delete_contact(contacts_db: ContactsDB, contact_id: str) -> bool:
    if contact_id not in contacts_db:
        return False
    if input(f"Delete {contact_id}? Type 'yes' to confirm: ").strip().lower() == "yes":
        contacts_db.pop(contact_id, None)
        return True
    return False


def merge_contacts(contacts_db: ContactsDB, contact_id1: str, contact_id2: str) -> Optional[str]:
    c1 = contacts_db.get(contact_id1)
    c2 = contacts_db.get(contact_id2)
    if not c1 or not c2:
        return None
    merged = {}
    keys = set(c1) | set(c2)
    
    def choose(label: str, v1, v2):
        if not v1 and v2: return v2
        if v1 and not v2: return v1
        if v1 == v2: return v1
        print(f"Conflict in {label}:\n 1) {v1}\n 2){v2}")
        while True:
            pick = input("Choose 1 or 2: ").strip()
            if pick in {"1", "2"}:
                return v1 if pick == "1" else v2
    for k in keys:
        if k == "address":
            a1 = c1.get("address", {}) or {}
            a2 = c2.get("address", {}) or {}
            addr = {}
            for ak in set(a1) | set(a2):
                addr[ak] = choose(f"address.{ak}", a1.get(ak, ""), a2.get(ak, ""))
            merged["address"] = addr
        elif k == "notes":
            n1, n2 = c1.get("notes", ""), c2.get("notes","")
            merged["notes"] = n1 if not n2 else (n2 if not n1 else f"{n1} | {n2}")
        elif k in {"created_date", "last_modified"}:
            continue
        else: 
            merged[k] = choose(k, c1.get(k, ""), c2.get(k, ""))
            
    from datetime import datetime
    d1, d2 = c1.get("created_date"), c2.get("created_date")
    merged["created_date"] = min(x for x in (d1, d2) if x) if (d1 or d2) else datetime.now().date().isoformat()
    merged["last_modified"] = datetime.now().date().isoformat()
    
    contacts_db[contact_id1] = merged
    contacts_db.pop(contact_id2, None)
    return contact_id1



def generate_contact_statistics(contacts_db: ContactsDB) -> Dict[str, Any]:
    total = len(contacts_db)
    by_cat, by_state, area_counts = {}, {}, {}
    no_email = 0
    
    for c in contacts_db():
        cat = (c.get("category", "")or"").strip().lower() or "uncategorized"
        by_cat[cat] = by_cat.get(cat, 0) + 1
        st = ((c.get("address", {}) or {}).get("state", "") or "").strip().upper()
        if st:
            by_state[st] = by_state.get(st, 0) + 1
        if not (c.get("email", "") or "").strip():
            no_email += 1
        pn = re.sub(r"\D+", "", c.get("phone", "") or "")
        if len(pn) >= 3:
            ac = pn[:3]
            area_counts[ac] = area_counts.get(ac, 0) + 1
    avg_per_cat = (total / len(by_cat)) if by_cat else 0.0
    most_common_ac = max(area_counts, key=area_counts.get)if area_counts else None
    return {
        "total_contacts": total,
        "contatcs_by_category": by_cat,
        "contacts_by_state": by_state,
        "average_contacts_per_category": round(avg_per_cat, 2),
        "most_common_are_code": most_common_ac,
        "contacts_without_email": no_email,
    }

def find_duplicate_contacts(contacts_db: ContactsDB) -> Dict[str, Any]:
    def groups(key_fn):
        m = {}
        for cid, c in contacts_db.items():
            k = key_fn(c)
            if k:
                m.setdefault(k,[]).append(cid)
        return [ids for ids in m.values() if len(ids) >= 2]
    phone_dupes = groups(lambda c: re.sub(r"\D+", "", c.get("phone", "") or ""))
    email_dupes = groups(lambda c: (c.get("email", "") or "").strip().lower())
    name_dupes = groups(lambda c: ((c.get("first_name", "") + "|" + c.get("last_name","")).strip().lower()) or "")
    
    return {"phone_duplicates": phone_dupes,
            "email_duplicates": email_dupes,
            "name_duplicates": name_dupes
    }


def export_contacts_by_category(contacts_db: ContactsDB, category: str) -> str:
    cat = (category or "").strip().lower()
    lines = []
    for cid, c in contacts_db.items():
        if (c.get("category", "") or "").strip().lower() == cat:
            addr = c.get("address",{}) or {}
            lines.extend([
                f"ID: {cid}",
                f"Name: {c.get("first_name,", '')}{c.get('last_name', '')}",
                f"Phone: {c.get('phone','')}",
                f"Email: {c.get('email','')}",
                f"Address: {addr.get('street','')}",
                f"         {addr.get('city','')},{addr.get('state','')}{addr.get('zip_code','')}",
                f"Notes: {c.get('notes','')}",
                "-" * 40
            ])
    return "\n".join(lines) if lines else "(No contacts in this category)"


# -------------------------
# Part 3 — CLI & Persistence
# -------------------------

def save_contacts_to_file(contacts_db: ContactsDB, filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(contacts_db, f, ensure_ascii=False, indent=2)
    pass


def load_contacts_from_file(filename: str) -> ContactsDB:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}


MENU = """
==============================
  Contact Manager — Main Menu
==============================
1. Add new contact
2. Search contacts
3. List all contacts
4. Update contact
5. Delete contact
6. Generate statistics
7. Find duplicates
8. Export by category
9. Save to file (bonus)
10. Load from file (bonus)
0. Exit
"""


def main_menu(contacts_db: ContactsDB) -> None:
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            cid = add_contact(contacts_db, create_contact())
            print(f"Added {cid}" if cid else "Add failed (missing required fields).")
        elif choice == "2":
            sub = input("search by (n)ame/(c)ategory/(p)hone: ").strip().lower()
            if sub == "n":
                term = input("Name contains: ")
                results = search_contacts_by_name(contacts_db, term)
            elif sub == "c":
                cat = input("Category: ")
                results = search_contacts_by_category(contacts_db, cat)
            elif sub == "p":
                ph = input("Phone")
                cid, c = find_contact_by_phone(contacts_db, ph)
                results = {cid: c} if cid and c else {}
            else: 
                results = {}
            print(f"Matches : {len(results)}")
            for rcid in results: 
                display_contact(contacts_db, rcid)
        elif choice == "3":
            list_all_contacts(contacts_db)
        elif choice == "4":
            cid = input("Contatc ID: ").strip()
            updates = {}
            print("Enter updates below (blank to skip): ")
            for k in ["first_name","last_name","phone","email","category","notes"]:
                v = input(f"{k}: ").strip()
                if v: updates[k] = v
            addr = {}
            print("-- Address updates --")
            for ak in ["street","city","state","zip_code"]:
                v = input(f"{ak}: ").strip()
                if v: updates[k] = v
            if addr: updates["address"] = addr
            print("Updated" if update_contact(contacts_db, cid, updates) else "Update failed.")
        elif choice == "5":
            cid = input("Contact ID to delete: ").strip()
            print("Deleted" if delete_contact(contacts_db, cid) else "Not deleted")
        elif choice == "6":
            print(json.dumps(generate_contact_statistics(contacts_db), indent=2))
        elif choice == "7":
            print(json.dumps(find_duplicate_contacts(contacts_db), indent=2))
        elif choice == "8":
            cat = input("Category to export: ").strip()
            print(export_contacts_by_category(contacts_db, cat))
        elif choice == "9":
            fn = input("Save filename (default contacts.json): ").strip() or "contacts.json"
            save_contacts_to_file(contacts_db, fn)
        elif choice == "10":
            fn = input("Load filename (default contacts.json): ").strip() or "contacts.json"
            contacts_db.clear()
            contacts_db.update(load_contacts_from_file(fn))
        else:
            print("Invalid choice — try again.")


def run_contact_manager() -> None:
    """Entry point: initialize an empty DB and start the menu loop."""
    contacts: ContactsDB = {}
    main_menu(contacts)


if __name__ == "__main__":
    run_contact_manager()
