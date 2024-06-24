from dataclasses import dataclass


@dataclass
class Paginator:
    page: int = 1
    per_page: int = 20


