#!/usr/bin/env node

import { existsSync, readFileSync, statSync } from "node:fs";
import { resolve, relative } from "node:path";
import { execFileSync } from "node:child_process";

const args = new Set(process.argv.slice(2));
const skipDrift = args.has("--skip-drift");
const rootArg = process.argv.slice(2).find((arg) => arg.startsWith("--root="));
const repoRoot = resolve(rootArg ? rootArg.slice("--root=".length) : process.cwd());
const manifestPath = resolve(repoRoot, ".agents/context-manifest.json");

const errors = [];
const stale = [];

function fail(message) {
  errors.push(message);
}

function mustExist(path, label = "path") {
  const absolute = resolve(repoRoot, path);
  if (!existsSync(absolute)) {
    fail(`${label} missing: ${path}`);
    return false;
  }
  return true;
}

function git(argsList) {
  return execFileSync("git", ["-C", repoRoot, ...argsList], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  }).trim();
}

function changedPaths(baseCommit, trackedRoots) {
  const paths = new Set();
  const collect = (output) => {
    for (const line of output.split(/\r?\n/)) {
      const value = line.trim();
      if (value) paths.add(value);
    }
  };

  collect(git(["diff", "--name-only", `${baseCommit}..HEAD`, "--", ...trackedRoots]));
  collect(git(["diff", "--name-only", "--", ...trackedRoots]));
  collect(git(["diff", "--cached", "--name-only", "--", ...trackedRoots]));
  return [...paths].sort();
}

if (!mustExist("AGENTS.md", "root router") || !mustExist(".agents/AGENTS.md", "context registry") || !mustExist(".agents/context-manifest.json", "manifest")) {
  // Continue to print all obvious structure errors.
}

let manifest;
try {
  manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
} catch (error) {
  fail(`manifest invalid JSON: ${error instanceof Error ? error.message : String(error)}`);
}

if (manifest) {
  if (manifest.schemaVersion !== 1) fail(`unsupported schemaVersion: ${manifest.schemaVersion}`);
  if (typeof manifest.sourceCommit !== "string" || !/^[0-9a-f]{40}$/.test(manifest.sourceCommit)) {
    fail("manifest.sourceCommit must be a 40-character git SHA");
  }

  for (const legacyPath of manifest.legacyPathsMustNotExist ?? []) {
    if (existsSync(resolve(repoRoot, legacyPath))) {
      fail(`legacy context conflict still exists: ${legacyPath}`);
    }
  }

  const rootRouter = existsSync(resolve(repoRoot, "AGENTS.md")) ? readFileSync(resolve(repoRoot, "AGENTS.md"), "utf8") : "";
  const registry = existsSync(resolve(repoRoot, ".agents/AGENTS.md")) ? readFileSync(resolve(repoRoot, ".agents/AGENTS.md"), "utf8") : "";

  for (const [scopeName, scope] of Object.entries(manifest.scopes ?? {})) {
    mustExist(scope.entry, `${scopeName} entry`);
    if (!rootRouter.includes(scope.entry)) fail(`root router does not reference ${scope.entry}`);
    const registryRelative = scope.entry.replace(/^\.agents\//, "");
    if (!registry.includes(registryRelative)) fail(`context registry does not reference ${registryRelative}`);

    for (const sourceRoot of scope.sourceRoots ?? []) mustExist(sourceRoot, `${scopeName} source root`);
    for (const page of scope.requiredPages ?? []) mustExist(page, `${scopeName} context page`);
    for (const sourcePath of scope.requiredSourcePaths ?? []) mustExist(sourcePath, `${scopeName} verified source`);

    if (scope.mode === "DEEP" && !skipDrift && (scope.trackedRoots?.length ?? 0) > 0) {
      try {
        git(["cat-file", "-e", `${manifest.sourceCommit}^{commit}`]);
        const changed = changedPaths(manifest.sourceCommit, scope.trackedRoots);
        if (changed.length > 0) stale.push({ scope: scopeName, changed });
      } catch (error) {
        fail(`cannot evaluate source drift for ${scopeName}: sourceCommit ${manifest.sourceCommit} is unavailable in this git checkout`);
      }
    }
  }
}

if (stale.length > 0) {
  for (const item of stale) {
    fail(`CONTEXT_STALE ${item.scope}:\n  - ${item.changed.join("\n  - ")}`);
  }
}

if (errors.length > 0) {
  console.error("AGENT_CONTEXT_INVALID");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

const manifestDisplay = relative(repoRoot, manifestPath) || ".agents/context-manifest.json";
console.log(`AGENT_CONTEXT_OK (${manifestDisplay}${skipDrift ? ", drift skipped" : ""})`);
