import { Component, input } from '@angular/core';

@Component({
  selector: 'study-mentor-page-header',
  template: `
    <header class="mentor-page-header">
      <div>
        <p class="mentor-page-eyebrow">MENTOR WORKSPACE</p>
        <h1>{{ title() }}</h1>
        @if (description()) { <p class="mentor-page-description">{{ description() }}</p> }
      </div>
      @if (apiLabel()) { <span class="mentor-api-label">Study API {{ apiLabel() }}</span> }
    </header>
  `,
  styles: `
    :host { display: block; }
    .mentor-page-header { display:flex; align-items:flex-start; justify-content:space-between; gap:18px; margin:0 0 24px; }
    .mentor-page-eyebrow { margin:0 0 7px; color:#0b719e; font-size:10px; font-weight:850; letter-spacing:.13em; }
    h1 { margin:0; color:#17324b; font-size:clamp(24px,3vw,32px); letter-spacing:-.035em; line-height:1.2; }
    .mentor-page-description { max-width:720px; margin:9px 0 0; color:#637991; font-size:14px; line-height:1.55; }
    .mentor-api-label { flex:none; padding:7px 10px; border:1px solid #cfe4ef; border-radius:999px; background:#f4fbfe; color:#28657f; font-size:11px; font-weight:750; }
    @media(max-width:560px){.mentor-page-header{display:block}.mentor-api-label{display:inline-flex;margin-top:12px}}
  `,
})
export class MentorPageHeader {
  readonly title = input.required<string>();
  readonly description = input<string>('');
  readonly apiLabel = input<string>('');
}
