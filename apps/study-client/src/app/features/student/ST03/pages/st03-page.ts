import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  imports: [RouterLink, RouterLinkActive],
  selector: 'study-st03-page',
  templateUrl: './st03-page.html',
})
export class ST03Page {
  preventSubmit(event: SubmitEvent): void {
    event.preventDefault();
  }
}
