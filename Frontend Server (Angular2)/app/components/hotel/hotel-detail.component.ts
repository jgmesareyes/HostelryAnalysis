import 'rxjs/add/operator/switchMap';
import { Component, OnInit }      from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { Hotel }                from '../../models/hotel/hotel';
import { HostelryService }      from '../../services/hostelry/hostelry.service';


@Component({
  moduleId: module.id,
  selector: 'hotel-detail',
  templateUrl: './hotel-detail.component.html',
  styleUrls: [ './hotel-detail.component.css' ]
})
export class HotelDetailComponent implements OnInit {
  hotel: Hotel;
  showOption: number = 0;

  constructor(
    private hostelryService: HostelryService,
    private route: ActivatedRoute,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.route.params
      .switchMap((params: Params) => this.hostelryService.getHotel(params['name']))
      .subscribe(hotel => this.hotel = hotel);
  }

  showReviews(): void {
    if (this.showOption != 1) {
      this.showOption = 1;
    } else {
      this.showOption = 0;
    }
  }

  showFacilities(): void {
    if (this.showOption != 2) {
      this.showOption = 2;
    } else {
      this.showOption = 0;
    }
  }

  goBack(): void {
    this.location.back();
  }
}


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/