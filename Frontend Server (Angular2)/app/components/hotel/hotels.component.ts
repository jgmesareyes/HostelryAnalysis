import { Component, OnInit } from '@angular/core';
import { Router }            from '@angular/router';

import { Hotel }                from '../../models/hotel/hotel';
import { HostelryService }      from '../../services/hostelry/hostelry.service';


@Component({
  moduleId: module.id,
  selector: 'hotels',
  templateUrl: './hotels.component.html',
  styleUrls: [ './hotels.component.css' ]
})
export class HotelsComponent implements OnInit {
  hotels: Hotel[]
  selectedHotel: Hotel;
  message: string;

  constructor(
    private hostelryService: HostelryService,
    private router: Router) { }

  getHotels(): void {
    this.hostelryService
        .getHotels()
        .then(results => this.hotels = results);
  }

/*
  getMessage(): void {
    this.hostelryService
        .getMessage()
        .subscribe((data) => this.message = data.message);
  }
*/

  ngOnInit(): void {
    this.getHotels();
    //this.getMessage();
  }

  onSelect(hotel: Hotel): void {
    this.selectedHotel = hotel;
  }

  gotoDetail(): void {
    this.router.navigate(['/hotel', this.selectedHotel.name]);
  }
}


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/