from langchain_core.tools import tool, Tool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper


 # Tool 1: Duck Duck Go API wrapper to search results online
ddg_search = DuckDuckGoSearchAPIWrapper()

@tool
def search(query: str) -> str:
    """searches the web for the provided query"""
    return ddg_search.run(query)


@tool
def legal_search(query: str) -> str:
    """Searches legal databases for the provided query"""
   
    legal_database = {
        "contract law": "Contract law in India is governed by the Indian Contract Act, 1872. Case: Mohori Bibee v. Dharmodas Ghose (1903).",
        "intellectual property": "Intellectual property law in India is protected under various statutes like the Indian Patents Act, 1970, and the Copyright Act, 1957. Case: R.G. Anand v. M/S Deluxe Films (1978).",
        "employment law": "Employment law in India includes statutes like the Industrial Disputes Act, 1947, and the Payment of Wages Act, 1936. Case: Bangalore Water Supply v. A Rajappa (1978).",
        "criminal law": "Criminal law in India is primarily governed by the Indian Penal Code (IPC), 1860. Case: State of Maharashtra v. Salman Salim Khan (2004).",
        "family law": "Family law in India covers various personal laws like the Hindu Marriage Act, 1955, and the Muslim Personal Law. Case: Shah Bano Case (1985)."
    }

    for keyword, result in legal_database.items():
        if keyword in query.lower():
            return f"Found result in legal database for '{keyword}': {result}"

    return f"No results found in the legal database for: {query}. Please refine your query."


@tool
def precedent_checker(case_description: str) -> str:
    """Checks for relevant legal precedents based on case description"""
    # Mock legal precedents database
    indian_precedents = {
      "contract breach": "Precedent: Nandganj Sihori Sugar Co. v. Badri Nath Dixit (1991) - Breach of contract by failing to deliver goods; damages awarded to the plaintiff.",
      "intellectual property theft": "Precedent: R.G. Anand v. Delux Films (1978) - The Supreme Court held that there was no copyright infringement, as the ideas were expressed differently.",
      "wrongful termination": "Precedent: Air India v. Nergesh Meerza (1981) - The Supreme Court ruled against the discriminatory termination of air hostesses on the basis of pregnancy.",
      "criminal defamation": "Precedent: Subramanian Swamy v. Union of India (2016) - The Supreme Court upheld the constitutional validity of criminal defamation under Sections 499 and 500 IPC.",
      "habeas corpus": "Precedent: ADM Jabalpur v. Shivkant Shukla (1976) - During the Emergency, the Supreme Court controversially ruled that citizens do not have the right to habeas corpus.",
      "fundamental rights": "Precedent: Kesavananda Bharati v. State of Kerala (1973) - The Supreme Court established the Basic Structure Doctrine, protecting the Constitution from arbitrary amendments.",
      "public interest litigation": "Precedent: S.P. Gupta v. Union of India (1981) - The court expanded the scope of Public Interest Litigation (PIL), allowing any public-spirited individual to approach the court.",
      "privacy rights": "Precedent: Justice K.S. Puttaswamy v. Union of India (2017) - The Supreme Court ruled that the right to privacy is a fundamental right under Article 21 of the Indian Constitution.",
      "reservation policies": "Precedent: Indra Sawhney v. Union of India (1992) - The Supreme Court upheld the reservation for Other Backward Classes (OBCs), but imposed a 50% cap on reservations.",
      "environmental law": "Precedent: M.C. Mehta v. Union of India (1986) - The Supreme Court introduced the concept of 'Absolute Liability' for industries engaged in hazardous activities.",
      "sexual harassment": "Precedent: Vishakha v. State of Rajasthan (1997) - The Supreme Court laid down guidelines for the prevention of sexual harassment at the workplace, known as the Vishakha Guidelines.",
      "property rights": "Precedent: Olga Tellis v. Bombay Municipal Corporation (1985) - The Supreme Court ruled that the right to livelihood is a part of the right to life under Article 21 of the Constitution.",
      "constitutional law": "Precedent: Golaknath v. State of Punjab (1967) - The Supreme Court ruled that Parliament cannot curtail any fundamental right guaranteed under the Constitution.",
      "censorship laws": "Precedent: Ramesh v. Union of India (1988) - The Supreme Court allowed the screening of a controversial TV series despite censorship challenges, citing freedom of speech and expression.",
      "dowry laws": "Precedent: Sushil Kumar Sharma v. Union of India (2005) - The court ruled that misuse of Section 498A (dowry harassment) cannot be ruled out, but the law itself is constitutional.",
      "child labor laws": "Precedent: M.C. Mehta v. State of Tamil Nadu (1996) - The court ruled against child labor and ordered the establishment of welfare funds for the rehabilitation of children involved in hazardous activities."
    }

    # Simulate checking for precedents based on keywords
    for keyword, result in indian_precedents.items():
        if keyword in case_description.lower():
            return f"Found relevant precedent: {result}"

    return f"No relevant precedents found for case description: {case_description[:100]}..."
