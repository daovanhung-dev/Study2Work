import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

import { ST03Page } from './st03-page';

describe('ST03Page', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ST03Page],
      providers: [provideRouter([])],
    }).compileComponents();
  });

  it('renders the G-03 contract gate and keeps unsupported actions disabled', () => {
    const fixture = TestBed.createComponent(ST03Page);
    fixture.detectChanges();

    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('[data-screen-id="ST-03"]')).not.toBeNull();
    expect(root.textContent).toContain('Gate G-03');
    expect(root.textContent).toContain('API #13');
    expect(root.textContent).toContain('API #14');
    expect(root.querySelector<HTMLButtonElement>('.profile-edit-upload')?.disabled).toBe(true);
    expect(root.querySelector<HTMLButtonElement>('.profile-edit-save')?.disabled).toBe(true);
    expect(root.querySelector<HTMLInputElement>('#st03-phone')?.disabled).toBe(true);
    expect(root.querySelector<HTMLTextAreaElement>('#st03-bio')?.disabled).toBe(true);
  });

  it('does not submit profile data while the contract gate is closed', () => {
    const fixture = TestBed.createComponent(ST03Page);
    fixture.detectChanges();

    const form = fixture.nativeElement.querySelector('form') as HTMLFormElement;
    const event = new Event('submit', { bubbles: true, cancelable: true });
    form.dispatchEvent(event);

    expect(event.defaultPrevented).toBe(true);
  });
});
