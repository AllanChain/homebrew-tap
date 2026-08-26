#!/usr/bin/env python3

"""Print Homebrew cask SHA lines for the Sane Break macOS release assets.

The script prefers the GitHub release asset digest returned by:

    gh release view <tag> --repo AllanChain/sane-break --json tagName,assets

At the time of writing, GitHub exposes asset digests as strings like
``sha256:<hex>`` in the JSON payload. If a matching asset does not include a
digest, this script falls back to downloading the asset and hashing it locally.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import urllib.request
from pathlib import Path


REPO = "AllanChain/sane-break"
ARM_ASSET = "sane-break-macos-arm64.dmg"
INTEL_ASSET = "sane-break-macos-x86_64.dmg"

# Repository layout: scripts/sane_break_sha.py sits next to Casks/.
DEFAULT_CASK = Path(__file__).resolve().parents[1] / "Casks" / "sane-break.rb"

VERSION_RE = re.compile(r'^(\s*version\s+")[^"]+("\s*)$', re.MULTILINE)
SHA256_BLOCK_RE = re.compile(
    r'(sha256 arm:\s+")([0-9a-f]{64})(",\s+intel:\s+")([0-9a-f]{64})(")'
)


def run_gh_release_view(tag: str | None) -> dict:
    cmd = ["gh", "release", "view", "--repo", REPO, "--json", "tagName,assets"]
    if tag:
        cmd.insert(3, tag)
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def find_asset(release: dict, asset_name: str) -> dict:
    for asset in release["assets"]:
        if asset["name"] == asset_name:
            return asset
    raise SystemExit(f"missing asset in release payload: {asset_name}")


def sha256_from_url(url: str) -> str:
    hasher = hashlib.sha256()
    with urllib.request.urlopen(url) as response:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def resolve_sha256(asset: dict) -> tuple[str, str]:
    digest = asset.get("digest", "")
    if digest.startswith("sha256:"):
        return digest.removeprefix("sha256:"), "github-api-digest"
    return sha256_from_url(asset["url"]), "downloaded-and-hashed"


def update_cask_file(
    cask_path: Path, version: str, arm_sha: str, intel_sha: str
) -> list[str]:
    """Rewrite the cask file in place. Returns a list of human-readable changes."""
    original = cask_path.read_text(encoding="utf-8")
    changes: list[str] = []

    def replace_version(match: re.Match[str]) -> str:
        old = match.group(0)
        new = f'{match.group(1)}{version}{match.group(2)}'
        if new != old:
            changes.append(f'version -> "{version}"')
        return new

    def replace_shas(match: re.Match[str]) -> str:
        old_arm, old_intel = match.group(2), match.group(4)
        if old_arm != arm_sha:
            changes.append(f"arm64 sha256 -> {arm_sha}")
        if old_intel != intel_sha:
            changes.append(f"intel sha256 -> {intel_sha}")
        return (
            f"{match.group(1)}{arm_sha}{match.group(3)}{intel_sha}{match.group(5)}"
        )

    updated = VERSION_RE.sub(replace_version, original, count=1)
    updated = SHA256_BLOCK_RE.sub(replace_shas, updated, count=1)

    if updated == original:
        return changes  # empty: nothing to write

    cask_path.write_text(updated, encoding="utf-8")
    return changes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch Sane Break release metadata and print Homebrew cask sha256 "
            "entries for the macOS arm64 and x86_64 DMGs. With --write, also "
            "updates the version and sha256 lines in the cask file."
        )
    )
    parser.add_argument(
        "tag",
        nargs="?",
        help="Release tag such as v0.10.0. Defaults to the latest GitHub release.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Update the cask file in place instead of only printing entries.",
    )
    parser.add_argument(
        "--cask",
        type=Path,
        default=DEFAULT_CASK,
        help=f"Path to the cask file to edit (default: {DEFAULT_CASK}).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    release = run_gh_release_view(args.tag)
    tag_name = release["tagName"]
    version = tag_name.removeprefix("v")

    arm_asset = find_asset(release, ARM_ASSET)
    intel_asset = find_asset(release, INTEL_ASSET)

    arm_sha, arm_source = resolve_sha256(arm_asset)
    intel_sha, intel_source = resolve_sha256(intel_asset)

    print(
        f"# Source: gh release view {tag_name} --repo {REPO} --json tagName,assets"
    )
    print(
        "# Note: GitHub currently includes release asset digests in the API as "
        "`digest: sha256:...`."
    )
    print(f"# arm64 source: {arm_source}")
    print(f"# intel source: {intel_source}")
    print()
    print(f'version "{version}"')
    print(f'sha256 arm:   "{arm_sha}",')
    print(f'       intel: "{intel_sha}"')

    if args.write:
        if not args.cask.is_file():
            raise SystemExit(f"cask file not found: {args.cask}")
        changes = update_cask_file(args.cask, version, arm_sha, intel_sha)
        if changes:
            print(f"\nUpdated {args.cask}:")
            for change in changes:
                print(f"  - {change}")
        else:
            print(f"\n{args.cask} already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
