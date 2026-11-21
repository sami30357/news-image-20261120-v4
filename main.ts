import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "output";
mkdirSync(outDir, { recursive: true });
const png = readFileSync(new URL("./entry.png", import.meta.url));
writeFileSync(join(outDir, "entry.png"), png);
