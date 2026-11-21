import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  imports: [RouterLink, RouterLinkActive],
  selector: 'study-student-public-frame',
  templateUrl: './student-public-frame.html',
  styleUrl: './student-public-frame.css',
})
export class StudentPublicFrame {}
