import { Component, OnInit }                 from '@angular/core';
import { Router, ActivatedRoute, Params }    from '@angular/router';

import { Statistics }           from '../../models/statistic/statistics';
import { HostelryService }      from '../../services/hostelry/hostelry.service';


@Component({
  moduleId: module.id,
  selector: 'results',
  templateUrl: './results.component.html',
  styleUrls: [ './results.component.css' ]
})
export class ResultsComponent implements OnInit {
  statistics: Statistics[];
  sectorStatistics: Statistics;
  statisticsMode: number = 1;
//  sectorId: number = 1;

  constructor(
    private hostelryService: HostelryService,
    private router: Router,
    private route: ActivatedRoute) { }

  getKeywords(): void {
    this.hostelryService
        .getKeywords()
        .then(statistics => this.statistics = statistics);
  }

  getFeatures(): void {
    this.hostelryService
        .getFeatures()
        .then(statistics => this.statistics = statistics);
  }

  ngOnInit(): void {
    this.getKeywords();
  }

  changeStatisticsMode(): void {
    if (this.statisticsMode != 1) {
      this.statisticsMode = 1;
      this.getKeywords();
    } else {
      this.statisticsMode = 0;
      this.getFeatures();
    }
    this.sectorStatistics = null;
  }

  /*
  getKeyword(): void {
    this.hostelryService.getKeyword(this.sectorId)
        .then(statistics => this.sectorStatistics = statistics);
  }

  changeSectorId(): void {
    if (this.sectorId != 1) {
      this.sectorId = 1;
    } else {
      this.sectorId = 2;
    }
  }

  submitResult(): void {
    this.getKeyword();
  }
*/

}


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/