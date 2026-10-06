#!/usr/bin/env python3
"""Build a lightweight project inventory and audit-mode recommendations."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "target",
    "out",
    "coverage",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".turbo",
    ".cache",
}

LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".ipynb": "Jupyter Notebook",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".mts": "TypeScript",
    ".cts": "TypeScript",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".rs": "Rust",
    ".go": "Go",
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".scala": "Scala",
    ".swift": "Swift",
    ".m": "Objective-C",
    ".mm": "Objective-C++",
    ".c": "C",
    ".h": "C/C++ Header",
    ".cc": "C++",
    ".cpp": "C++",
    ".cxx": "C++",
    ".hpp": "C++ Header",
    ".cs": "C#",
    ".fs": "F#",
    ".php": "PHP",
    ".rb": "Ruby",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".erl": "Erlang",
    ".hrl": "Erlang",
    ".dart": "Dart",
    ".r": "R",
    ".R": "R",
    ".lua": "Lua",
    ".pl": "Perl",
    ".pm": "Perl",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".fish": "Shell",
    ".ps1": "PowerShell",
    ".sql": "SQL",
    ".tf": "Terraform",
    ".tfvars": "Terraform",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".json": "JSON",
    ".toml": "TOML",
    ".xml": "XML",
    ".md": "Markdown",
}

SPECIAL_LANGUAGE_FILES = {
    "Dockerfile": "Dockerfile",
    "Makefile": "Makefile",
    "Rakefile": "Ruby",
    "Gemfile": "Ruby",
    "go.mod": "Go",
    "Cargo.toml": "Rust",
    "pyproject.toml": "Python",
    "requirements.txt": "Python",
    "package.json": "JavaScript/TypeScript",
    "composer.json": "PHP",
    "mix.exs": "Elixir",
    "pubspec.yaml": "Dart",
}

MANIFEST_NAMES = {
    "package.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "package-lock.json",
    "bun.lockb",
    "deno.json",
    "tsconfig.json",
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "poetry.lock",
    "Pipfile",
    "Cargo.toml",
    "Cargo.lock",
    "go.mod",
    "go.sum",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "composer.json",
    "composer.lock",
    "Gemfile",
    "Gemfile.lock",
    "mix.exs",
    "mix.lock",
    "pubspec.yaml",
    "pubspec.lock",
    "Package.swift",
    "*.csproj",
    "*.fsproj",
    "*.sln",
}

SURFACE_LABELS = {
    "frontend": {"zh": "前端 / 浏览器 UI", "en": "Frontend / browser UI"},
    "backend_api": {"zh": "后端 API / 服务端接口", "en": "Backend API / server endpoints"},
    "database": {"zh": "数据库 / 迁移 / 持久化", "en": "Database / migrations / persistence"},
    "ai_llm": {"zh": "AI / LLM / RAG", "en": "AI / LLM / RAG"},
    "mobile": {"zh": "移动端", "en": "Mobile app"},
    "desktop": {"zh": "桌面端", "en": "Desktop app"},
    "cli": {"zh": "CLI / 脚本工具", "en": "CLI / scripting tool"},
    "ci": {"zh": "CI/CD", "en": "CI/CD"},
    "deployment": {"zh": "部署 / 容器 / 基础设施", "en": "Deployment / containers / infrastructure"},
    "docs": {"zh": "文档", "en": "Documentation"},
    "tests": {"zh": "测试", "en": "Tests"},
    "auth": {"zh": "认证 / 授权", "en": "Authentication / authorization"},
    "privacy": {"zh": "隐私 / 个人数据", "en": "Privacy / personal data"},
}


def iter_files(root: Path, max_files: int) -> list[Path]:
    if max_files < 1:
        raise ValueError("max_files must be positive")
    files: list[Path] = []
    # Prune before descending; materializing rglob would still traverse caches
    # and dependencies before applying either exclusions or the file limit.
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in EXCLUDED_DIRS)
        for name in sorted(names):
            path = Path(directory) / name
            if path.is_symlink() or not path.is_file():
                continue
            files.append(path)
            if len(files) >= max_files:
                return files
    return files


def read_text(path: Path, limit: int = 200_000) -> str:
    try:
        with path.open(encoding="utf-8", errors="ignore") as stream:
            return stream.read(limit)
    except OSError:
        return ""


def detect_languages(root: Path, files: list[Path]) -> list[dict[str, Any]]:
    counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = {}
    for path in files:
        relative = path.relative_to(root).as_posix()
        language = SPECIAL_LANGUAGE_FILES.get(path.name)
        if language is None:
            language = LANGUAGE_BY_EXTENSION.get(path.suffix)
        if language is None:
            continue
        counts[language] += 1
        examples.setdefault(language, [])
        if len(examples[language]) < 4:
            examples[language].append(relative)

    return [
        {"name": language, "files": count, "examples": examples.get(language, [])}
        for language, count in counts.most_common()
    ]


def manifest_matches(name: str, manifest: str) -> bool:
    if "*" not in manifest:
        return name == manifest
    pattern = "^" + re.escape(manifest).replace("\\*", ".*") + "$"
    return re.match(pattern, name) is not None


def detect_manifests(root: Path, files: list[Path]) -> list[str]:
    manifests: list[str] = []
    for path in files:
        for manifest in MANIFEST_NAMES:
            if manifest_matches(path.name, manifest):
                manifests.append(path.relative_to(root).as_posix())
                break
    return sorted(manifests)


def dependency_blob(root: Path, files: list[Path]) -> str:
    interesting = {
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "Cargo.toml",
        "go.mod",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "composer.json",
        "Gemfile",
        "mix.exs",
        "pubspec.yaml",
        "Package.swift",
    }
    parts: list[str] = []
    for path in files:
        if path.name in interesting or path.suffix in {".csproj", ".fsproj"}:
            relative = path.relative_to(root).as_posix()
            parts.append(f"\n# {relative}\n{read_text(path, 80_000)}")
    return "\n".join(parts).lower()


def has_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(needle in text for needle in needles)


def add_surface(surfaces: dict[str, list[str]], key: str, evidence: str) -> None:
    surfaces.setdefault(key, [])
    if evidence not in surfaces[key] and len(surfaces[key]) < 8:
        surfaces[key].append(evidence)


def detect_surfaces(root: Path, files: list[Path], manifests: list[str], dep_text: str) -> dict[str, list[str]]:
    surfaces: dict[str, list[str]] = {}
    paths = [path.relative_to(root).as_posix() for path in files]
    names = {path.name for path in files}
    path_blob = "\n".join(paths).lower()

    if has_any(dep_text, ("react", "next", "vue", "nuxt", "svelte", "@angular/", "vite", "webpack", "astro", "solid-js")):
        add_surface(surfaces, "frontend", "front-end dependency in manifest")
    if any(path.endswith((".tsx", ".jsx", ".vue", ".svelte")) for path in paths):
        add_surface(surfaces, "frontend", "front-end component files")
    if has_any(path_blob, ("src/components/", "app/page.", "pages/index.", "public/index.html")):
        add_surface(surfaces, "frontend", "front-end directory structure")

    if has_any(dep_text, ("express", "fastify", "koa", "hapi", "nestjs", "fastapi", "django", "flask", "starlette", "axum", "actix-web", "rocket", "gin-gonic", "labstack/echo", "gofiber", "spring-boot", "micronaut", "quarkus", "laravel", "symfony", "rails", "phoenix")):
        add_surface(surfaces, "backend_api", "server/API framework dependency")
    if has_any(path_blob, ("routes/", "controllers/", "api/", "openapi", "swagger", "graphql", "schema.graphql")):
        add_surface(surfaces, "backend_api", "API route/schema files")

    if has_any(dep_text, ("prisma", "typeorm", "sequelize", "mongoose", "drizzle", "knex", "sqlalchemy", "alembic", "django", "diesel", "sqlx", "gorm", "hibernate", "entityframework", "ecto")):
        add_surface(surfaces, "database", "database/ORM dependency")
    if has_any(path_blob, ("migrations/", "migration/", "schema.prisma", ".sql", "db/", "database/")):
        add_surface(surfaces, "database", "database schema or migration files")

    if has_any(dep_text, ("openai", "anthropic", "langchain", "llama-index", "llamaindex", "transformers", "sentence-transformers", "pydantic-ai", "vercel ai", "@ai-sdk/", "semantic-kernel")):
        add_surface(surfaces, "ai_llm", "AI/LLM dependency")
    if has_any(path_blob, ("prompt", "rag", "embedding", "vector", "llm", "model_config", "eval")):
        add_surface(surfaces, "ai_llm", "AI/LLM-related file names")

    if has_any(dep_text, ("react-native", "expo", "flutter", "androidx", "swiftui")) or has_any(path_blob, ("android/", "ios/", "pubspec.yaml")):
        add_surface(surfaces, "mobile", "mobile framework or platform files")

    if has_any(dep_text, ("electron", "tauri", "wails")) or has_any(path_blob, ("electron", "tauri.conf", "wails.json")):
        add_surface(surfaces, "desktop", "desktop app framework files")

    if any(path.startswith((".github/workflows/", ".gitlab-ci")) for path in paths) or any(name in names for name in ("Jenkinsfile", "azure-pipelines.yml", "circle.yml")):
        add_surface(surfaces, "ci", "CI workflow files")

    if any(name == "Dockerfile" or name.startswith("docker-compose") for name in names):
        add_surface(surfaces, "deployment", "Docker files")
    if has_any(path_blob, ("k8s/", "kubernetes/", "helm/", ".tf", "terraform", "pulumi", "serverless.yml")):
        add_surface(surfaces, "deployment", "deployment or infrastructure files")

    if any(path.lower().startswith(("readme", "docs/")) or path.endswith(".md") for path in paths):
        add_surface(surfaces, "docs", "README/docs markdown files")

    if any(re.search(r"(^|/)(test|tests|spec|__tests__)/", path.lower()) or re.search(r"(\.|_)(test|spec)\.", path.lower()) for path in paths):
        add_surface(surfaces, "tests", "test/spec files")

    if has_any(dep_text, ("passport", "next-auth", "auth0", "oauth", "openid", "spring-security", "devise", "guardian", "casbin")) or has_any(path_blob, ("auth/", "login", "oauth", "permission", "rbac", "acl")):
        add_surface(surfaces, "auth", "auth-related dependencies or files")

    if has_any(path_blob, ("privacy", "gdpr", "pii", "personal", "user_profile", "billing", "customer", "account")):
        add_surface(surfaces, "privacy", "privacy/user-data-related names")

    if has_any(path_blob, ("cli.", "cmd/", "commands/", "bin/")) or any(name in names for name in ("Makefile",)):
        add_surface(surfaces, "cli", "CLI/script entry files")

    for manifest in manifests:
        if manifest.endswith(("package.json", "pyproject.toml", "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "composer.json", "Gemfile", "mix.exs")):
            add_surface(surfaces, "deployment", "runtime dependency manifests")
            break

    return dict(sorted(surfaces.items()))


def recommendation(
    rec_id: str,
    modes: list[str],
    label_zh: str,
    label_en: str,
    when_zh: str,
    when_en: str,
    reason_zh: str,
    reason_en: str,
    priority: int,
) -> dict[str, Any]:
    return {
        "id": rec_id,
        "modes": modes,
        "labels": {"zh": label_zh, "en": label_en},
        "when": {"zh": when_zh, "en": when_en},
        "reasons": {"zh": reason_zh, "en": reason_en},
        "priority": priority,
    }


def build_recommendations(languages: list[dict[str, Any]], surfaces: dict[str, list[str]]) -> list[dict[str, Any]]:
    language_names = [item["name"] for item in languages[:4]]
    surface_keys = set(surfaces)
    primary_zh = "、".join(language_names) if language_names else "未知语言"
    primary_en = ", ".join(language_names) if language_names else "unknown-language"

    recs = [
        recommendation(
            "full",
            ["full"],
            "全量审计",
            "Full audit",
            "第一次体检、准备发布、接手陌生项目，或你不确定该从哪里看起。",
            "Use this for a first health check, release readiness review, unfamiliar project handoff, or when you are not sure where to start.",
            f"已识别到 {primary_zh} 项目；全量审计会覆盖架构、安全、稳定性、测试、发布、文档等全部维度。",
            f"Detected a {primary_en} project. A full audit covers architecture, security, stability, testing, release, documentation, and the other dimensions.",
            100,
        )
    ]

    if {"backend_api", "auth", "privacy", "ci", "deployment", "database"} & surface_keys:
        modes = ["security", "privacy", "supply-chain", "configuration"]
        if "backend_api" in surface_keys:
            modes.append("backend-api")
        if "database" in surface_keys:
            modes.append("data-integrity")
        recs.append(
            recommendation(
                "security_privacy",
                modes,
                "偏安全与隐私",
                "Security and privacy focused",
                "你最关心认证、权限、输入边界、密钥、依赖供应链或用户数据风险。",
                "Use this when authentication, authorization, input boundaries, secrets, dependency supply chain, or user-data risk matter most.",
                "项目存在安全、隐私、服务端、部署、数据或 CI 线索，适合优先检查攻击面和数据边界。",
                "The project has security, privacy, backend, deployment, data, or CI signals, so attack surface and data boundaries deserve early attention.",
                90,
            )
        )

    if {"frontend", "mobile", "desktop"} & surface_keys:
        recs.append(
            recommendation(
                "frontend_experience",
                ["frontend-state", "accessibility", "performance", "testing"],
                "偏前端体验",
                "Frontend experience focused",
                "你最关心界面状态、可访问性、加载/错误/空状态、响应式体验和前端测试信心。",
                "Use this when UI state, accessibility, loading/error/empty states, responsive behavior, and frontend test confidence matter most.",
                "项目包含前端或客户端 UI 线索，适合检查用户能直接感知的体验和状态管理问题。",
                "The project has frontend or client UI signals, so user-visible experience and state management risks are likely relevant.",
                80,
            )
        )

    if {"backend_api", "database"} & surface_keys:
        modes = ["backend-api", "data-integrity", "stability", "observability"]
        recs.append(
            recommendation(
                "backend_data",
                modes,
                "偏后端接口与数据",
                "Backend API and data focused",
                "你最关心接口契约、校验、事务、幂等、迁移、错误处理和故障定位能力。",
                "Use this when API contracts, validation, transactions, idempotency, migrations, error handling, and debuggability matter most.",
                "项目包含 API 或数据库线索，适合检查请求链路、数据一致性和线上可诊断性。",
                "The project has API or database signals, so request flow, data consistency, and production diagnosis are important.",
                78,
            )
        )

    if {"ci", "deployment"} & surface_keys:
        recs.append(
            recommendation(
                "release_operability",
                ["release", "configuration", "observability", "supply-chain"],
                "偏发布与运维",
                "Release and operability focused",
                "你准备上线、交付、迁移环境，或担心 CI/CD、配置、回滚、健康检查和告警。",
                "Use this before shipping, handoff, environment migration, or when CI/CD, config, rollback, health checks, and alerts are the concern.",
                "项目包含 CI、容器、基础设施或部署清单，适合检查发布可靠性和运行期可控性。",
                "The project has CI, container, infrastructure, or deployment evidence, so release reliability and runtime control are relevant.",
                74,
            )
        )

    if "ai_llm" in surface_keys:
        recs.append(
            recommendation(
                "ai_safety_cost",
                ["ai-safety", "cost", "privacy", "security", "testing"],
                "偏 AI 安全与成本",
                "AI safety and cost focused",
                "你最关心 prompt injection、工具调用授权、RAG 数据泄露、模型 fallback、eval 和账单风险。",
                "Use this when prompt injection, tool authorization, RAG leakage, model fallback, eval coverage, and billing risk matter most.",
                "项目包含 AI/LLM 依赖或文件线索，适合检查模型边界、数据泄露和成本失控风险。",
                "The project has AI/LLM dependency or file signals, so model boundaries, data leakage, and cost-control risks are likely relevant.",
                86,
            )
        )

    if "tests" not in surface_keys:
        recs.append(
            recommendation(
                "testing_confidence",
                ["testing", "testing-authenticity", "stability"],
                "偏测试补强",
                "Testing confidence focused",
                "你想先知道测试是否真的能兜住关键行为，尤其是仓库里测试线索较弱时。",
                "Use this when you first want to know whether the tests protect critical behavior, especially when test signals look weak.",
                "未识别到明显测试目录或测试文件，适合先评估风险最高的测试缺口。",
                "No obvious test directories or test files were detected, so the highest-risk confidence gaps should be checked early.",
                68,
            )
        )

    recs.append(
        recommendation(
            "maintainability_docs",
            ["architecture", "maintainability", "documentation", "comment-coverage", "code-consistency"],
            "偏可维护性与文档",
            "Maintainability and documentation focused",
            "你准备重构、交接、扩展功能，或想知道代码是否容易继续维护。",
            "Use this before refactoring, handoff, feature expansion, or when you want to know whether the code is easy to keep changing.",
            "该组合关注边界、复杂度、一致性、文档和注释有效性，适合作为工程健康度专项检查。",
            "This combination checks boundaries, complexity, consistency, documentation, and comment usefulness as an engineering-health review.",
            60,
        )
    )

    return sorted(recs, key=lambda item: item["priority"], reverse=True)


def build_inventory(root: Path, max_files: int) -> dict[str, Any]:
    files = iter_files(root, max_files)
    languages = detect_languages(root, files)
    manifests = detect_manifests(root, files)
    dep_text = dependency_blob(root, files)
    surfaces = detect_surfaces(root, files, manifests, dep_text)
    recommendations = build_recommendations(languages, surfaces)

    return {
        "root": str(root),
        "files_scanned": len(files),
        "scan_limit_reached": len(files) >= max_files,
        "languages": languages,
        "manifests": manifests[:80],
        "surfaces": [
            {
                "id": key,
                "labels": SURFACE_LABELS.get(key, {"zh": key, "en": key}),
                "evidence": evidence,
            }
            for key, evidence in surfaces.items()
        ],
        "recommendations": recommendations,
    }


def localized(value: dict[str, str], language: str) -> str:
    return value.get(language) or value["en"]


def format_text(inventory: dict[str, Any], language: str, show_modes: bool) -> str:
    joiner = "、" if language == "zh" else ", "
    language_line = joiner.join(
        f"{item['name']}({item['files']})" for item in inventory["languages"][:8]
    ) or ("未识别到主要语言" if language == "zh" else "No primary language detected")
    surface_line = joiner.join(
        localized(surface["labels"], language) for surface in inventory["surfaces"]
    ) or ("未识别到明显项目表面" if language == "zh" else "No obvious project surfaces detected")

    labels = {
        "title": "项目画像" if language == "zh" else "Project inventory",
        "files": "扫描文件数" if language == "zh" else "Files scanned",
        "limit": "（达到扫描上限）" if language == "zh" else " (scan limit reached)",
        "languages": "主要语言" if language == "zh" else "Primary languages",
        "surfaces": "识别表面" if language == "zh" else "Detected surfaces",
        "manifests": "关键清单" if language == "zh" else "Key manifests",
        "recommendations": "审计推荐" if language == "zh" else "Audit recommendations",
        "when": "适合" if language == "zh" else "Best for",
        "reason": "原因" if language == "zh" else "Reason",
        "modes": "内部模式" if language == "zh" else "Internal modes",
    }

    lines = [
        labels["title"],
        f"- {labels['files']}: {inventory['files_scanned']}" + (labels["limit"] if inventory["scan_limit_reached"] else ""),
        f"- {labels['languages']}: {language_line}",
        f"- {labels['surfaces']}: {surface_line}",
    ]

    if inventory["manifests"]:
        lines.append(f"- {labels['manifests']}: " + joiner.join(inventory["manifests"][:12]))

    lines.extend(["", labels["recommendations"]])
    for index, rec in enumerate(inventory["recommendations"][:7], start=1):
        lines.append(f"{index}. {localized(rec['labels'], language)}")
        lines.append(f"   {labels['when']}: {localized(rec['when'], language)}")
        lines.append(f"   {labels['reason']}: {localized(rec['reasons'], language)}")
        if show_modes:
            lines.append(f"   {labels['modes']}: {', '.join(rec['modes'])}")

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Inspect a repository and recommend audit modes with localized user-facing labels.")
    parser.add_argument("root", nargs="?", default=".", type=Path, help="Project root to inspect")
    parser.add_argument("--format", choices=("json", "text"), default="json", help="Output format")
    parser.add_argument("--language", choices=("en", "zh"), default="en", help="Text output language. Use JSON for other user languages and translate in the assistant response.")
    parser.add_argument("--max-files", type=int, default=8000, help="Maximum number of files to scan")
    parser.add_argument("--show-modes", action="store_true", help="Show internal audit mode tokens in text output")
    args = parser.parse_args(argv)
    if args.max_files < 1:
        parser.error("--max-files must be positive")

    root = args.root.resolve()
    if not root.exists() or not root.is_dir():
        print(f"{root}: not a directory", file=sys.stderr)
        return 2

    inventory = build_inventory(root, args.max_files)
    if args.format == "json":
        print(json.dumps(inventory, ensure_ascii=False, indent=2))
    else:
        print(format_text(inventory, args.language, args.show_modes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
