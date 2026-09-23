#!/usr/bin/env node

import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join, relative, resolve } from "node:path";

const repoRoot = resolve(process.cwd());
const worklogRoot = resolve(repoRoot, ".agents/worklog");

function option(name, fallback = "") {
  const prefix = `--${name}=`;
  const inline = process.argv.find((arg) => arg.startsWith(prefix));
  if (inline) return inline.slice(prefix.length);

  const index = process.argv.indexOf(`--${name}`);
  if (index >= 0 && process.argv[index + 1]) return process.argv[index + 1];
  return fallback;
}

function usage(message) {
  if (message) console.error(`ERROR: ${message}`);
  console.error("Usage: node scripts/select-worklogs.mjs --type <primary_task_type> [--limit 3]");
  process.exitCode = 2;
}

const taskType = option("type").trim();
const limitText = option("limit", "3").trim();
const limit = Number.parseInt(limitText, 10);

if (!taskType) usage("--type is required");
if (!Number.isInteger(limit) || limit < 1) usage("--limit must be a positive integer");
if (!taskType || !Number.isInteger(limit) || limit < 1) process.exit();

if (!existsSync(worklogRoot)) {
  console.error(`ERROR: worklog root missing: ${relative(repoRoot, worklogRoot)}`);
  process.exitCode = 1;
  process.exit();
}

function markdownFiles(directory, output = []) {
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    if (entry.name === "README.md" || entry.name === "TEMPLATE.md") continue;
    const absolute = join(directory, entry.name);
    if (entry.isDirectory()) markdownFiles(absolute, output);
    else if (entry.isFile() && entry.name.endsWith(".md")) output.push(absolute);
  }
  return output;
}

function field(text, name) {
  const frontMatterMatch = text.match(/^---\s*\n([\s\S]*?)\n---/);
  const sources = frontMatterMatch ? [frontMatterMatch[1], text] : [text];
  const patterns = [
    new RegExp(`^\\s*${name}:\\s*["']?([^"'\\n]+?)["']?\\s*$`, "m"),
    new RegExp(`^\\s*-\\s*${name}:\\s*["']?([^"'\\n]+?)["']?\\s*$`, "m"),
  ];

  for (const source of sources) {
    for (const pattern of patterns) {
      const match = source.match(pattern);
      if (match) return match[1].trim();
    }
  }
  return "";
}

function parseWorklog(absolute) {
  const text = readFileSync(absolute, "utf8");
  const primary = field(text, "primary_task_type") || field(text, "task_type");
  const normalizedType = primary.split(/[\\/|]/, 1)[0].trim();
  const date = field(text, "date");
  const path = relative(repoRoot, absolute).split("\\").join("/");
  return {
    path,
    date: /^\d{4}-\d{2}-\d{2}$/.test(date) ? date : "",
    primaryTaskType: normalizedType,
  };
}

const entries = markdownFiles(worklogRoot)
  .map(parseWorklog)
  .filter((entry) => entry.primaryTaskType === taskType)
  .sort((left, right) => {
    const dateOrder = right.date.localeCompare(left.date);
    return dateOrder || left.path.localeCompare(right.path);
  });

const selected = entries.slice(0, limit);
const shortage = Math.max(0, limit - entries.length);

console.log("WORKLOG_PREFLIGHT");
console.log(`primary_task_type: ${taskType}`);
console.log(`requested: ${limit}`);
console.log(`available: ${entries.length}`);
console.log(`selected: ${selected.length}`);
console.log(`status: ${shortage ? "SHORTAGE" : "READY"}`);
if (shortage) {
  console.log(`shortage: ${shortage}`);
  console.log("shortage_policy: read_all_available_and_record_shortage");
}
for (const entry of selected) console.log(`- ${entry.path}`);
