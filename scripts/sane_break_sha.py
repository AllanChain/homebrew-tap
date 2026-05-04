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
import subprocess
import urllib.request


REPO = "AllanChain/sane-break"
ARM_ASSET = "sane-break-macos-arm64.dmg"
INTEL_ASSET = "sane-break-macos-x86_64.dmg"


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch Sane Break release metadata and print Homebrew cask sha256 "
            "entries for the macOS arm64 and x86_64 DMGs."
        )
    )
    parser.add_argument(
        "tag",
        nargs="?",
        help="Release tag such as v0.10.0. Defaults to the latest GitHub release.",
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
