import { BriefcaseBusiness } from "lucide-react";

import { workApiBaseUrl } from "../shared/api/http";

export function HomePage() {
  return (
    <main className="shell">
      <section className="hero" aria-labelledby="work-title">
        <div className="title-row">
          <BriefcaseBusiness aria-hidden="true" size={32} />
          <p className="eyebrow">Work subsystem</p>
        </div>
        <h1 id="work-title">Study2Work Work</h1>
        <p className="summary">
          Career profiles, CVs, jobs, applications, enterprise workflow, and Study evidence
          visibility will live here.
        </p>
        <dl className="facts">
          <div>
            <dt>API</dt>
            <dd>{workApiBaseUrl}</dd>
          </div>
          <div>
            <dt>Health</dt>
            <dd>/health/live</dd>
          </div>
        </dl>
      </section>
    </main>
  );
}
