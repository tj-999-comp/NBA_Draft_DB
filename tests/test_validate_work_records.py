import tempfile
import unittest
from pathlib import Path

from scripts.validate_work_records import PROJECT_ID, validate


class WorkRecordValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name) / "work-records"
        (self.root / "md").mkdir(parents=True)
        (self.root / "metadata").mkdir()

    def tearDown(self):
        self.tempdir.cleanup()

    def write_record(self, basename="work_record_001", *, publish=False, project_id=PROJECT_ID):
        (self.root / "md" / f"{basename}.md").write_text("# 作業記録\n", encoding="utf-8")
        (self.root / "metadata" / f"{basename}.yml").write_text(
            "schema_version: 1\n"
            "title: 検証用作業記録\n"
            'date: "2026-08-30"\n'
            f"project_id: {project_id}\n"
            "tags:\n"
            "  - validation\n"
            f"publish: {'true' if publish else 'false'}\n",
            encoding="utf-8",
        )

    def test_valid_record_and_publish_target(self):
        self.write_record(publish=True)
        self.assertEqual(validate(self.root), [])
        self.assertEqual(
            validate(self.root, target_basename="work_record_001", require_publish=True), []
        )

    def test_unpublished_record_is_valid_but_not_publishable(self):
        self.write_record()
        self.assertEqual(validate(self.root), [])
        errors = validate(self.root, target_basename="work_record_001", require_publish=True)
        self.assertTrue(any("publish: true" in error for error in errors))

    def test_markdown_and_metadata_must_pair(self):
        (self.root / "md" / "work_record_001.md").write_text("# record\n", encoding="utf-8")
        self.assertTrue(any("one-to-one" in error for error in validate(self.root)))

    def test_rejects_unknown_metadata_and_duplicate_keys(self):
        self.write_record()
        metadata = self.root / "metadata" / "work_record_001.yml"
        metadata.write_text(
            "schema_version: 1\n"
            "title: title\n"
            "date: 2026-08-30\n"
            "project_id: NBA_Draft_DB\n"
            "tags:\n"
            "  - validation\n"
            "publish: false\n"
            "owner: someone\n"
            "title: duplicate\n",
            encoding="utf-8",
        )
        errors = validate(self.root)
        self.assertTrue(any("invalid metadata" in error for error in errors))

    def test_rejects_invalid_date_project_and_publish_type(self):
        self.write_record(project_id="other-project")
        metadata = self.root / "metadata" / "work_record_001.yml"
        metadata.write_text(
            "schema_version: 1\n"
            "title: title\n"
            'date: "2026-02-30"\n'
            "project_id: other-project\n"
            "tags: []\n"
            "publish: yes\n",
            encoding="utf-8",
        )
        errors = validate(self.root)
        self.assertTrue(any("invalid metadata" in error for error in errors))

    def test_rejects_rule_out_names_and_out_of_range_numbers(self):
        self.write_record("work_record_000")
        (self.root / "md" / "record_002.md").write_text("# invalid\n", encoding="utf-8")
        (self.root / "metadata" / "work_record_000.yml").unlink()
        errors = validate(self.root)
        self.assertGreaterEqual(len(errors), 2)
        self.assertTrue(any("work_record_001 through work_record_999" in error for error in errors))

    def test_rejects_unexpected_files_and_directories(self):
        self.write_record()
        (self.root / "README.md").write_text("not a support file\n", encoding="utf-8")
        (self.root / "md" / "nested").mkdir()
        errors = validate(self.root)
        self.assertTrue(any("unexpected file or directory" in error for error in errors))
        self.assertTrue(any("only regular record files" in error for error in errors))

    def test_target_must_be_fixed_basename_and_exist(self):
        self.write_record(publish=True)
        errors = validate(self.root, target_basename="work_record_01", require_publish=True)
        self.assertTrue(any("target_basename" in error for error in errors))
        errors = validate(self.root, target_basename="work_record_002", require_publish=True)
        self.assertTrue(any("both Markdown and metadata" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
