#!/usr/bin/env python3
"""Export ClasseViva data into a TXT study context grouped by subject."""

import argparse
import datetime
import json
import logging
import os
import re
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import requests


BASE_URL = "https://web.spaggiari.eu/rest/v1"
API_KEY = "Tg1NWEwNGIgIC0K"
USER_AGENT = "CVVS/std/4.1.7 Android/10"

SUBJECT_UNKNOWN = "MATERIA_NON_SPECIFICATA"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def build_headers(token: Optional[str] = None) -> Dict[str, str]:
    """Build HTTP headers for ClasseViva API calls."""
    headers = {
        "Content-Type": "application/json",
        "Z-Dev-ApiKey": API_KEY,
        "User-Agent": USER_AGENT,
    }
    if token:
        headers["Z-Auth-Token"] = token
    return headers


def request_json(
    method: str,
    url: str,
    token: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    """Execute an HTTP request and return parsed JSON."""
    response = requests.request(
        method=method,
        url=url,
        headers=build_headers(token),
        json=payload,
        timeout=timeout,
    )
    if response.status_code >= 400:
        logger.error("API request failed: %s %s -> %s", method, url, response.status_code)
        logger.error("Response: %s", response.text)
        response.raise_for_status()

    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError(f"Invalid JSON response from {url}") from exc


def parse_yyyymmdd(value: str) -> datetime.date:
    """Parse a YYYYMMDD date string."""
    return datetime.datetime.strptime(value, "%Y%m%d").date()


def validate_range(start: str, end: str) -> Tuple[str, str]:
    """Validate start/end date strings in YYYYMMDD format."""
    start_date = parse_yyyymmdd(start)
    end_date = parse_yyyymmdd(end)
    if end_date < start_date:
        raise ValueError("End date must be greater than or equal to start date")
    return start, end


def get_config_path(explicit_path: Optional[str] = None) -> str:
    """Resolve config path for local or Docker execution."""
    if explicit_path:
        return explicit_path
    if os.path.isdir("/app"):
        return "/app/config.json"
    # Default to config.json in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "config.json")


def get_default_output_path() -> str:
    """Resolve default output path (list.md) relative to the script."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "list.md")


def load_config(config_path: str) -> Dict[str, Any]:
    """Load JSON configuration from file."""
    try:
        with open(config_path, "r", encoding="utf-8") as config_file:
            return json.load(config_file)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Configuration file not found: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in config file: {config_path}") from exc


def extract_student_id(user_id: str) -> str:
    """Extract numeric student ID from ClasseViva user ID."""
    student_id = "".join(filter(str.isdigit, user_id))
    if not student_id:
        raise RuntimeError("Could not extract student_id from user_id")
    return student_id


def login(user_id: str, user_pass: str, timeout: int) -> Dict[str, Any]:
    """Authenticate against ClasseViva API."""
    return request_json(
        method="POST",
        url=f"{BASE_URL}/auth/login",
        payload={"ident": None, "pass": user_pass, "uid": user_id},
        timeout=timeout,
    )


def get_periods(student_id: str, token: str, timeout: int) -> List[Dict[str, Any]]:
    """Fetch school periods from ClasseViva."""
    data = request_json(
        method="GET",
        url=f"{BASE_URL}/students/{student_id}/periods",
        token=token,
        timeout=timeout,
    )
    return data.get("periods", [])


def resolve_date_range(
    student_id: str,
    token: str,
    timeout: int,
    start: Optional[str],
    end: Optional[str],
) -> Tuple[str, str]:
    """Resolve date range either from args or from full school periods."""
    if start or end:
        if not start or not end:
            raise ValueError("Both --start and --end are required when one is provided")
        return validate_range(start, end)

    periods = get_periods(student_id, token, timeout)
    if not periods:
        raise RuntimeError("No school periods found and no explicit date range provided")

    starts = [item.get("dateStart") for item in periods if item.get("dateStart")]
    ends = [item.get("dateEnd") for item in periods if item.get("dateEnd")]
    if not starts or not ends:
        raise RuntimeError("Could not determine date range from periods")

    first_day = min(starts).replace("-", "")
    last_day = max(ends).replace("-", "")
    return validate_range(first_day, last_day)


def get_agenda(student_id: str, token: str, start: str, end: str, timeout: int) -> List[Dict[str, Any]]:
    """Fetch agenda events for date range."""
    data = request_json(
        method="GET",
        url=f"{BASE_URL}/students/{student_id}/agenda/all/{start}/{end}",
        token=token,
        timeout=timeout,
    )
    return data.get("agenda", [])


def get_lessons(student_id: str, token: str, start: str, end: str, timeout: int) -> List[Dict[str, Any]]:
    """Fetch lessons for date range."""
    data = request_json(
        method="GET",
        url=f"{BASE_URL}/students/{student_id}/lessons/{start}/{end}",
        token=token,
        timeout=timeout,
    )
    return data.get("lessons", [])


def get_didactics(student_id: str, token: str, timeout: int) -> List[Dict[str, Any]]:
    """Fetch didactics tree from ClasseViva."""
    data = request_json(
        method="GET",
        url=f"{BASE_URL}/students/{student_id}/didactics",
        token=token,
        timeout=timeout,
    )
    if "didacticts" in data:
        return data.get("didacticts", [])
    return data.get("didactics", [])


def get_didactics_item(student_id: str, token: str, content_id: int, timeout: int) -> Dict[str, Any]:
    """Fetch didactics item metadata/details without downloading large bodies."""
    url = f"{BASE_URL}/students/{student_id}/didactics/item/{content_id}"
    response = requests.get(
        url=url,
        headers=build_headers(token),
        timeout=timeout,
        allow_redirects=True,
        stream=True,
    )

    try:
        if response.status_code >= 400:
            logger.error("API request failed: GET %s -> %s", url, response.status_code)
            logger.error("Response headers: %s", dict(response.headers))
            response.raise_for_status()

        content_type = (response.headers.get("Content-Type") or "").lower()
        detail: Dict[str, Any] = {
            "_final_url": response.url,
            "_content_type": content_type,
            "_content_length": response.headers.get("Content-Length", ""),
        }

        location = response.headers.get("Location")
        if location:
            detail["_location"] = location

        if "application/json" in content_type:
            try:
                payload = response.json()
                detail["payload"] = payload
            except ValueError:
                # Keep metadata-only result if payload isn't valid JSON.
                pass

        return detail
    finally:
        response.close()


def clean_text(value: Any) -> str:
    """Return a safe one-line text value."""
    if value is None:
        return ""
    text = str(value).strip()
    return re.sub(r"\s+", " ", text)


def clean_subject(value: Any) -> str:
    """Normalize subject value."""
    text = clean_text(value)
    return text if text else SUBJECT_UNKNOWN


def iter_strings(data: Any) -> Iterable[str]:
    """Yield all string values found in nested JSON-like structures."""
    if isinstance(data, str):
        yield data
        return

    if isinstance(data, dict):
        for value in data.values():
            yield from iter_strings(value)
        return

    if isinstance(data, list):
        for item in data:
            yield from iter_strings(item)


def extract_links(data: Any) -> List[str]:
    """Extract and deduplicate URLs from nested objects."""
    links: Set[str] = set()
    url_pattern = re.compile(r"https?://[^\s\"'<>]+")

    for text in iter_strings(data):
        for match in url_pattern.findall(text):
            links.add(match)

    return sorted(links)


def find_values_by_keys(data: Any, keys: Set[str]) -> List[str]:
    """Collect string values for specific keys across nested objects."""
    matches: List[str] = []

    if isinstance(data, dict):
        for key, value in data.items():
            if key.lower() in keys and isinstance(value, str) and value.strip():
                matches.append(value.strip())
            matches.extend(find_values_by_keys(value, keys))
    elif isinstance(data, list):
        for item in data:
            matches.extend(find_values_by_keys(item, keys))

    return matches


def infer_subject_from_candidates(candidates: Iterable[str], known_subjects: Set[str]) -> Optional[str]:
    """Infer the closest subject from known subjects based on candidate texts."""
    normalized_subjects = sorted(known_subjects, key=lambda subject: len(subject), reverse=True)

    for candidate in candidates:
        lower_candidate = candidate.lower()
        for subject in normalized_subjects:
            if subject.lower() in lower_candidate:
                return subject
    return None


def build_subject_buckets(
    agenda: List[Dict[str, Any]],
    lessons: List[Dict[str, Any]],
    didactics: List[Dict[str, Any]],
    student_id: str,
    token: str,
    timeout: int,
    include_material_details: bool,
) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """Group agenda, lessons, and didactics by subject."""
    buckets: Dict[str, Dict[str, List[Dict[str, Any]]]] = defaultdict(
        lambda: {"agenda": [], "lessons": [], "materials": []}
    )

    known_subjects: Set[str] = set()
    teacher_subject_counts: Dict[str, Counter[str]] = defaultdict(Counter)

    for event in agenda:
        subject = clean_subject(event.get("subjectDesc"))
        author = clean_text(event.get("authorName"))
        known_subjects.add(subject)
        if author and subject != SUBJECT_UNKNOWN:
            teacher_subject_counts[author][subject] += 1
        buckets[subject]["agenda"].append(
            {
                "start": clean_text(event.get("evtDatetimeBegin")),
                "end": clean_text(event.get("evtDatetimeEnd")),
                "notes": clean_text(event.get("notes")),
                "author": author,
                "class": clean_text(event.get("classDesc")),
            }
        )

    for lesson in lessons:
        subject = clean_subject(lesson.get("subjectDesc"))
        author = clean_text(lesson.get("authorName"))
        known_subjects.add(subject)
        if author and subject != SUBJECT_UNKNOWN:
            teacher_subject_counts[author][subject] += 1
        buckets[subject]["lessons"].append(
            {
                "date": clean_text(lesson.get("evtDate")),
                "type": clean_text(lesson.get("lessonType")),
                "arg": clean_text(lesson.get("lessonArg")),
                "author": author,
                "class": clean_text(lesson.get("classDesc")),
            }
        )

    teacher_subject_map: Dict[str, str] = {}
    for teacher, counter in teacher_subject_counts.items():
        most_common = counter.most_common(1)
        if most_common:
            teacher_subject_map[teacher] = most_common[0][0]

    seen_material_ids: Set[int] = set()

    for teacher_block in didactics:
        teacher_name = clean_text(teacher_block.get("teacherName"))
        folders = teacher_block.get("folders", [])
        if not isinstance(folders, list):
            continue

        for folder in folders:
            folder_name = clean_text(folder.get("folderName"))
            contents = folder.get("contents", [])
            if not isinstance(contents, list):
                continue

            for content in contents:
                content_id_raw = content.get("contentId")
                try:
                    content_id = int(content_id_raw)
                except (TypeError, ValueError):
                    continue
                if content_id in seen_material_ids:
                    continue
                seen_material_ids.add(content_id)

                content_name = clean_text(content.get("contentName"))
                share_dt = clean_text(content.get("shareDT"))
                object_type = clean_text(content.get("objectType"))
                object_id = clean_text(content.get("objectId"))

                detail: Dict[str, Any] = {}
                if include_material_details:
                    try:
                        detail = get_didactics_item(
                            student_id=student_id,
                            token=token,
                            content_id=content_id,
                            timeout=timeout,
                        )
                    except requests.RequestException as exc:
                        logger.warning(
                            "Skipping didactics detail for content %s due to API error: %s",
                            content_id,
                            exc,
                        )

                links = extract_links({"content": content, "detail": detail})

                explicit_subject_candidates = find_values_by_keys(
                    detail,
                    {
                        "subject",
                        "subjectdesc",
                        "subjectname",
                        "materia",
                        "materiadesc",
                        "classsubject",
                    },
                )

                explicit_subject = None
                if explicit_subject_candidates:
                    explicit_subject = clean_subject(explicit_subject_candidates[0])

                inferred_subject = infer_subject_from_candidates(
                    [folder_name, content_name, teacher_name] + explicit_subject_candidates,
                    known_subjects,
                )
                teacher_subject = teacher_subject_map.get(teacher_name)

                subject = explicit_subject or inferred_subject or teacher_subject or SUBJECT_UNKNOWN
                buckets[subject]["materials"].append(
                    {
                        "name": content_name,
                        "id": content_id,
                        "object_id": object_id,
                        "folder": folder_name,
                        "teacher": teacher_name,
                        "share": share_dt,
                        "type": object_type,
                        "links": links,
                    }
                )

    for subject in buckets:
        buckets[subject]["agenda"].sort(key=lambda item: item.get("start", ""))
        buckets[subject]["lessons"].sort(key=lambda item: item.get("date", ""))
        buckets[subject]["materials"].sort(key=lambda item: item.get("name", ""))

    return buckets


def format_report(
    buckets: Dict[str, Dict[str, List[Dict[str, Any]]]],
    start: str,
    end: str,
) -> str:
    """Create TXT report content grouped by subject."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: List[str] = []

    lines.append("CVV STUDY CONTEXT EXPORT")
    lines.append(f"Generated at: {now}")
    lines.append(f"Agenda/Lessons range: {start} -> {end}")
    lines.append(f"Subjects found: {len(buckets)}")
    lines.append("")

    for subject in sorted(buckets.keys()):
        data = buckets[subject]
        lines.append("=" * 72)
        lines.append(f"MATERIA: {subject}")
        lines.append("=" * 72)
        lines.append("")

        lines.append(f"[AGENDA] ({len(data['agenda'])} eventi)")
        if data["agenda"]:
            for event in data["agenda"]:
                lines.append(
                    "- "
                    f"{event['start']} -> {event['end']} | "
                    f"{event['notes'] or 'Senza note'}"
                )
                lines.append(f"  Docente: {event['author'] or 'N/A'}")
                lines.append(f"  Classe: {event['class'] or 'N/A'}")
        else:
            lines.append("- Nessun evento agenda")
        lines.append("")

        lines.append(f"[LEZIONI SVOLTE] ({len(data['lessons'])} lezioni)")
        if data["lessons"]:
            for lesson in data["lessons"]:
                lines.append(
                    "- "
                    f"{lesson['date']} | "
                    f"{lesson['type'] or 'Lezione'} | "
                    f"{lesson['arg'] or 'Argomento non disponibile'}"
                )
                lines.append(f"  Docente: {lesson['author'] or 'N/A'}")
                lines.append(f"  Classe: {lesson['class'] or 'N/A'}")
        else:
            lines.append("- Nessuna lezione")
        lines.append("")

        lines.append(f"[MATERIALE DIDATTICO] ({len(data['materials'])} elementi)")
        if data["materials"]:
            for material in data["materials"]:
                lines.append(
                    "- "
                    f"{material['name'] or 'Senza nome'} "
                    f"(contentId={material['id']}, objectId={material['object_id'] or 'N/A'}, type={material['type'] or 'N/A'})"
                )
                lines.append(f"  Cartella: {material['folder'] or 'N/A'}")
                lines.append(f"  Docente: {material['teacher'] or 'N/A'}")
                lines.append(f"  Condiviso: {material['share'] or 'N/A'}")
                if material["links"]:
                    for link in material["links"]:
                        lines.append(f"  Link: {link}")
                elif (material["type"] or "").lower() == "link" and material["object_id"]:
                    lines.append(f"  Link: riferimento interno objectId={material['object_id']}")
                else:
                    lines.append("  Link: non disponibile")
        else:
            lines.append("- Nessun materiale")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def write_report(output_path: str, content: str) -> None:
    """Write report to TXT file."""
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(content)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Export agenda, lessons and didactic materials from ClasseViva into a TXT file"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to config.json (default: /app/config.json in Docker, otherwise ./config.json)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=get_default_output_path(),
        help=f"Output path (default: {get_default_output_path()})",
    )
    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help="Start date in YYYYMMDD. If omitted, first period dateStart is used.",
    )
    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="End date in YYYYMMDD. If omitted, last period dateEnd is used.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="HTTP timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--include-material-details",
        action="store_true",
        help="Also call didactics/item endpoint to try extracting additional links (slower)",
    )
    return parser.parse_args()


def main() -> int:
    """Script entrypoint."""
    args = parse_args()
    logger.info("=== Study Context Export Start ===")

    config_path = get_config_path(args.config)
    config = load_config(config_path)

    user_id = config.get("user_id")
    user_pass = config.get("user_pass")
    if not user_id or not user_pass:
        raise RuntimeError("Missing user_id or user_pass in config")

    student_id = extract_student_id(user_id)
    logger.info("Student ID resolved: %s", student_id)

    login_response = login(user_id, user_pass, timeout=args.timeout)
    token = login_response.get("token")
    if not token:
        raise RuntimeError("Login succeeded but token is missing")
    logger.info(
        "Logged in as %s %s",
        clean_text(login_response.get("firstName")),
        clean_text(login_response.get("lastName")),
    )

    start, end = resolve_date_range(
        student_id=student_id,
        token=token,
        timeout=args.timeout,
        start=args.start,
        end=args.end,
    )
    logger.info("Date range selected: %s -> %s", start, end)

    agenda = get_agenda(student_id=student_id, token=token, start=start, end=end, timeout=args.timeout)
    lessons = get_lessons(student_id=student_id, token=token, start=start, end=end, timeout=args.timeout)
    didactics = get_didactics(student_id=student_id, token=token, timeout=args.timeout)

    logger.info("Fetched agenda events: %d", len(agenda))
    logger.info("Fetched lessons: %d", len(lessons))
    logger.info("Fetched didactics teacher blocks: %d", len(didactics))
    if not args.include_material_details:
        logger.info("Material detail endpoint disabled (default). Use --include-material-details to enable it.")

    buckets = build_subject_buckets(
        agenda=agenda,
        lessons=lessons,
        didactics=didactics,
        student_id=student_id,
        token=token,
        timeout=args.timeout,
        include_material_details=args.include_material_details,
    )

    report = format_report(buckets=buckets, start=start, end=end)
    write_report(args.output, report)
    logger.info("Study context written to: %s", args.output)
    logger.info("=== Study Context Export Completed ===")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except requests.RequestException as exc:
        logger.error("Network/API error: %s", exc, exc_info=True)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        logger.error("Unexpected error: %s", exc, exc_info=True)
        sys.exit(1)