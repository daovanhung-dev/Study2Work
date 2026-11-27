import { Component, Input } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  imports: [RouterLink, RouterLinkActive],
  selector: 'study-st03-profile-frame',
  styleUrl: './st03-profile-frame.css',
  templateUrl: './st03-profile-frame.html',
})
export class ST03ProfileFrame {
  @Input() fullName: string | null = null;
}
