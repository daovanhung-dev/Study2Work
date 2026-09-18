#!/usr/bin/env node

import { existsSync, readFileSync, readdirSync } from "node:fs";
import { basename, dirname, relative, resolve } from "node:path";
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

const SKIP_DIRS = new Set([".git", "node_modules", ".venv", ".dart_tool", "build"]);

function collectFiles(path, output = []) {
  const absolute = resolve(repoRoot, path);
  if (!existsSync(absolute)) return output;

  for (const entry of readdirSync(absolute, { withFileTypes: true })) {
    if (SKIP_DIRS.has(entry.name)) continue;
    const child = resolve(absolute, entry.name);
    const childRelative = relative(repoRoot, child);
    if (entry.isDirectory()) collectFiles(childRelative, output);
    else output.push(childRelative);
  }
  return output;
}

function collectDirectories(path, output = []) {
  const absolute = resolve(repoRoot, path);
  if (!existsSync(absolute)) return output;

  for (const entry of readdirSync(absolute, { withFileTypes: true })) {
    if (SKIP_DIRS.has(entry.name)) continue;
    const child = resolve(absolute, entry.name);
    const childRelative = relative(repoRoot, child);
    if (entry.isDirectory()) {
      output.push(childRelative);
      collectDirectories(childRelative, output);
    }
  }
  return output;
}

function contextFiles(manifest) {
  const roots = [".agents/project"];
  for (const scope of Object.values(manifest.scopes ?? {})) {
    roots.push(dirname(scope.entry));
  }
  return [...new Set(roots.flatMap((root) => collectFiles(root)))].sort();
}

function registeredContextFiles(manifest) {
  const registered = new Set([".agents/AGENTS.md"]);
  if (manifest.project) {
    registered.add(manifest.project.index);
    for (const page of manifest.project.pages ?? []) registered.add(page);
  }
  for (const scope of Object.values(manifest.scopes ?? {})) {
    registered.add(scope.entry);
    registered.add(scope.index);
    for (const page of scope.pages ?? scope.requiredPages ?? []) registered.add(page);
  }
  return registered;
}

function checkPageGraph(manifest, registry) {
  if (manifest.project) {
    mustExist(manifest.project.index, "project context index");
    const index = existsSync(resolve(repoRoot, manifest.project.index))
      ? readFileSync(resolve(repoRoot, manifest.project.index), "utf8")
      : "";
    for (const page of manifest.project.pages ?? []) {
      mustExist(page, "project context page");
      if (!index.includes(basename(page))) {
        fail(`project index does not reference ${page}`);
      }
    }
  }

  for (const [scopeName, scope] of Object.entries(manifest.scopes ?? {})) {
    mustExist(scope.index, `${scopeName} context index`);
    const entry = existsSync(resolve(repoRoot, scope.entry))
      ? readFileSync(resolve(repoRoot, scope.entry), "utf8")
      : "";
    if (!entry.includes(basename(scope.index))) {
      fail(`${scopeName} entry does not reference ${scope.index}`);
    }

    const index = existsSync(resolve(repoRoot, scope.index))
      ? readFileSync(resolve(repoRoot, scope.index), "utf8")
      : "";
    for (const page of scope.pages ?? scope.requiredPages ?? []) {
      mustExist(page, `${scopeName} context page`);
      if (!index.includes(basename(page))) {
        fail(`${scopeName} index does not reference ${page}`);
      }
    }
  }

  if (!registry.includes("project/INDEX.md")) {
    fail("context registry does not reference project/INDEX.md");
  }
}

function checkInternalLinks(manifest) {
  const files = ["AGENTS.md", ".agents/AGENTS.md", ...contextFiles(manifest)];
  const markdownLink = /\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g;

  for (const file of files) {
    if (!existsSync(resolve(repoRoot, file))) continue;
    const source = readFileSync(resolve(repoRoot, file), "utf8");
    for (const match of source.matchAll(markdownLink)) {
      const rawTarget = match[1];
      if (/^(https?:|mailto:|#)/.test(rawTarget)) continue;
      const target = rawTarget.split("#", 1)[0];
      if (!target) continue;
      const absolute = target.startsWith("/")
        ? resolve(repoRoot, target.slice(1))
        : resolve(dirname(resolve(repoRoot, file)), target);
      if (!existsSync(absolute)) {
        fail(`broken context link: ${file} -> ${rawTarget}`);
      }
    }
  }
}

function checkNoAgentContextInApps() {
  for (const path of collectFiles("apps")) {
    if (path.endsWith("/AGENTS.md") || path.includes("/.agent/")) {
      fail(`agent context must live under .agents: ${path}`);
    }
  }
  for (const path of collectDirectories("apps")) {
    if (path.endsWith("/.agent")) {
      fail(`agent context directory must live under .agents: ${path}`);
    }
  }
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
  if (manifest.schemaVersion !== 2) fail(`unsupported schemaVersion: ${manifest.schemaVersion}`);
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

  checkNoAgentContextInApps();
  checkPageGraph(manifest, registry);

  const registered = registeredContextFiles(manifest);
  for (const file of contextFiles(manifest)) {
    if (!registered.has(file)) fail(`ORPHAN_CONTEXT_PAGE ${file}`);
  }
  checkInternalLinks(manifest);

  for (const [scopeName, scope] of Object.entries(manifest.scopes ?? {})) {
    mustExist(scope.entry, `${scopeName} entry`);
    if (!rootRouter.includes(scope.entry)) fail(`root router does not reference ${scope.entry}`);
    const registryRelative = scope.entry.replace(/^\.agents\//, "");
    if (!registry.includes(registryRelative)) fail(`context registry does not reference ${registryRelative}`);

    for (const sourceRoot of scope.sourceRoots ?? []) mustExist(sourceRoot, `${scopeName} source root`);
    for (const page of scope.pages ?? scope.requiredPages ?? []) mustExist(page, `${scopeName} context page`);
    for (const sourcePath of scope.requiredSourcePaths ?? []) mustExist(sourcePath, `${scopeName} verified source`);

    if (scope.mode === "DEEP" && !skipDrift && (scope.trackedRoots?.length ?? 0) > 0) {
      try {
        git(["cat-file", "-e", `${manifest.sourceCommit}^{commit}`]);
        const changed = changedPaths(manifest.sourceCommit, scope.trackedRoots);
        if (changed.length > 0) stale.push({ scope: scopeName, changed });
      } catch (error) {
        const detail = error instanceof Error ? error.message : String(error);
        fail(`cannot evaluate source drift for ${scopeName}: ${detail}`);
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
