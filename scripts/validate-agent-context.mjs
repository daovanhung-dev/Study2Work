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

function contextNodes(manifest) {
  const nodes = [];
  const visit = (name, node, parent = null) => {
    nodes.push({ name, node, parent });
    for (const [childName, child] of Object.entries(node.subcontexts ?? {})) {
      visit(`${name}/${childName}`, child, name);
    }
  };

  for (const [scopeName, scope] of Object.entries(manifest.scopes ?? {})) {
    visit(scopeName, scope);
  }
  return nodes;
}

function contextFiles(manifest) {
  // Worklog entries are audit records, not context pages. They are validated
  // through the worklog registry and preflight selector instead of the page
  // graph/orphan-page check.
  const roots = [".agents/project"];
  for (const { node } of contextNodes(manifest)) roots.push(dirname(node.entry));
  return [...new Set(roots.flatMap((root) => collectFiles(root)))].sort();
}

function skillFiles() {
  return collectFiles(".agents/skills").filter((file) => file.endsWith(".md"));
}

function resourceFiles(path) {
  if (!existsSync(resolve(repoRoot, path))) return [];
  return collectFiles(path).length > 0 ? collectFiles(path) : [path];
}

function registeredContextFiles(manifest) {
  const registered = new Set([".agents/AGENTS.md"]);
  if (manifest.project) {
    registered.add(manifest.project.index);
    for (const page of manifest.project.pages ?? []) registered.add(page);
  }
  for (const { node } of contextNodes(manifest)) {
    registered.add(node.entry);
    registered.add(node.index);
    for (const page of node.pages ?? node.requiredPages ?? []) registered.add(page);
  }
  if (manifest.worklog) {
    registered.add(manifest.worklog.index);
    registered.add(manifest.worklog.template);
  }
  if (manifest.contextMap) registered.add(manifest.contextMap);
  if (manifest.skillsIndex) registered.add(manifest.skillsIndex);
  for (const skill of Object.values(manifest.skills ?? {})) {
    registered.add(skill.entry);
    for (const resourcePath of skill.resourcePaths ?? []) {
      for (const file of resourceFiles(resourcePath)) registered.add(file);
    }
  }
  return registered;
}

function checkContextNode(label, node, parentIndexText = "") {
  mustExist(node.entry, `${label} entry`);
  mustExist(node.index, `${label} context index`);
  const entry = existsSync(resolve(repoRoot, node.entry))
    ? readFileSync(resolve(repoRoot, node.entry), "utf8")
    : "";
  if (!entry.includes(basename(node.index))) {
    fail(`${label} entry does not reference ${node.index}`);
  }

  const index = existsSync(resolve(repoRoot, node.index))
    ? readFileSync(resolve(repoRoot, node.index), "utf8")
    : "";
  for (const page of node.pages ?? node.requiredPages ?? []) {
    mustExist(page, `${label} context page`);
    if (!index.includes(basename(page))) fail(`${label} index does not reference ${page}`);
  }
  if (parentIndexText && node.entry !== node.index && !parentIndexText.includes(basename(node.entry))) {
    fail(`${label} parent index does not reference ${node.entry}`);
  }
  return index;
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

  for (const { name, node, parent } of contextNodes(manifest)) {
    const parentIndex = parent
      ? contextNodes(manifest).find((item) => item.name === parent)?.node.index
      : "";
    const parentText = parentIndex && existsSync(resolve(repoRoot, parentIndex))
      ? readFileSync(resolve(repoRoot, parentIndex), "utf8")
      : "";
    checkContextNode(name, node, parentText);
  }

  if (!registry.includes("project/INDEX.md")) {
    fail("context registry does not reference project/INDEX.md");
  }
}

const VALID_STATUSES = new Set([
  "VERIFIED",
  "SOURCE_BACKED",
  "SOURCE_BACKED_WITH_TEST_BLOCKER",
  "SOURCE_BACKED_SKELETON",
  "VERIFIED_EXPRESS_JSON_API",
  "VERIFIED_REACT_EXPRESS_SPLIT",
  "VERIFIED_WITH_UNWIRED_COMPONENTS",
  "VERIFIED_WITH_BLOCKED_GENERATOR",
  "UNWIRED",
  "EMPTY_PLACEHOLDER",
  "SKELETON_ONLY",
  "NOT_FOUND",
  "SOURCE_REQUIRED",
  "DECLARED_NOT_RUNNABLE",
  "DISCREPANCY",
  "SOURCE_CHANGED",
  "CONTEXT_STALE",
]);

function checkStatus(status, label) {
  if (typeof status !== "string" || !VALID_STATUSES.has(status)) {
    fail(`${label} has unsupported status: ${status}`);
  }
}

function checkRegistries(manifest) {
  const scopeNames = new Set(Object.keys(manifest.scopes ?? {}));
  scopeNames.add("all");
  for (const { name, node } of contextNodes(manifest)) {
    checkStatus(node.status, `${name} context`);
    for (const sourceRoot of node.sourceRoots ?? []) mustExist(sourceRoot, `${name} source root`);
    for (const sourcePath of node.requiredSourcePaths ?? []) mustExist(sourcePath, `${name} verified source`);
    for (const skillRef of node.skillRefs ?? []) {
      if (!manifest.skills?.[skillRef]) {
        fail(`${name} references unknown skill ${skillRef}`);
      } else if (!(manifest.skills[skillRef].scopeRefs ?? []).includes(name)) {
        fail(`${name} skill reference ${skillRef} is missing the scope reference`);
      }
    }
  }

  if (!manifest.worklog) fail("worklog registry is missing");
  else {
    mustExist(manifest.worklog.root, "worklog root");
    mustExist(manifest.worklog.index, "worklog index");
    mustExist(manifest.worklog.template, "worklog template");
    const preflight = manifest.worklog.preflight;
    if (!preflight || typeof preflight !== "object") {
      fail("worklog preflight registry is missing");
    } else {
      mustExist(preflight.script, "worklog preflight script");
      if (preflight.typeField !== "primary_task_type") {
        fail("worklog preflight must match primary_task_type");
      }
      if (preflight.limit !== 3) fail("worklog preflight limit must be 3");
      if (preflight.shortagePolicy !== "read_all_available_and_record_shortage") {
        fail("worklog preflight shortagePolicy is invalid");
      }
    }
    const worklogIndex = existsSync(resolve(repoRoot, manifest.worklog.index))
      ? readFileSync(resolve(repoRoot, manifest.worklog.index), "utf8")
      : "";
    if (!worklogIndex.includes(basename(manifest.worklog.template))) {
      fail("worklog index does not reference its template");
    }
    const templateText = existsSync(resolve(repoRoot, manifest.worklog.template))
      ? readFileSync(resolve(repoRoot, manifest.worklog.template), "utf8")
      : "";
    const normalizedTemplate = templateText.toLowerCase().replace(/[^a-z0-9]+/g, "_");
    for (const field of manifest.worklog.requiredFields ?? []) {
      if (!field.trim()) fail("worklog requiredFields contains an empty field");
      else if (!normalizedTemplate.includes(field.toLowerCase())) {
        fail(`worklog template is missing required field ${field}`);
      }
    }
  }

  if (manifest.skillsIndex) mustExist(manifest.skillsIndex, "skills index");
  if (!manifest.contextMap) fail("contextMap registry is missing");
  else mustExist(manifest.contextMap, "context map");
  for (const [skillName, skill] of Object.entries(manifest.skills ?? {})) {
    checkStatus(skill.status, `skill ${skillName}`);
    mustExist(skill.entry, `skill ${skillName} entry`);
    if (!Array.isArray(skill.triggers) || skill.triggers.length === 0) {
      fail(`skill ${skillName} must define triggers`);
    }
    for (const scope of skill.scopeRefs ?? []) {
      if (!scopeNames.has(scope) && ![...contextNodes(manifest).map((item) => item.name)].includes(scope)) {
        fail(`skill ${skillName} references unknown scope ${scope}`);
      }
    }
    for (const workflowRef of skill.workflowRefs ?? []) {
      if (!manifest.workflows?.[workflowRef]) {
        fail(`skill ${skillName} references unknown workflow ${workflowRef}`);
      }
    }
    for (const resourcePath of skill.resourcePaths ?? []) mustExist(resourcePath, `skill ${skillName} resource`);
  }

  for (const [workflowName, workflow] of Object.entries(manifest.workflows ?? {})) {
    checkStatus(workflow.status, `workflow ${workflowName}`);
    mustExist(workflow.entry, `workflow ${workflowName} entry`);
    if (!Array.isArray(workflow.triggers) || workflow.triggers.length === 0) {
      fail(`workflow ${workflowName} must define triggers`);
    }
    if (!Array.isArray(workflow.verificationCommands) || workflow.verificationCommands.length === 0) {
      fail(`workflow ${workflowName} must define verificationCommands`);
    }
    if (workflow.preflight === "worklog.preflight" && !manifest.worklog?.preflight) {
      fail(`workflow ${workflowName} references missing worklog preflight`);
    }
    for (const scope of workflow.scopeRefs ?? []) {
      if (!scopeNames.has(scope)) fail(`workflow ${workflowName} references unknown scope ${scope}`);
    }
  }

  for (const [contractName, contract] of Object.entries(manifest.contracts ?? {})) {
    checkStatus(contract.status, `contract ${contractName}`);
    mustExist(contract.path, `contract ${contractName} path`);
    if (!contract.producer || !Array.isArray(contract.consumers)) {
      fail(`contract ${contractName} must define producer and consumers`);
    }
  }
}

function checkContextMap(manifest) {
  if (!manifest.contextMap || !existsSync(resolve(repoRoot, manifest.contextMap))) return;

  const mapText = readFileSync(resolve(repoRoot, manifest.contextMap), "utf8");
  const required = new Set([
    manifest.rootRouter,
    manifest.registry,
    manifest.contextMap,
    manifest.skillsIndex,
  ]);

  if (manifest.project) {
    required.add(manifest.project.index);
    for (const page of manifest.project.pages ?? []) required.add(page);
  }

  for (const { node } of contextNodes(manifest)) {
    required.add(node.entry);
    required.add(node.index);
    for (const page of node.pages ?? node.requiredPages ?? []) required.add(page);
  }

  for (const skill of Object.values(manifest.skills ?? {})) {
    required.add(skill.entry);
    for (const resourcePath of skill.resourcePaths ?? []) required.add(resourcePath);
  }

  for (const workflow of Object.values(manifest.workflows ?? {})) required.add(workflow.entry);
  for (const contract of Object.values(manifest.contracts ?? {})) required.add(contract.path);

  if (manifest.worklog) {
    required.add(manifest.worklog.root);
    required.add(manifest.worklog.index);
    required.add(manifest.worklog.template);
    if (manifest.worklog.preflight?.script) required.add(manifest.worklog.preflight.script);
  }

  for (const path of required) {
    if (typeof path === "string" && !mapText.includes(path)) {
      fail(`context map does not mention ${path}`);
    }
  }
}

function checkInternalLinks(manifest) {
  // Skill bodies contain intentional template/example placeholders such as
  // `./07_<mapping>.md`; validate the skill registry/index links here and
  // validate resource existence separately, but do not treat those examples
  // as repository context page links.
  const registryFiles = [manifest.skillsIndex, manifest.contextMap].filter(Boolean);
  const files = ["AGENTS.md", ".agents/AGENTS.md", ...contextFiles(manifest), ...registryFiles];
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
  if (manifest.schemaVersion !== 3) fail(`unsupported schemaVersion: ${manifest.schemaVersion}`);
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

  if (manifest.contextMap) {
    if (!rootRouter.includes(manifest.contextMap)) {
      fail(`root router does not reference ${manifest.contextMap}`);
    }
    const mapRelative = manifest.contextMap.replace(/^\.agents\//, "");
    if (!registry.includes(mapRelative)) {
      fail(`context registry does not reference ${mapRelative}`);
    }
  }

  checkNoAgentContextInApps();
  checkPageGraph(manifest, registry);
  checkRegistries(manifest);
  checkContextMap(manifest);

  const registered = registeredContextFiles(manifest);
  for (const file of contextFiles(manifest)) {
    if (!registered.has(file)) fail(`ORPHAN_CONTEXT_PAGE ${file}`);
  }
  for (const file of skillFiles()) {
    if (!registered.has(file)) fail(`ORPHAN_SKILL_RESOURCE ${file}`);
  }
  checkInternalLinks(manifest);

  for (const [scopeName, scope] of Object.entries(manifest.scopes ?? {})) {
    mustExist(scope.entry, `${scopeName} entry`);
    if (!rootRouter.includes(scope.entry)) fail(`root router does not reference ${scope.entry}`);
    const registryRelative = scope.entry.replace(/^\.agents\//, "");
    if (!registry.includes(registryRelative)) fail(`context registry does not reference ${registryRelative}`);
  }

  for (const { name, node } of contextNodes(manifest)) {
    if (node.mode === "DEEP" && !skipDrift && (node.trackedRoots?.length ?? 0) > 0) {
      try {
        git(["cat-file", "-e", `${manifest.sourceCommit}^{commit}`]);
        const changed = changedPaths(manifest.sourceCommit, node.trackedRoots);
        if (changed.length > 0) stale.push({ scope: name, changed });
      } catch (error) {
        const detail = error instanceof Error ? error.message : String(error);
        fail(`cannot evaluate source drift for ${name}: ${detail}`);
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
