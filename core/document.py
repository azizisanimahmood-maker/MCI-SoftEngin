from __future__ import annotations

from typing import Iterable, Optional


class Document:
    """
    مدل مرکزی سند MCI SoftEngine.

    مسئولیت:
    - نگهداری Entityها
    - افزودن Entity
    - حذف Entity
    - دسترسی به Entity
    - پاک‌سازی سند
    """

    def __init__(self):
        self.entities = []

    # =====================================================
    # ADD
    # =====================================================

    def add_entity(self, entity):
        if entity is None:
            return None

        self.entities.append(entity)
        return entity

    # =====================================================
    # REMOVE
    # =====================================================

    def remove_entity(self, entity) -> bool:
        if entity not in self.entities:
            return False

        self.entities.remove(entity)
        return True

    # =====================================================
    # GET
    # =====================================================

    def get_entity(self, index: int):
        if index < 0 or index >= len(self.entities):
            return None

        return self.entities[index]

    # =====================================================
    # COUNT
    # =====================================================

    def entity_count(self) -> int:
        return len(self.entities)

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):
        self.entities.clear()

    # =====================================================
    # ITERATION
    # =====================================================

    def __iter__(self):
        return iter(self.entities)

    def __len__(self):
        return len(self.entities)

    def __getitem__(self, index):
        return self.entities[index]

    # =====================================================
    # SEARCH BY ID
    # =====================================================

    def find_by_id(self, entity_id: str):
        for entity in self.entities:
            if getattr(entity, "id", None) == entity_id:
                return entity

        return None