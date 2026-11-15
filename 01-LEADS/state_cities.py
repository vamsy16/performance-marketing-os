#!/usr/bin/env python3
"""State-scoped lead collection: a state name in, an allowlist of cities out.

    from state_cities import in_state, filter_leads, cities_for

    ok, why = in_state("Begumpet, Hyderabad", "Telangana")   # (True, ...)
    ok, why = in_state("Kamakshipalya, Bengaluru", "Telangana")  # (False, ...)

Why this exists
---------------
A sweep for one state keeps surfacing advertisers from the next one over -
V1 Solar Solutions is rowed with city "Kamakshipalya, Bengaluru (advertising
into Hyderabad)", and mr_koti_00 was vetoed as Guntur, Andhra Pradesh. Both
were caught by hand. This module makes the check mechanical: a lead is only
kept if its city resolves to a city inside the configured state.

Two things make that harder than a string compare, and both are handled here:

  1. City fields are free text. leads.csv holds "Begumpet, Hyderabad",
     "Suncity, Bandlaguda Jagir, Hyderabad", "Kothagudem 507101 (serves
     Telangana and Andhra Pradesh)" and "Kamakshipalya, Bengaluru
     (advertising into Hyderabad)". Parenthetical notes, pin codes and
     locality-then-city ordering all have to be parsed before anything can be
     matched.

  2. Localities are not cities. "Begumpet" and "Mehdipatnam" are Hyderabad
     localities, and "Kamakshipalya" is a Bengaluru locality. Without a
     locality map, a lead that is genuinely in Hyderabad reads as an unknown
     city and gets dropped for the wrong reason.

Resolution order for a city string
----------------------------------
  1. strip anything in parentheses - "(serves ...)", "(advertising into ...)"
  2. strip a trailing pin code - "Kothagudem 507101" -> "Kothagudem"
  3. split on commas; the LAST segment is the city, earlier ones are localities
     of it. "Suncity, Bandlaguda Jagir, Hyderabad" -> Hyderabad
  4. if the last segment is itself a known locality, map it to its parent city
  5. if nothing resolves, the city is unknown - reported as such, never guessed

Nothing here invents a city. An unresolved string is reported as unresolved so
the operator can add it, rather than being silently matched or dropped.
"""

# ---------------------------------------------------------------------------
# States and their cities
# ---------------------------------------------------------------------------
# Canonical spelling is the key; the values are the cities that count as
# inside that state. A city appears under exactly one state unless it is
# genuinely disputed or shared, which is noted in the comment.

STATE_CITIES = {
    "Andaman and Nicobar Islands": ("Port Blair",),
    "Andhra Pradesh": (
        "Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool",
        "Rajahmundry", "Tirupati", "Kadapa", "Kakinada", "Anantapur",
        "Vizianagaram", "Eluru", "Ongole", "Nandyal", "Machilipatnam",
        "Adoni", "Tenali", "Proddatur", "Chittoor", "Hindupur", "Srikakulam",
        "Bhimavaram", "Guntakal", "Dharmavaram", "Gudivada", "Narasaraopet",
        "Tadepalligudem", "Chirala", "Amaravati",
    ),
    "Arunachal Pradesh": (
        "Itanagar", "Pasighat", "Tawang", "Ziro", "Bomdila", "Naharlagun",
    ),
    "Assam": (
        "Guwahati", "Dibrugarh", "Jorhat", "Silchar", "Tezpur", "Nagaon",
        "Tinsukia", "Bongaigaon", "Dhubri", "Diphu", "Dhemaji", "Goalpara",
        "Karimganj", "Sivasagar", "Haflong",
    ),
    "Bihar": (
        "Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga", "Purnia",
        "Ara", "Begusarai", "Katihar", "Chapra", "Sasaram", "Hajipur",
        "Dehri", "Siwan", "Motihari", "Nalanda", "Bettiah", "Jehanabad",
        "Aurangabad", "Sitamarhi",
    ),
    "Chandigarh": ("Chandigarh",),
    "Chhattisgarh": (
        "Raipur", "Bhilai", "Bilaspur", "Korba", "Durg", "Rajnandgaon",
        "Jagdalpur", "Raigarh", "Ambikapur", "Mahasamund", "Dhamtari",
        "Chirmiri", "Bhatapara", "Kanker",
    ),
    "Dadra and Nagar Haveli and Daman and Diu": ("Silvassa", "Daman", "Diu"),
    "Delhi": (
        "New Delhi", "Delhi", "Dwarka", "Rohini", "Saket", "Karol Bagh",
        "Pitampura", "Janakpuri", "Lajpat Nagar", "Vasant Kunj", "Najafgarh",
        "Narela", "Shahdara", "Mayur Vihar",
    ),
    "Goa": ("Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda", "Bicholim"),
    "Gujarat": (
        "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar",
        "Gandhinagar", "Junagadh", "Anand", "Nadiad", "Morbi", "Mehsana",
        "Bharuch", "Vapi", "Navsari", "Valsad", "Porbandar", "Gandhidham",
        "Veraval", "Palanpur", "Bhuj", "Ankleshwar", "Patan",
    ),
    "Haryana": (
        "Faridabad", "Gurugram", "Panipat", "Ambala", "Yamunanagar",
        "Rohtak", "Hisar", "Karnal", "Sonipat", "Panchkula", "Bhiwani",
        "Sirsa", "Bahadurgarh", "Jind", "Thanesar", "Kaithal", "Rewari",
        "Palwal", "Narnaul",
    ),
    "Himachal Pradesh": (
        "Shimla", "Solan", "Mandi", "Dharamshala", "Bilaspur", "Hamirpur",
        "Kullu", "Una", "Chamba", "Palampur", "Nahan",
    ),
    "Jammu and Kashmir": (
        "Srinagar", "Jammu", "Anantnag", "Baramulla", "Sopore", "Kathua",
        "Udhampur", "Rajouri", "Poonch", "Kupwara", "Bandipora",
    ),
    "Jharkhand": (
        "Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Deoghar", "Hazaribagh",
        "Giridih", "Ramgarh", "Medininagar", "Chirkunda", "Phusro", "Jhumri",
        "Sahibganj", "Chaibasa",
    ),
    "Karnataka": (
        "Bengaluru", "Mysuru", "Hubballi", "Mangaluru", "Belagavi",
        "Kalaburagi", "Davanagere", "Ballari", "Vijayapura", "Shivamogga",
        "Tumakuru", "Raichur", "Bidar", "Hassan", "Udupi", "Robertsonpet",
        "Kolar", "Mandya", "Chikkamagaluru", "Karwar", "Ranebennuru",
        "Bagalkot", "Gadag", "Yadgir", "Koppal", "Chitradurga", "Haveri",
        "Kundapura", "Tiptur",
    ),
    "Kerala": (
        "Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam",
        "Alappuzha", "Kannur", "Kottayam", "Palakkad", "Manjeri",
        "Thalassery", "Ponnani", "Vatakara", "Kanhangad", "Payyanur",
        "Koyilandy", "Parappanangadi", "Taliparamba", "Perinthalmanna",
        "Punalur", "Kayamkulam",
    ),
    "Ladakh": ("Leh", "Kargil"),
    "Lakshadweep": ("Kavaratti",),
    "Madhya Pradesh": (
        "Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain", "Sagar",
        "Dewas", "Satna", "Ratlam", "Rewa", "Katni", "Singrauli", "Burhanpur",
        "Khandwa", "Morena", "Bhind", "Chhindwara", "Guna", "Shivpuri",
        "Vidisha", "Damoh", "Mandsaur", "Khargone", "Neemuch", "Pithampur",
        "Hoshangabad", "Itarsi",
    ),
    "Maharashtra": (
        "Mumbai", "Pune", "Nagpur", "Nashik", "Thane", "Aurangabad",
        "Solapur", "Amravati", "Kolhapur", "Navi Mumbai", "Sangli",
        "Jalgaon", "Akola", "Latur", "Ahmednagar", "Dhule", "Chandrapur",
        "Parbhani", "Ichalkaranji", "Jalna", "Bhiwandi", "Panvel",
        "Malegaon", "Nanded", "Satara", "Wardha", "Yavatmal", "Osmanabad",
        "Ratnagiri", "Barshi",
    ),
    "Manipur": ("Imphal", "Thoubal", "Kakching", "Churachandpur"),
    "Meghalaya": ("Shillong", "Tura", "Jowai", "Nongstoin", "Williamnagar"),
    "Mizoram": ("Aizawl", "Lunglei", "Champhai", "Serchhip", "Kolasib"),
    "Nagaland": ("Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha",
                 "Zunheboto"),
    "Odisha": (
        "Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur",
        "Puri", "Balasore", "Bhadrak", "Baripada", "Jharsuguda", "Jeypore",
        "Angul", "Baleshwar", "Kendrapara", "Paradip",
    ),
    "Puducherry": ("Puducherry", "Karaikal", "Yanam", "Mahe"),
    "Punjab": (
        "Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda",
        "Mohali", "Pathankot", "Hoshiarpur", "Batala", "Moga", "Sangrur",
        "Barnala", "Firozpur", "Phagwara", "Kapurthala", "Rajpura",
        "Sahnewal", "Goindwal",
    ),
    "Rajasthan": (
        "Jaipur", "Jodhpur", "Kota", "Bikaner", "Ajmer", "Udaipur",
        "Bhilwara", "Alwar", "Sikar", "Bharatpur", "Pali", "Sri Ganganagar",
        "Kishangarh", "Kota", "Ajmer", "Banswara", "Baran", "Beawar",
        "Hanumangarh", "Jhunjhunu", "Chittorgarh", "Nagaur", "Makrana",
        "Bhiwadi", "Neemrana",
    ),
    "Sikkim": ("Gangtok", "Namchi", "Gyalshing", "Mangan", "Rangpo"),
    "Tamil Nadu": (
        "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem",
        "Tirunelveli", "Tiruppur", "Erode", "Vellore", "Thoothukudi",
        "Thanjavur", "Dindigul", "Tambaram", "Nagercoil", "Kanchipuram",
        "Karur", "Hosur", "Cuddalore", "Kumbakonam", "Sivakasi", "Pudukkottai",
        "Rajapalayam", "Nagapattinam", "Villupuram", "Ambattur", "Avadi",
        "Tiruvannamalai", "Pollachi", "Neyveli",
    ),
    "Telangana": (
        "Hyderabad", "Secunderabad", "Warangal", "Nizamabad", "Karimnagar",
        "Khammam", "Ramagundam", "Mahbubnagar", "Nalgonda", "Adilabad",
        "Suryapet", "Miryalaguda", "Jagtial", "Wanaparthy", "Koratla",
        "Siddipet", "Sangareddy", "Zahirabad", "Bodhan", "Kothagudem",
        "Mancherial", "Nirmal", "Kamareddy", "Jangaon", "Bhupalpally",
        "Vikarabad", "Tandur", "Ibrahimpatnam", "Shadnagar", "Chevella",
        "Gadwal", "Nagarkurnool", "Medak", "Narayanpet", "Yellandu",
        "Bhadrachalam", "Palwancha",
    ),
    "Tripura": ("Agartala", "Udaipur", "Dharmanagar", "Kailasahar", "Belonia"),
    "Uttar Pradesh": (
        "Lucknow", "Kanpur", "Ghaziabad", "Agra", "Varanasi", "Meerut",
        "Prayagraj", "Bareilly", "Aligarh", "Moradabad", "Saharanpur",
        "Gorakhpur", "Noida", "Firozabad", "Jhansi", "Muzaffarnagar",
        "Mathura", "Rampur", "Shahjahanpur", "Farrukhabad", "Ayodhya",
        "Sitapur", "Jaunpur", "Bahraich", "Bulandshahr", "Hardoi",
        "Sultanpur", "Unnao", "Hapur", "Raebareli",
    ),
    "Uttarakhand": (
        "Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rudrapur",
        "Kashipur", "Rishikesh", "Pithoragarh", "Ramnagar", "Manglaur",
        "Nainital", "Almora", "Pauri", "Kotdwara",
    ),
    "West Bengal": (
        "Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Bardhaman",
        "Malda", "Baharampur", "Habra", "Kharagpur", "Shantipur", "Dankuni",
        "Haldia", "Raiganj", "Krishnanagar", "Jalpaiguri", "Balurghat",
        "Bankura", "Purulia", "Cooch Behar", "Darjeeling", "Alipurduar",
        "Barasat", "Madhyamgram", "Naihati",
    ),
}

# ---------------------------------------------------------------------------
# Localities -> the city they belong to
# ---------------------------------------------------------------------------
# Every key here is a place that shows up as the FIRST segment of a city string
# ("Begumpet, Hyderabad") or on its own, and that is not itself a city. Values
# are canonical city names. Without this map, a genuinely in-state lead reads
# as an unknown city and is dropped for the wrong reason.

LOCALITIES = {
    # Hyderabad
    "Begumpet": "Hyderabad",
    "Mehdipatnam": "Hyderabad",
    "Gachibowli": "Hyderabad",
    "Kothapet": "Hyderabad",
    "Jubilee Hills": "Hyderabad",
    "Shaikpet": "Hyderabad",
    "IDA Jeedimetla": "Hyderabad",
    "Bandlaguda Jagir": "Hyderabad",
    "Suncity": "Hyderabad",
    "Madhapur": "Hyderabad",
    "Hitec City": "Hyderabad",
    "Kondapur": "Hyderabad",
    "Kukatpally": "Hyderabad",
    "Ameerpet": "Hyderabad",
    "Charminar": "Hyderabad",
    "Lakdikapul": "Hyderabad",
    "Banjara Hills": "Hyderabad",
    "Somajiguda": "Hyderabad",
    "Rajendranagar": "Hyderabad",
    "Attapur": "Hyderabad",
    "Malkajgiri": "Hyderabad",
    "Uppal": "Hyderabad",
    "LB Nagar": "Hyderabad",
    "Dilsukhnagar": "Hyderabad",
    "Miyapur": "Hyderabad",
    "Kompally": "Hyderabad",
    "Shamshabad": "Hyderabad",
    "Kokapet": "Hyderabad",
    "Narsingi": "Hyderabad",
    "Manikonda": "Hyderabad",
    "Tolichowki": "Hyderabad",
    "Saroornagar": "Hyderabad",
    "Sainikpuri": "Hyderabad",
    "Alwal": "Hyderabad",
    # Secunderabad is a twin city and is listed as its own city above; keep
    # its localities pointing at it so "Trimulgherry, Secunderabad" resolves.
    "Trimulgherry": "Secunderabad",
    "Marredpally": "Secunderabad",
    "West Marredpally": "Secunderabad",
    # Bengaluru
    "Kamakshipalya": "Bengaluru",
    "Whitefield": "Bengaluru",
    "Koramangala": "Bengaluru",
    "Indiranagar": "Bengaluru",
    "Jayanagar": "Bengaluru",
    "Malleshwaram": "Bengaluru",
    "Rajajinagar": "Bengaluru",
    "Yeshwanthpur": "Bengaluru",
    "Electronic City": "Bengaluru",
    "HSR Layout": "Bengaluru",
    "BTM Layout": "Bengaluru",
    "Hebbal": "Bengaluru",
    "Yelahanka": "Bengaluru",
    "Peenya": "Bengaluru",
    "Bommanahalli": "Bengaluru",
    "Hennur": "Bengaluru",
    "Basavanagudi": "Bengaluru",
    # Chennai
    "T Nagar": "Chennai",
    "Thiruvanmiyur": "Chennai",
    "Velachery": "Chennai",
    "Adyar": "Chennai",
    "Ambattur": "Chennai",
    "Anna Nagar": "Chennai",
    "Guindy": "Chennai",
    "Porur": "Chennai",
    "OMR": "Chennai",
    "Sholinganallur": "Chennai",
    # Mumbai
    "Andheri": "Mumbai",
    "Bandra": "Mumbai",
    "Borivali": "Mumbai",
    "Dadar": "Mumbai",
    "Powai": "Mumbai",
    "Thane West": "Thane",
    "Vikhroli": "Mumbai",
    "Chembur": "Mumbai",
    "Goregaon": "Mumbai",
    "Malad": "Mumbai",
    "Kurla": "Mumbai",
    "Wadala": "Mumbai",
    # Pune
    "Hinjewadi": "Pune",
    "Kothrud": "Pune",
    "Wakad": "Pune",
    "Baner": "Pune",
    "Hadapsar": "Pune",
    "Viman Nagar": "Pune",
    "Kharadi": "Pune",
    "Pimpri": "Pune",
    "Chinchwad": "Pune",
    "Aundh": "Pune",
    # Delhi NCR
    "Connaught Place": "New Delhi",
    "Laxmi Nagar": "Delhi",
    "Rajouri Garden": "New Delhi",
    "Okhla": "New Delhi",
    "Naraina": "New Delhi",
    "Bawana": "Delhi",
    "Mundka": "Delhi",
    "Dwarka Sector": "Dwarka",
    "Sector 63": "Noida",
    "Sector 18": "Noida",
    # Visakhapatnam
    "MVP Colony": "Visakhapatnam",
    "Gajuwaka": "Visakhapatnam",
    "Madhurawada": "Visakhapatnam",
    # Vijayawada
    "Kanuru": "Vijayawada",
    "Gollapudi": "Vijayawada",
    "Gunadala": "Vijayawada",
}

# Aliases: alternative spellings seen in ad copy and on websites.
CITY_ALIASES = {
    "Bangalore": "Bengaluru",
    "Bombay": "Mumbai",
    "Calcutta": "Kolkata",
    "Madras": "Chennai",
    "Mysore": "Mysuru",
    "Mangalore": "Mangaluru",
    "Belgaum": "Belagavi",
    "Gulbarga": "Kalaburagi",
    "Bijapur": "Vijayapura",
    "Hubli": "Hubballi",
    "Dharwad": "Dharwad",
    "Trichy": "Tiruchirappalli",
    "Trichinopoly": "Tiruchirappalli",
    "Pondicherry": "Puducherry",
    "Vizag": "Visakhapatnam",
    "Waltair": "Visakhapatnam",
    "Vijayawada": "Vijayawada",
    "Bezawada": "Vijayawada",
    "Rajahmundry": "Rajahmundry",
    "Rajamundry": "Rajahmundry",
    "Eluru": "Eluru",
    "Nellore": "Nellore",
    "Sri Nellore": "Nellore",
    "Guntur": "Guntur",
    "Warangal": "Warangal",
    "Orugallu": "Warangal",
    "Hanamkonda": "Hanamkonda",
    "Kazipet": "Warangal",
    "Nizamabad": "Nizamabad",
    "Indur": "Nizamabad",
    "Karimnagar": "Karimnagar",
    "Khammam": "Khammam",
    "Nalgonda": "Nalgonda",
    "Mahbubnagar": "Mahbubnagar",
    "Palamoor": "Mahbubnagar",
    "Sangareddy": "Sangareddy",
    "Sangareddi": "Sangareddy",
    "Siddipet": "Siddipet",
    "Suryapet": "Suryapet",
    "Miryalaguda": "Miryalaguda",
    "Adilabad": "Adilabad",
    "Ramagundam": "Ramagundam",
    "Ramagundem": "Ramagundam",
    "Jagtial": "Jagtial",
    "Jagityal": "Jagtial",
    "Kothagudem": "Kothagudem",
    "Kothagudem": "Kothagudem",
    "Palwancha": "Palwancha",
    "Manuguru": "Kothagudem",
    "Bhadrachalam": "Bhadrachalam",
    "Hyderabad": "Hyderabad",
    "Secunderabad": "Secunderabad",
    "Secunderabd": "Secunderabad",
    "Bhagyanagar": "Hyderabad",
}

# City -> state, built once from STATE_CITIES.
_CITY_TO_STATE = {}
for _st, _cities in STATE_CITIES.items():
    for _c in _cities:
        # A city listed under two states keeps the first; that is noted by the
        # duplicate disappearing rather than silently overwriting.
        _CITY_TO_STATE.setdefault(_c, _st)


def _strip_parenthetical(raw):
    """Drop '(serves ...)' / '(advertising into ...)' notes."""
    out = []
    depth = 0
    for ch in raw:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif depth == 0:
            out.append(ch)
    return "".join(out).strip()


def _strip_pincode(part):
    """'Kothagudem 507101' -> 'Kothagudem'. Only a 6-digit group is removed."""
    words = [w for w in part.split() if not (w.isdigit() and len(w) == 6)]
    return " ".join(words).strip()


def normalize_city(raw):
    """Resolve a free-text city field to a canonical city, or '' if unknown.

    Returns '' rather than a guess when nothing matches - the caller reports
    it as unresolved so a human can decide, instead of the code deciding.
    """
    if not raw:
        return ""
    text = _strip_parenthetical(str(raw)).strip()
    if not text:
        return ""
    parts = [p.strip() for p in text.split(",") if p.strip()]
    if not parts:
        return ""
    # The last segment is the city; earlier segments are localities of it.
    for part in reversed(parts):
        cand = _strip_pincode(part)
        cand = CITY_ALIASES.get(cand, cand)
        if cand in _CITY_TO_STATE:
            return cand
        # A locality on its own: "Begumpet, Hyderabad" is handled above, but
        # "Begumpet" alone should still resolve.
        if cand in LOCALITIES:
            parent = LOCALITIES[cand]
            return CITY_ALIASES.get(parent, parent)
        # Try the whole remaining string, e.g. "Bandlaguda Jagir".
        joined = _strip_pincode(part)
        if joined in LOCALITIES:
            return LOCALITIES[joined]
    return ""


def city_state(city):
    """Canonical state for a city name, or None."""
    if not city:
        return None
    c = CITY_ALIASES.get(city, city)
    return _CITY_TO_STATE.get(c)


def in_state(raw_city, state):
    """(ok, reason). ok is True only when the city resolves inside `state`.

    A city that resolves to a DIFFERENT state is a rejection with a reason.
    A city that resolves to nothing is also a rejection - it is reported as
    unresolved rather than being waved through, because an unknown city is
    exactly how a Guntur or Bengaluru lead gets rowed by accident.
    """
    if not state:
        return True, "no state configured - city check skipped"
    city = normalize_city(raw_city)
    if not city:
        return False, ("city %r does not resolve to any known city - "
                       "add it to STATE_CITIES or LOCALITIES before "
                       "accepting this lead" % (raw_city,))
    st = city_state(city)
    if st is None:
        return False, ("city %r resolves to %r, which is not in STATE_CITIES"
                       % (raw_city, city))
    if st == state:
        return True, "%s is in %s" % (city, state)
    return False, "%s resolves to %s (%s), not %s" % (raw_city, city, st, state)


def cities_for(state):
    """Sorted city list for a state, for display."""
    return sorted(STATE_CITIES.get(state, ()))


def states():
    """All configured state names, sorted."""
    return sorted(STATE_CITIES)


def filter_leads(leads, state, city_of=None):
    """Split a leads mapping into (kept, rejected).

    `leads` is an OrderedDict of name -> ad (or any value). `city_of` is a
    callable name -> city string; when omitted the ad's own 'city' key is
    used, falling back to ''. Returns (kept, rejected) where rejected is a
    list of (name, city, reason), preserving input order.
    """
    if not state:
        return leads, []
    if city_of is None:
        def city_of(name, ad):
            if isinstance(ad, dict):
                return ad.get("city", "")
            return ""
    kept, rejected = {}, []
    for name, ad in leads.items():
        city = city_of(name, ad)
        ok, why = in_state(city, state)
        if ok:
            kept[name] = ad
        else:
            rejected.append((name, city, why))
    return kept, rejected


def check_rows(rows, state, city_key="city", name_key="name"):
    """Audit existing rows (e.g. leads.csv) against a state.

    Returns (inside, outside, unresolved) as lists of
    (identifier, city, reason). Use it to prove a configured state matches the
    pipeline before trusting it on new sweeps.
    """
    inside, outside, unresolved = [], [], []
    for r in rows:
        city = r.get(city_key, "") if isinstance(r, dict) else r[city_key]
        name = r.get(name_key, "") if isinstance(r, dict) else r[name_key]
        ok, why = in_state(city, state)
        if ok:
            inside.append((name, city, why))
        elif not normalize_city(city):
            unresolved.append((name, city, why))
        else:
            outside.append((name, city, why))
    return inside, outside, unresolved


if __name__ == "__main__":
    import sys
    print("Configured states: %d" % len(STATE_CITIES))
    print("Configured cities: %d" % len(_CITY_TO_STATE))
    print("Known localities: %d" % len(LOCALITIES))
    if len(sys.argv) > 1:
        st = " ".join(sys.argv[1:])
        if st not in STATE_CITIES:
            print("\n%r is not a configured state. Did you mean one of:" % st)
            for s in states():
                if st.lower()[:4] in s.lower():
                    print("   ", s)
            sys.exit(1)
        print("\n%s (%d cities):" % (st, len(cities_for(st))))
        for c in cities_for(st):
            print("   ", c)
