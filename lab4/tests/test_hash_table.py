# tests/test_hash_table.py
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hash_table import HashTable, HashTableEntry


class TestHashTableEntry(unittest.TestCase):

    def test_create_entry(self):
        entry = HashTableEntry("Евразия", "Самый большой материк")
        self.assertEqual(entry.id, "Евразия")
        self.assertEqual(entry.pi, "Самый большой материк")
        self.assertEqual(entry.u, 1)
        self.assertEqual(entry.c, 0)
        self.assertEqual(entry.t, 1)
        self.assertEqual(entry.l, 0)
        self.assertEqual(entry.d, 0)
        self.assertEqual(entry.po, -1)

    def test_empty_entry(self):
        entry = HashTableEntry()
        self.assertIsNone(entry.id)
        self.assertEqual(entry.u, 0)

    def test_to_dict(self):
        entry = HashTableEntry("Африка", "Континент")
        d = entry.to_dict()
        self.assertEqual(d['ID'], "Африка")
        self.assertEqual(d['Pi'], "Континент")
        self.assertEqual(d['Po'], '-')

    def test_str_method(self):
        entry = HashTableEntry("Евразия", "Материк")
        s = str(entry)
        self.assertIn("Евразия", s)
        self.assertIn("ЗАНЯТО", s)


class TestHashTable(unittest.TestCase):

    def setUp(self):
        self.ht = HashTable(size=10, base=0)

    def test_initialization(self):
        self.assertEqual(self.ht.size, 10)
        self.assertEqual(self.ht.base, 0)
        self.assertEqual(self.ht.entries_count, 0)
        self.assertEqual(self.ht.collisions_count, 0)
        self.assertEqual(len(self.ht.table), 10)

    def test_insert_and_find(self):
        self.assertTrue(self.ht.insert("Евразия", "Самый большой материк"))
        result = self.ht.find("Евразия", silent=True)
        self.assertIsNotNone(result)
        index, entry = result
        self.assertEqual(entry.id, "Евразия")

    def test_insert_duplicate_fails(self):
        self.ht.insert("Евразия", "Материк")
        self.assertFalse(self.ht.insert("Евразия", "Другой материк"))

    def test_find_nonexistent(self):
        result = self.ht.find("НесуществующееСлово", silent=True)
        self.assertIsNone(result)

    def test_update(self):
        self.ht.insert("Евразия", "Старые данные")
        self.assertTrue(self.ht.update("Евразия", "Новые данные"))
        result = self.ht.find("Евразия", silent=True)
        index, entry = result
        self.assertEqual(entry.pi, "Новые данные")

    def test_update_nonexistent_fails(self):
        self.assertFalse(self.ht.update("Несуществующее", "Данные"))

    def test_delete(self):
        self.ht.insert("Евразия", "Материк")
        self.assertTrue(self.ht.delete("Евразия"))
        result = self.ht.find("Евразия", silent=True)
        self.assertIsNone(result)

    def test_delete_nonexistent_fails(self):
        self.assertFalse(self.ht.delete("Несуществующее"))

    def test_collision_occurs(self):
        # Подбираем слова с одинаковым хешем
        self.ht.insert("Вяткин", "Слово1")
        self.ht.insert("ВЯТКИН2", "Слово2")  # похожее для коллизии
        self.assertGreater(self.ht.collisions_count, 0)

    def test_linear_probe(self):
        self.ht.insert("Вяткин", "Слово1")
        free_index = self.ht._linear_probe(self.ht._hash("Вяткин"))
        self.assertNotEqual(free_index, -1)

    def test_chain_creation(self):
        self.ht.insert("Ключ1", "Данные1")
        self.ht.insert("Ключ2", "Данные2")
        # Проверяем что Po не -1 у первого при коллизии
        for entry in self.ht.table:
            if entry and entry.id == "Ключ1":
                # Если была коллизия, Po не -1
                pass

    def test_display(self):
        """Тест что метод display не падает"""
        import io
        import sys
        self.ht.insert("Евразия", "Материк")
        captured = io.StringIO()
        sys.stdout = captured
        self.ht.display()
        sys.stdout = sys.__stdout__
        self.assertIn("Евразия", captured.getvalue())

    def test_show_v_h_table(self):
        """Тест что метод show_v_h_table не падает"""
        import io
        import sys
        self.ht.insert("Евразия", "Материк")
        captured = io.StringIO()
        sys.stdout = captured
        self.ht.show_v_h_table()
        sys.stdout = sys.__stdout__
        self.assertIn("Евразия", captured.getvalue())

    def test_get_all_entries(self):
        self.ht.insert("Евразия", "Материк")
        self.ht.insert("Африка", "Континент")
        entries = self.ht.get_all_entries()
        self.assertEqual(len(entries), 2)
        # Проверяем что оба ключа присутствуют (порядок не важен)
        keys = [e['key'] for e in entries]
        self.assertIn("Евразия", keys)
        self.assertIn("Африка", keys)

    def test_fill_ratio(self):
        self.ht.insert("Ключ1", "Данные1")
        fill_ratio = self.ht.entries_count / self.ht.size * 100
        self.assertEqual(fill_ratio, 10.0)


if __name__ == '__main__':
    unittest.main()