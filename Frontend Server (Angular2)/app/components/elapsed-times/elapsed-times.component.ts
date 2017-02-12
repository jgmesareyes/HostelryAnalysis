import 'rxjs/add/operator/switchMap';
import { Component, OnInit }      from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { ElapsedTimes }         from '../../models/elapsed-times/elapsed-times';
import { HostelryService }      from '../../services/hostelry/hostelry.service';


@Component({
  moduleId: module.id,
  selector: 'elapsed-times',
  templateUrl: './elapsed-times.component.html',
  styleUrls: [ './elapsed-times.component.css' ]
})
export class ElapsedTimesComponent implements OnInit {
  elapsedTimes: ElapsedTimes;
  showOption: number = 0;

  constructor(
    private hostelryService: HostelryService,
    private route: ActivatedRoute,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.route.params
      .switchMap((params: Params) => this.hostelryService.getElapsedTimes())
      .subscribe(elapsedTimes => this.elapsedTimes = elapsedTimes);
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