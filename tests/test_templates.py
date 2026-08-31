import unittest
import os
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "99 - Meta", "Template")

class TestTemplates(unittest.TestCase):
    def setUp(self):
        self.template_files = []
        for root, dirs, files in os.walk(TEMPLATE_DIR):
            for file in files:
                if file.endswith(".md"):
                    self.template_files.append(os.path.join(root, file))

    def test_all_templates_discovered(self):
        """Asserts that exactly 3 universal templates exist in 99 - Meta/Template/."""
        self.assertEqual(len(self.template_files), 3)

    def test_templates_no_static_frontmatter_prefix(self):
        """Asserts no template starts with a raw static YAML frontmatter block preceding Templater script per D-02."""
        for path in self.template_files:
            rel_path = os.path.relpath(path, PROJECT_ROOT)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().lstrip()

            # If template starts with ---, it must NOT be static YAML without <%
            if content.startswith("---"):
                # Must not be static hardcoded YAML before Templater block
                first_block = content.split("---")[1] if len(content.split("---")) > 1 else ""
                self.assertFalse(
                    "status: permanent" in first_block and "<%*" not in content.split("---")[0],
                    f"Template {rel_path} contains hardcoded static frontmatter prefix preceding Templater block."
                )

    def test_templates_have_dynamic_templater_block(self):
        """Asserts all interactive templates contain dynamic Templater script <%* per D-01, D-03."""
        for path in self.template_files:
            rel_path = os.path.relpath(path, PROJECT_ROOT)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn("<%*", content, f"Template {rel_path} is missing dynamic Templater block <%*")
            self.assertIn("tR +=", content, f"Template {rel_path} is missing tR += output construction")

    def test_templates_construct_canonical_frontmatter(self):
        """Asserts all permanent and blog templates generate canonical YAML frontmatter strings per D-01."""
        canonical_fields = ["type:", "area:", "related:", "aliases:", "source:", "title:", "date:", "updated:", "tags:", "summary:"]
        for path in self.template_files:
            rel_path = os.path.relpath(path, PROJECT_ROOT)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            if "Raw Inbox Note.md" in rel_path:
                self.assertIn("ready:", content)
                self.assertIn("title:", content)
                self.assertIn("date:", content)
                self.assertIn("tags:", content)
                continue

            for field in canonical_fields:
                self.assertIn(field, content, f"Template {rel_path} is missing canonical field {field}")

            # Status (Atlas/Meta/Inbox) or Stage+Draft (Blog)
            if "Blog" in rel_path:
                self.assertIn("stage:", content, f"Blog template {rel_path} missing stage field")
                self.assertIn("draft:", content, f"Blog template {rel_path} missing draft field")
            else:
                self.assertIn("status:", content, f"Template {rel_path} missing status field")

    def test_templates_have_breadcrumbs_and_no_collegamenti(self):
        """Asserts all templates construct standard breadcrumbs and have NO ## Collegamenti section."""
        for path in self.template_files:
            rel_path = os.path.relpath(path, PROJECT_ROOT)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn("[[Home MOC|Home]]", content, f"Template {rel_path} missing standard Home breadcrumb")
            self.assertNotIn("## Collegamenti", content, f"Template {rel_path} contains unexpected ## Collegamenti section")

    def test_templates_have_no_heading_emojis(self):
        """Asserts no template includes emojis in markdown headings."""
        for path in self.template_files:
            rel_path = os.path.relpath(path, PROJECT_ROOT)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertFalse(
                re.search(r'^#{1,6}\s+[\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff]', content, re.MULTILINE),
                f"Template {rel_path} contains emoji in heading."
            )

    def test_templates_target_folders_exist(self):
        """Asserts all static targetFolder strings defined in templates point to existing directories in the vault."""
        for path in self.template_files:
            rel_path = os.path.relpath(path, PROJECT_ROOT)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            matches = re.findall(r'targetFolder\s*=\s*["\']([^"\']+)["\']', content)
            for target_folder in matches:
                full_target = os.path.join(PROJECT_ROOT, target_folder)
                self.assertTrue(
                    os.path.isdir(full_target),
                    f"Template {rel_path} references non-existent target folder '{target_folder}'."
                )

    def test_raw_inbox_note_youtube_validation(self):
        """Asserts Raw Inbox Note template contains robust YouTube URL validation regex and user notification."""
        raw_inbox_path = os.path.join(TEMPLATE_DIR, "Raw Inbox Note.md")
        with open(raw_inbox_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("ytRegex", content)
        self.assertIn("Notice", content)
        
        # Test the regex against valid and invalid URLs
        regex_match = re.search(r'const ytRegex = (\/.*?\/[a-z]*);', content)
        self.assertIsNotNone(regex_match, "ytRegex definition not found in Raw Inbox Note.md")
        
        # Extract python-compatible regex
        js_regex_str = regex_match.group(1).strip('/')
        # Remove trailing regex flags like 'i'
        flags = re.IGNORECASE if js_regex_str.endswith('i') or regex_match.group(1).endswith('/i') else 0
        cleaned_pattern = re.sub(r'\/[a-z]*$', '', regex_match.group(1)).lstrip('/')
        
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/watch?feature=shared&v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ?t=42",
            "https://www.youtube.com/shorts/dQw4w9WgXcQ",
            "https://youtube.com/shorts/dQw4w9WgXcQ",
            "https://www.youtube.com/live/dQw4w9WgXcQ",
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "www.youtube.com/watch?v=dQw4w9WgXcQ",
            "youtube.com/watch?v=dQw4w9WgXcQ"
        ]
        
        invalid_urls = [
            "https://google.com",
            "https://vimeo.com/123456789",
            "https://github.com/loackyPKM",
            "https://notyoutube.com/watch?v=dQw4w9WgXcQ",
            "not a url",
            "https://youtube.com/about"
        ]
        
        for url in valid_urls:
            self.assertTrue(
                bool(re.search(cleaned_pattern, url, flags)),
                f"Valid YouTube URL failed validation: {url}"
            )
            
        for url in invalid_urls:
            self.assertFalse(
                bool(re.search(cleaned_pattern, url, flags)),
                f"Invalid YouTube URL unexpectedly passed validation: {url}"
            )

    def test_templates_handle_esc_cancellation(self):
        """Asserts all interactive templates define cancelCreation logic to abort without creating notes on ESC."""
        for path in self.template_files:
            rel_path = os.path.relpath(path, PROJECT_ROOT)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn("cancelCreation", content, f"Template {rel_path} missing cancelCreation helper.")
            self.assertIn("app.vault.trash", content, f"Template {rel_path} missing app.vault.trash call for clean abort.")

if __name__ == "__main__":
    unittest.main()
